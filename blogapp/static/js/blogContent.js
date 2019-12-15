// let div=document.getElementById('input_feedback')
$(document).ready(function(){
    let limitNum = 140;
    let inputAlready=0;
    let pattern = inputAlready+'/'+limitNum;
    $('#input_feedback').html(pattern);
    /*
    keydown - 键按下的过程
    keypress - 键被按下
    keyup - 键被松开
   当键盘键被松开时发生 keyup 事件
    * */
    $('#comment').keyup(
    function(){
        let inputAlready = $(this).val().length;
        if(inputAlready > limitNum){
                pattern = "Out Of the Limit!";
            }else{
                pattern = inputAlready+'/'+limitNum;
            }
            $('#input_feedback').html(pattern);
        }
    );
});