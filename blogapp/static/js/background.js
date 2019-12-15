/*
* All JS code here is referenced from: https://blog.csdn.net/z_zhy/article/details/82711151
*I make some modifications according to this context
*I promise I can answer questions if you ask some related questions
* */
let canvas = document.getElementById("background_canvas");
//get the canvas element
let ctx = canvas.getContext('2d');
//getContext("2d") 对象是内建的 HTML5 对象，拥有多种绘制路径、矩形、圆形、字符以及添加图像的方法。
//可以看作是获取了画板的画笔
resize();
window.onresize = resize;
//这里是执行了resize函数，并且将resize函数赋给了window对象的内部方法
/*
* 为什么要赋给window对象这个函数？
*   onresize可以看作是一种事件监听器，该事件会在窗口或框架被调整大小时发生
*   如果没有这句话，那么我缩放浏览器的展示框的时候，canvas的大小不会随之变化
* */
function resize() {
    //获得的是可视区域的宽高：
    // window.innerWidth宽度包含了纵向滚动条的宽度，
    // window.innerHeight高度包含了横向滚动条的高度
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
//第一种方法：
// let RAF=function(){
//     return window.requestAnimationFrame
// }();
// console.log(RAF)

//第二种方法：
// let RAF = (
//     function () {
//         return window.requestAnimationFrame
// 		//告诉浏览器——你希望执行一个动画，并且要求浏览器在下次重绘之前调用指定的回调函数更新动画。
// 		//该方法需要传入一个回调函数作为参数，该回调函数会在浏览器下一次重绘之前执行
//     })();

//以上两种写法都可以，在上交的作业中，我们采用了第二种
//其实本质上来说都是返回了window对象中的requestAnimationFrame方法

var warea = {x: null, y: null};
//设置一系列的监听事件
//onmousemove 事件会在鼠标指针移动时发生，并调用该方法
window.onmousemove = function (e) {
    //clientX/Y获取到的是触发点相对浏览器可视区域左上角距离，不随页面滚动而改变。
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
    //Math.random()会返回给一个0-1之间的随机数
    var x = Math.random() * canvas.width;//圆心位置 x坐标
    var y = Math.random() * canvas.height;//圆心位置 y坐标
    var xa = Math.random() * 2 - 1;//x方向的速度
    var ya = Math.random() * 2 - 1;//y方向的速度
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
//以上的for循环只是生成了一个最初的状态的点集合

//setTimeout()方法设置一个定时器，该定时器在定时器到期后执行一个函数或指定的一段代码
//延迟100毫秒开始执行动画，如果立即执行有时位置计算会出错
//这个函数只执行了一次
setTimeout(function () {
    animate();
}, 100);

// 每一帧循环的逻辑
function animate() {
    //clearRect()可以用来在给定矩形内清空一个矩形
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    //将鼠标坐标添加进去，产生一个用于比对距离的点数组
    //concat()方法：合并两个或多个数组。此方法不会更改现有数组，而是返回一个新数组
    //var ndots = [warea].concat(dots);
    //可以直接删除，这是我在design的时候改主意了，不用理会之前的代码

    dots.forEach(function (dot) {
        // 粒子位移
        dot.x += dot.xa;
        dot.y += dot.ya;
        // 遇到边界将速度反向
        dot.xa *= (dot.x > canvas.width || dot.x < 0) ? -1 : 1;
        dot.ya *= (dot.y > canvas.height || dot.y < 0) ? -1 : 1;
        // 绘制点
		ctx.beginPath();
		ctx.fillStyle = 'rgba('+dot.red+', '+dot.blue+', '+dot.yellow+',0.7)';
  		ctx.arc(dot.x, dot.y, 10, 0, Math.PI*2, false);
  		ctx.fill();
        //ndots.splice(ndots.indexOf(dot), 1);
    });
    window.requestAnimationFrame(animate)//递归调用：recursive invocation
}
//如果将这个函数放在外面（比如放在下面），那么就会导致页面处于静止状态
// window.requestAnimationFrame(animate);
/*
* 关于： window.requestAnimationFrame(animate)
* 系统每次绘制之前会主动调用 rAF 中的回调函数，
* 如果系统绘制率是 60Hz，那么回调函数就每16.7ms 被执行一次，
* 如果绘制频率是75Hz，那么这个间隔时间就变成了 1000/75=13.3ms。
* 换句话说就是，rAF 的执行步伐跟着系统的绘制频率走。
* 它能保证回调函数在屏幕每一次的绘制间隔中只被执行一次。
* */