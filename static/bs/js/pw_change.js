$(document).ready(function(){
    $('.update_btn').off().on('click',check_form);
});

function check_form(){
    var current_pw = $('input[name=current_pw]').val().trim()
    var new_pw = $('input[name=new_pw]').val().trim()
    var confirm_pw = $('input[name=confirm_pw]').val().trim()
    var pwPat = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;
    if(current_pw == ""){
        $('input[name=current_pw]').focus();
        return false;
    }
    else if(new_pw == ""){
        $('input[name=new_pw]').focus();
        return false;
    }
    else if(confirm_pw == ""){
        $('input[name=confirm_pw]').focus();
        return false;
    }
    else if(!pwPat.test(new_pw)){
        $('#error_new').html("8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.")
        return false;
    }
    else if (new_pw != confirm_pw){
        $('#error_cfrm').html('비밀번호가 일치하지 않습니다')
        return false;
    }
    
    return true;
}