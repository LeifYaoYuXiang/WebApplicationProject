$(document).ready(function () {
    let logout=document.getElementById('logout');
    console.log(logout.innerHTML)
    logout.onclick=function () {
        $.get('/logout')
    };
});