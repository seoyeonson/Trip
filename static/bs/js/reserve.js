$(document).ready(function(){
    $("#all_agree").change(all_agree);

    $(".reserve_check").change(del_agree);
});

function all_agree(){
    if($("#all_agree").is(":checked")){
        $(".reserve_check").prop("checked", true)        
    }else{
        $(".reserve_check").prop("checked", false)        
    }
}

function del_agree(){
    var check = $(this).is(":checked")
    if(!check){
        $("#all_agree").prop("checked", false)
    }
};