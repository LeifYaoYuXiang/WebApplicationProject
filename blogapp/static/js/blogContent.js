// let div=document.getElementById('input_feedback')
$(document).ready(function(){
    let limitNum = 140;
    let inputAlready=0;
    let pattern = inputAlready+'/'+limitNum;
    $('#input_feedback').html(pattern);
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