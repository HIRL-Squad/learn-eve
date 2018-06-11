window.onload = prepareAnimation;
var testdata = null;
var requestIdList = [];
var tickImg = loadImage("../static/img/check_bg.png", null);
var crossImg = loadImage("../static/img/cross_bg.png", null);

function loadImage(src, onload) {
    var img = new Image();
    img.onload = onload;
    img.src = src;
    return img;
}

function prepareAnimation() {
    var testId = document.getElementById("testId").innerText;
    $.ajax({
        url: "../testdata/"+testId,
        type: 'get',
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        success: function (data) {
            populateExampleRow();
            testdata = data;
            var allDigitList = testdata.test.vas_cog_block;
            populateGrid(allDigitList);
            var count = Object.keys(allDigitList).length;
            for(var i=0;i<count; i++){
                drawDigitCell(allDigitList[i], i);
            }
        }
    });
}

function populateExampleRow(){
    var container = document.getElementById("SDMTExample");
    var count = 9;
    for (var i = 0; i < count * 2; i++) {
        var remainder = i%18;
        if(remainder < 9) {
            var vas_ques = Math.floor(i/18)*9 + remainder + 1;
            buildSymbolBlock(i, vas_ques, container);
        }
        if(remainder>=9){
            var vas_ques = Math.floor(i/18)*9 + remainder - 9 + 1;
            buildPrintDigitBlock(vas_ques, container);
        }
    }
}

function populateGrid(allDigitList) {
    var container = document.getElementById("SDMTContainer");
    var count = Object.keys(allDigitList).length;
    for (var i = 0; i < count * 2; i++) {
        var remainder = i%20;
        if(remainder < 10) {
            var j = Math.floor(i/20)*10 + remainder;
            buildSymbolBlock(j, allDigitList[j].vas_ques, container);
        }
        if(remainder>=10){
            var j = Math.floor(i/20)*10 + remainder - 10;
            buildDigitBlock(j, allDigitList[j], container);
        }
    }
}

function buildSymbolBlock(i, vas_ques, container){
    //Create div
    var div = document.createElement("DIV");
    div.setAttribute("class", "grid-item");
    div.setAttribute("height", 162);
    div.setAttribute("width", 180);
    //Create img
    var img = document.createElement("IMG");
    img.setAttribute("height", 162);
    img.setAttribute("width", 180);
    img.setAttribute("src", "../static/img/vas"+vas_ques+".png");
    div.appendChild(img);
    container.appendChild(div);
}

function buildPrintDigitBlock(vas_ques, container){
    //Create div
    var div = document.createElement("DIV");
    div.setAttribute("class", "grid-item-digit");
    div.setAttribute("height", 162);
    div.setAttribute("width", 180);
    div.innerText = vas_ques;
    var fontSize = 162;
    div.style.fontSize = fontSize + "px";
    container.appendChild(div);
}

function buildDigitBlock(i, vasCogBlock, container){
    //Create div
    var div = document.createElement("DIV");
    div.setAttribute("class", "grid-item grid-item-digit");
    //Create canvas
    var canvas = document.createElement("CANVAS");
    canvas.setAttribute("id", "canvas-"+i);
    canvas.setAttribute("class","digit-canvas")
    canvas.setAttribute("height", 162);
    canvas.setAttribute("width", 180);
    //Create overlay div
    var overlayDiv = document.createElement("DIV");
    overlayDiv.setAttribute("id", "digit-overlay-"+i);
    overlayDiv.setAttribute("class", "digit-overlay");
    var imgPlayButton = document.createElement("IMG");
    imgPlayButton.setAttribute("class", "img-play-button");
    imgPlayButton.setAttribute("src", "../static/img/playButton.png");
    imgPlayButton.setAttribute("height", 162);
    imgPlayButton.setAttribute("width", 180);
    imgPlayButton.setAttribute("onclick","playStrokes("+i+")");
    overlayDiv.appendChild(imgPlayButton);

    div.appendChild(canvas);
    div.appendChild(overlayDiv);
    container.appendChild(div);
}

function playStrokes(index){
    var allDigitList = testdata.test.vas_cog_block;
    var pathList = allDigitList[index].path_list;
    // If pathList is empty, do nothing
    if(!pathList)
        return;
    disableOverlayClasses(index);
    playAnimation(pathList, index);
}

function disableOverlayClasses(index){
    var canvas = document.getElementById("canvas-"+index);
    canvas.classList.remove("dim");
    var overlayDiv = document.getElementById("digit-overlay-"+index);
    overlayDiv.classList.remove("overlay");
}

function enableOverlayClasses(index){
    var canvas = document.getElementById("canvas-"+index);
    if(!canvas.classList.contains("dim"))
        canvas.classList.add("dim");
    var overlayDiv = document.getElementById("digit-overlay-"+index);
    if(!overlayDiv.classList.contains("overlay"))
        overlayDiv.classList.add("overlay");
}

function playAnimation(pathList, index) {
    // Stop existing animation, if any.
    if(requestIdList[index]){
        cancelAnimationFrame(requestIdList[index]);
        requestIdList[index] = null;
    }

    var canvas = document.getElementById("canvas-"+index);
    var context = createContextForDrawing(canvas);
    // Clear canvas
    context.clearRect(0,0,canvas.width, canvas.height);
    // Initialization
    var path_i = 0;
    var i = 0;
    var point_list = pathList[path_i].point_list;
    var start_point_x = point_list[i]['x'];
    var start_point_y = point_list[i]['y'];
    var first_point_time = point_list[i]['t'];

    context.beginPath();
    context.moveTo(start_point_x, start_point_y);
    var first_frame_time = performance.now();
    var lapsed = 0;
    updateToPresentTime();

    function drawPointOnLine(x, y, i){
        if(i > 0){
            context.lineTo(x,y);
            context.stroke();
        }
        else if(i===0){ // If first point in a line, move there instead of drawing.
            context.moveTo(x,y);
        }
    }

    function TryFetchNextPoint(){
        var next_i = i+1;
        var next_path_i = path_i;

        //if reached end of current stroke path already
        if(next_i>=pathList[next_path_i].point_list.length){
            next_path_i=path_i+1;
            next_i=0;
            if(!pathList[next_path_i]){
                return false;
            }
        }

        var time_since_first_point = pathList[next_path_i].point_list[next_i]["t"] - first_point_time;
        if(time_since_first_point > lapsed)
            return false;
        else
        {
            i = next_i;
            path_i = next_path_i;
            return true;
        }
    }

    function updateToPresentTime(){
        // get current time
        var current = performance.now();
        // get lapsed time since last frame
        lapsed = current - first_frame_time;

        var fetchResult;
        while(fetchResult = TryFetchNextPoint()){
            var x = pathList[path_i].point_list[i]['x'];
            var y = pathList[path_i].point_list[i]['y'];
            drawPointOnLine(x,y,i);
        }

        if(!fetchResult){// If next point cannot be fetched
            //Maybe we already reached the end of all paths.
            //then we shall stop the animation
            if(i+1>=pathList[path_i].point_list.length)
                if(path_i+1>=pathList.length)
                {
                    enableOverlayClasses(index);
                    drawTickOrCross(index);
                    return;
                }
        }
        requestIdList[index] = requestAnimationFrame(updateToPresentTime);
    }
};

function drawDigitCell(vasCogBlock, index){
    var pathList = vasCogBlock.path_list;

    // if pathList is null or undefined, do nothing
    if(!pathList)
        return;

    drawDigit(pathList, index);
    drawTickOrCross(index);
    enableOverlayClasses(index);
}

function drawDigit(pathList, index){
    var canvas = document.getElementById("canvas-"+index);
    var context = createContextForDrawing(canvas);
    context.beginPath();

    for(var i =0; i<pathList.length; i++){
        drawOnCanvasContext(pathList[i].point_list, context);
    }
}

function drawTickOrCross(index){
    var canvas = document.getElementById("canvas-"+index);
    var context = canvas.getContext("2d");
    var result = testdata.test.result[index];
    var img = result? tickImg:crossImg;
    context.drawImage(img, 0, 0, context.canvas.width, context.canvas.height);
}

function drawOnCanvasContext(point_list, context){
    if(point_list.length==0)
        return;
    var start_point_x = point_list[0]['x'];
    var start_point_y = point_list[0]['y'];
    context.moveTo(start_point_x, start_point_y);
    for (var i = 1; i < point_list.length; i++) {
        context.lineTo(point_list[i]['x'],point_list[i]['y']);
    }
    context.stroke();
}

function createContextForDrawing(canvas){
    var context = canvas.getContext("2d");
    context.lineWidth = 5;
    context.strokeStyle = "#686565";
    context.lineCap = "round";
    return context;
}