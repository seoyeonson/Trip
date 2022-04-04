$(document).ready(function(){
    $("#all_agree").change(all_agree);
    $(".reserve_check").change(del_agree);
    $("#auth_btn").click(phone_confirm);
    $("#confirm_btn").off().on("click",confirm_num);
    $("#purchase_btn").off().on("click",purchase);
    $("#")
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
    alert('야');
    phone_num = $('#phone_num').val().trim();
    phone_pat = /^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$/;

    if(phone_num==""){
        $('#phone_num').focus();
        return false;
    }
    if(!phone_pat.test(phone_num)){
        $('#error_phone').html('전화번호 형식에 맞게 입력해주세요');
        return false;
    }else{
        $('#error_phone').html("");
    }
    var phone_new = phone_num.replace(/[^0-9]/g, "").replace(/([0|1|6|7|8|9]?)([0-9]{3,4})([0-9]{4})$/, "$1-$2-$3");
    $('#phone_num').val(phone_new);
    $('.phone_confirm').css("display", "block"); 
};

function confirm_num(){
    auth_num = $('#confirm_box').val().trim()
    if(auth_num==""){
        $('#confirm_box').focus();
        return false;
    };
    // 인증번호 일치하는지 확인
    $('#confirmOk').html('Ok');
    $('.confirm_box').attr("readonly", true);
    $('#phone_num').attr("readonly", true);
    $("#auth_btn").css("background-color", "#BDBDBD");
    $('.confirm_btn').css("background-color", "#BDBDBD");
    
    (()=>{alert('휴대폰 인증 완료')})();
};

function purchase(){
    var reserve_name = $('#reserve_name').val().trim()
    // var check = $(".reserve_check").is(":checked")
    // phone_num = $('#phone_num').val().trim();
    if(reserve_name==""){
        $('#reserve_name').focus();
        return false;
    }else if($('#phone_num').val().trim()==""){
        $('#phone_num').focus();
        return false;
    }else if($("#confirmOk").html()==""){
            (() => {alert('휴대폰 인증을 완료해주세요')})();
            return false;
    }else if($(".reserve_check:checked").length != $(".reserve_check").length){
            (() => {alert('약관에 모두 동의하세요')})();
            return false;
    };
    $('.reserve').submit();
    return true;
};

function coolSMS(){

}