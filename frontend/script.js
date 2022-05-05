const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

const WIDTH = 100;
const HEIGHT = 100;
console.log(`WIDTH = ${WIDTH}\nHEIGHT = ${HEIGHT}`);

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

const pixelslist = loadFile('/frontend/canvas.csv').split(',').map(Number);

const pixels = Uint8ClampedArray.from(pixelslist);

const imageData = new ImageData(pixels, WIDTH, HEIGHT);

ctx.putImageData(imageData, 0, 0);


window.onload = function(){ 
	var scale = 1,
	panning = false,
	pointX = 0,
	pointY = 0,
	drag = false,
	start = { x: 0, y: 0 };
	
	
	var zoom = document.getElementById('zoom');
	
	function setTransform() {
		zoom.style.transform = "translate(" + pointX + "px, " + pointY + "px) scale(" + scale + ")";
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
	
	zoom.onclick = function (e) {
		e.preventDefault();
		if (!drag) {
			console.log('clicked');
			console.log(e.clientX, e.clientY);
			console.log(pointX, pointY);
			console.log(start);
			
			
			// pointX = (e.clientX - pointX);
			// pointY = (e.clientY - pointY);
			// setTransform();
			
			
		};
	}
};

