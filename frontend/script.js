const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

const WIDTH = 100;
const HEIGHT = 100;
console.log(`Dimensions du canvas :\nWIDTH = ${WIDTH}\nHEIGHT = ${HEIGHT}`);

const arrayBuffer = new ArrayBuffer(WIDTH * HEIGHT * 4);

function loadFile(filePath) {
	var result = null;
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open("GET", filePath, false);
	xmlhttp.send();
	if (xmlhttp.status==200) {
		result = xmlhttp.responseText;
	}
	return result;
}

function shader(pixels){
	for (let y = 0; y < HEIGHT; y++) {
		for (let x = 0; x < WIDTH; x++) {
			const i = (y*WIDTH + x) * 4;
			pixels[i  ] = x;   // red
			pixels[i+1] = y;   // green
			pixels[i+2] = 0;   // blue
			pixels[i+3] = 255; // alpha
		}
	}
}

function limitNumberWithinRange(num, min, max){
	const MIN = min;
	const MAX = max;
	const parsed = parseInt(num)
	return Math.min(Math.max(parsed, MIN), MAX)
}

function getCanvas(){
	const pixelslist = loadFile('/frontend/canvas.csv').split(',').map(Number);
	const pixels = Uint8ClampedArray.from(pixelslist);
	const imageData = new ImageData(pixels, WIDTH, HEIGHT);
	ctx.putImageData(imageData, 0, 0);

}

getCanvas();
setInterval(getCanvas,2000);



function openForm() {document.getElementById("popupForm").style.display = "block";}
function closeForm() {document.getElementById("popupForm").style.display = "none";}

function editPixel(r, g, b, username) {
	var http = new XMLHttpRequest();
	var url = '/editpixel'; // ca marche pas
	var params = {'userid':"1", 'username':'crocogab','position':[clicked_pixel.x, clicked_pixel.y], 'color':[r,g,b]};
	console.log(params);
	http.open('POST', url, true);
	http.setRequestHeader('Content-type', 'application/json');
	http.send(params);
}

function hexToRgb() {
	var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(document.getElementById("colorChoice").value);
	return result ? {
	  r: parseInt(result[1], 16),
	  g: parseInt(result[2], 16),
	  b: parseInt(result[3], 16)
	} : null;
}

	var scale = 1,
	panning = false,
	pointX = 0,
	pointY = 0,
	drag = false,
	start = { x: 0, y: 0 },
	canvasHeight = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--CANVAS-WIDTH')),
	canvasWidth = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--CANVAS-HEIGHT'));
	
	
	var zoom = document.getElementById('zoom');
	
	function setTransform() {
		zoom.style.transform = "translate(" + pointX + "px, " + (pointY - 59)  + "px) scale(" + scale + ")";
	}
	
	zoom.onmousedown = function (e) {
		e.preventDefault();
		start = { x: e.clientX - pointX, y: e.clientY - pointY };
		panning = true;
		drag = false;
	}
	
	zoom.onmouseup = function (e) {
		panning = false;
	}
	
	zoom.onmousemove = function (e) {
		e.preventDefault();
		drag = true;
		if (!panning) {
			return;
		}
		pointX = (e.clientX - start.x);
		pointY = (e.clientY - start.y);
		setTransform();
	}
	
	zoom.onwheel = function (e) {
		e.preventDefault();
		var xs = (e.clientX - pointX) / scale,
		ys = (e.clientY - pointY) / scale,
		delta = (e.wheelDelta ? e.wheelDelta : -e.deltaY);
		(delta > 0) ? (scale *= 1.2) : (scale /= 1.2);
		pointX = e.clientX - xs * scale;
		pointY = e.clientY - ys * scale;
		setTransform();
	}
	var clicked_pixel = {x:0, y:0};
	zoom.onclick = function (e) {
		e.preventDefault();
		if (!drag) {	// if click
			clicked_pixel = {x:Math.floor(100*(start.x/scale)/canvasWidth), y:Math.floor(100*(start.y/scale)/canvasHeight)}		
			console.log(`clicked pixel @ ${clicked_pixel.x}, ${clicked_pixel.y}`);

			document.getElementById("pixel-edit").innerHTML = `pixel @ ${clicked_pixel.x}, ${clicked_pixel.y}`;
			openForm()
			
			// WIP : click pour focus sur un pixel 
			
			// console.log(start)
			// console.log(e.clientX, e.clientY)
			// console.log(pointX, pointY)
			// pointX = (pointX + start.x - 400/scale);
			// pointY = (pointY + start.y - 400/scale);
			// setTransform();

		};
	}
