var hole = document.querySelectorAll(".hole");

function mouseout() {
    var i = Math.floor(Math.random() * 9);
    hole[i].lastElementChild.style.visibility = "visible";
    hole[i].firstElementChild.style.visibility = "hidden";
}

function clearboom() {
    for (var i = 0; i < hole.length; i++) {
        hole[i].firstElementChild.style.visibility = "hidden";
    }
}

setInterval(mouseout, 1000);
for (var i = 0; i < hole.length; i++) {
    hole[i].lastElementChild.onclick = function () {
        this.style.visibility = "hidden";
        this.parentElement.firstElementChild.style.visibility = "visible";
        setTimeout(clearboom, 260);
        document.querySelector(".score").innerHTML = Number(document.querySelector(".score").innerHTML) + 100;
    }
}

function knock() {
    document.querySelector("body").style.cursor = "url('img/hammerdown.ico'),auto";
    setTimeout(function () {
        document.querySelector("body").style.cursor = "url('img/hammer.ico'),auto";
    }, 300);
}