/*
* All JS code here is referenced from: https://blog.csdn.net/z_zhy/article/details/82711151
*I make some modifications according to this context
*I promise I can answer questions if you ask some related questions
* */
let canvas = document.getElementById("background_canvas");
//get the canvas element
let ctx = canvas.getContext('2d');
//getContext("2d") 对象是内建的 HTML5 对象，拥有多种绘制路径、矩形、圆形、字符以及添加图像的方法。
resize();
window.onresize = resize;

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

let RAF = (
    function () {
        return window.requestAnimationFrame
		//告诉浏览器——你希望执行一个动画，并且要求浏览器在下次重绘之前调用指定的回调函数更新动画。
		//该方法需要传入一个回调函数作为参数，该回调函数会在浏览器下一次重绘之前执行
    })();

var warea = {x: null, y: null};
window.onmousemove = function (e) {
    //e = e || window.event;
    warea.x = e.clientX;
    warea.y = e.clientY;
};
window.onmouseout = function (e) {
    warea.x = null;
    warea.y = null;
};
// 添加粒子
// x，y为粒子坐标，xa, ya为粒子xy轴加速度，max为连线的最大距离
var dots = [];
for (var i = 0; i < 150; i++) {
    var x = Math.random() * canvas.width;
    var y = Math.random() * canvas.height;
    var xa = Math.random() * 2 - 1;
    var ya = Math.random() * 2 - 1;
    red=Math.random()*255;
    blue=Math.random()*255;
    yellow=Math.random()*255;
    dots.push({
        x: x,
        y: y,
        xa: xa,
        ya: ya,
        max: 6000,
		red:red,
		blue:blue,
		yellow:yellow,
    })
}
// 延迟100毫秒开始执行动画，如果立即执行有时位置计算会出错
setTimeout(function () {
    animate();
}, 100);

// 每一帧循环的逻辑
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // 将鼠标坐标添加进去，产生一个用于比对距离的点数组
    var ndots = [warea].concat(dots);
    dots.forEach(function (dot) {
        // 粒子位移
        dot.x += dot.xa;
        dot.y += dot.ya;
        // 遇到边界将加速度反向
        dot.xa *= (dot.x > canvas.width || dot.x < 0) ? -1 : 1;
        dot.ya *= (dot.y > canvas.height || dot.y < 0) ? -1 : 1;
        // 绘制点
		ctx.beginPath();
		red=Math.random()*255;
		blue=Math.random()*255;
		yellow=Math.random()*255;
		ctx.fillStyle = 'rgba('+dot.red+', '+dot.blue+', '+dot.yellow+',0.7)';
  		ctx.arc(dot.x, dot.y, 10, 0, Math.PI*2, false);
  		ctx.fill();
        ndots.splice(ndots.indexOf(dot), 1);
    });
    RAF(animate);
}