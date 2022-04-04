$(document).ready(function(){
    $('.update_btn').on('click',check_form)

});

function check_form(){
    current_pw = $('input[name=current_pw]').val().trim()
    new_pw = $('input[name=new_pw]').val().trim()
    confirm_pw = $('input[name=confirm_pw]').val().trim()
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
    else if (new_pw != confirm_pw){
        $('#error_cfrm').html('비밀번호가 일치하지 않습니다')
        return false;
    }
    alert('비밀번호가 변경되었습니다.');
    return true;
}