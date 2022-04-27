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



const pixelslist = loadFile('canvas.csv').split(',').map(Number);

const pixels = Uint8ClampedArray.from(pixelslist);

const imageData = new ImageData(pixels, WIDTH, HEIGHT);

ctx.putImageData(imageData, 0, 0);

// zoomer
const scale = document.getElementById('scale');
window.addEventListener('scroll', function(){
  scale.style.transform = `scale(${scrollY/100 + 1})`;
});

// bouger


var mousePosition;
var offset = [0,0];
var isDown = false;
var drag = false;

const position = document.getElementById('position');
position.addEventListener('mousedown', function(e) {
  drag = false;
  console.log('mousedown');

  isDown = true;
  offset = [
      position.offsetLeft - e.clientX,
      position.offsetTop - e.clientY
  ];

}, true);


document.addEventListener('mouseup', function(event) {

  if (!drag) {
    mousePosition = {
  
      x : event.clientX,
      y : event.clientY

    };
    console.log(`click ${mousePosition.x + offset[0]} ${mousePosition.y + offset[1]}`);
  };

  console.log('mouseup');

  isDown = false;
}, true);



document.addEventListener('mousemove', function(event) {
  event.preventDefault();
  drag = true;
  if (isDown) {
      mousePosition = {
  
          x : event.clientX,
          y : event.clientY
  
      };

      position.style.left = (mousePosition.x + offset[0]) + 'px';
      position.style.top = (mousePosition.y + offset[1]) + 'px';
  }
}, true);