window.onload = prepareAnimation;
var testdata = null;
var requestIdList = [];

function prepareAnimation() {
    var testId = document.getElementById("testId").innerText;
    $.ajax({
        url: "../testdata/"+testId,
        type: 'get',
        headers: {
            Accept: "application/json; charset=utf-8"
        },
        success: function (data) {
            testdata = data;
            var allDigitList = testdata.test.vas_cog_block;
            populateGrid(allDigitList);
            var count = Object.keys(allDigitList).length;
            for(var i=0;i<count; i++){
                drawDigit(allDigitList[i], i);
            }
        }
    });
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
    //Create img
    var img = document.createElement("IMG");
    img.setAttribute("height", 162);
    img.setAttribute("width", 180);
    img.setAttribute("src", "../static/img/vas"+vas_ques+".png");
    div.appendChild(img);
    container.appendChild(div);
}

function buildDigitBlock(i, vasCogBlock, container){
    //Create div
    var div = document.createElement("DIV");
    div.setAttribute("class", "grid-item grid-item-digit");
    //Create canvas
    var canvas = document.createElement("CANVAS");
    canvas.setAttribute("id", "canvas-"+i);
    canvas.setAttribute("height", 162);
    canvas.setAttribute("weight", 180);
    canvas.setAttribute("onclick","playStrokes("+i+")");
    div.appendChild(canvas);
    container.appendChild(div);
}

function playStrokes(index){
    var allDigitList = testdata.test.vas_cog_block;
    playAnimation(allDigitList[index].path_list, index);
}

function playAnimation(pathList, index) {
    // If pathList is empty, do nothing
    if(!pathList)
        return;
    // Stop existing animation, if any.
    if(requestIdList[index]){
        cancelAnimationFrame(requestIdList[index]);
        requestIdList[index] = null;
    }

    var canvas = document.getElementById("canvas-"+index),
        context = canvas.getContext("2d");
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
    context.lineWidth = 5;
    context.lineCap="round";
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

        var fetchResult = true;
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
                    return;
        }
        requestIdList[index] = requestAnimationFrame(updateToPresentTime);
    }
};

function drawDigit(vasCogBlock, index){
    var canvas = document.getElementById("canvas-"+index);
    var context = canvas.getContext("2d");
    context.beginPath();
    context.lineWidth = 5;
    context.lineCap="round";
    var pathList = vasCogBlock.path_list;

    // if pathList is null or undefined, do nothing
    if(!pathList)
        return;

    var vasQues = vasCogBlock.vas_ques;
    for(var i =0; i<pathList.length; i++){
        drawOnCanvasContext(pathList[i].point_list, context);
    }
    // TODO draw tick
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
