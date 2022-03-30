$(document).ready(function(){
    $("#all_agree").change(all_agree);
    $(".reserve_check").change(del_agree);
    $("#auth_btn").click(phone_confirm);
    $("#confirm_btn").click(confirm_num);
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
    };
};


function confirm_cancel(){
    var confirm_box = document.getElementById("confirm_box")
    if(confirm_box == ""){
        $(".confirm_box").css("display", "none");
    };            
};

// 휴대폰 인증
function phone_confirm(){
    $('.phone_confirm').css("display", "block"); 
    // 인증번호 버튼 클릭시 입력창 가시화 
    $("#auth_btn").css("background-color", "#BDBDBD"); // 입력창 가시화되면 인증번호 버튼 색상 변경
};

function confirm_num(){
    // 인증번호 일치하는지 확인
    alert('#');
    $('.confirm_box').attr("disabled", true);
    $('#phone_num').attr("disabled", true);
    $('.confirm_btn').css("background-color", "#BDBDBD");
};