let lastPointX = null 
let lastPointY = null 
let canvas = null
let con = null
let canvasPos = null

let penColor = 'rgba(0, 0, 0, 255)'

window.onload = function (e) {
    console.log("[draw.js] Hello")

    canvas = $('canvas')[0]
    con = canvas.getContext('2d')

    canvas.addEventListener('touchstart', initalizeCanvas, false) 
    console.log("[draw.js] Waiting for initialization")
}

function initalizeCanvas(e)
{
    console.log("[draw.js] Canvas Initialized")
    canvas.removeEventListener('touchstart', initalizeCanvas)
    
    canvasPos = canvas.getBoundingClientRect()
    con.canvas.width = $(canvas).width()
    con.canvas.height = $(canvas).height()

    con.lineJoin = "round"
    con.lineCap = "round"
    con.strokeStyle = 'rgba(0,0,0,255)'
    con.lineWidth = 50; // these are non-static vars
    con.globalCompositeOperation="source-over";

    try{draw(e)}catch(e){console.log("[draw.js] False touch")}

    canvas.addEventListener('touchmove', draw, {passive: true}) 
    canvas.addEventListener('touchstart', draw, {passive: true}) 
    canvas.addEventListener('touchend', function(e){
        lastPointX = null
        lastPointY = null
        console.log("end")
    }, {passive: true}) 

    $('#penRed').on('input', penColorChange)
    $('#penGreen').on('input', penColorChange)
    $('#penBlue').on('input', penColorChange)
}

function draw(e)
{
    drawxy(e.changedTouches[0].pageX, e.changedTouches[0].pageY)
}

function drawxy(x, y)
{
    // var grd = con.createLinearGradient(x, y, 1, canvasPos.height);

    // grd.addColorStop(0, '#12a6eb');   

    // grd.addColorStop(1, '#ebc711');

    con.strokeStyle = penColor
    con.lineWidth = parseInt($('#penSize').val()); // these are non-static vars

    let newPointX = Math.floor(x - canvasPos.left)+0.5
    let newPointY = Math.floor(y - canvasPos.top)+0.5
    con.beginPath();
    
    if (lastPointX != null && lastPointY != null)
    {
        var deltaX = newPointX - lastPointX;
        var deltaY = newPointY - lastPointY;

        con.moveTo(lastPointX, lastPointY);
        con.lineTo(lastPointX+(deltaX/4), lastPointY+(deltaY/4));
        con.lineTo(lastPointX+(deltaX*(2/4)), lastPointY+(deltaY*(2/4)));
        con.lineTo(lastPointX+(deltaX*(3/4)), lastPointY+(deltaY*(3/4)));
    }
    else
        con.moveTo(newPointX, newPointY);

    con.lineTo(newPointX, newPointY);
    con.closePath();
    con.stroke();

    lastPointX = newPointX
    lastPointY = newPointY
}

function penColorChange(e)
{
    let newPenColor = "rgba(" + $('#penRed').val() + ","
    newPenColor+= $('#penGreen').val() + ","
    newPenColor+= $('#penBlue').val() + ", 255)"

    $('#penColorText').css('color', newPenColor)

    penColor = newPenColor
}

function toggleEraser()
{
    if (appV.eraser)
        con.globalCompositeOperation = "source-over"
    else 
        con.globalCompositeOperation = "destination-out"

    appV.eraser= !appV.eraser
}

function copyMessage()
{
    let copiedImage = new Image()
    copiedImage.src = $('#messages-container .message')[$('#messages-container').children().length - 1].children[1].src
    copiedImage.onload = function(){
        con.drawImage(copiedImage, 0, 0);
    }
}

function clearCanvas() {
    con.clearRect(0, 0, canvas.width, canvas.height)
}