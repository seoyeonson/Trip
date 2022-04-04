$(document).ready(function(){
    $('#let_phone_update').click(update_info);
    $('#let_email_update').click(update_info);
    $('.cancel_btn').click(end_update);
    $('.ok_btn').click(end_update);
})

function update_info(){
    $(this).css('display', 'none');
    if(this.id=="let_phone_update"){
        $('.box_phNm').css('display', 'block');
        $('input[name=user_phonNum]').attr('disabled',false);
    }
    else if(this.id=="let_email_update"){
        $('.box_email').css('display','block');
        $('input[name=user_email]').attr('disabled',false);
    }
}

function phNm_close(){
    $('input[name="user_phonNum"]').value = null
    $('.box_phNm').css('display', 'none');
    $('#let_phone_update').css('display','block');
    $('input[name=user_phonNum]').attr('disabled',true);
}
function email_close(){
    $('input[name="user_email"]').value = null
    $('.box_email').css('display','none');
    $('#let_email_update').css('display','block');
    $('input[name=user_email]').attr('disabled',true);
}

function end_update(){

    if(this.id=='cancel_phNm'){
        phNm_close();
    }
    else if(this.id=='email_updateOk'){
        email = $('input[name="user_email"]').val().trim()
        email_pat = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
        if (email==""){
            $('#error_email').html("이메일을 입력하세요")
            return false;
        }else if(!email_pat.test(email)){
            $('#error_email').html("이메일 형식에 맞게 입력해주세요")
            return false;
        };
        return true;
    }
    else if(this.id=='cancel_email'){
        email_close();
    }
    else if(this.id=='phNm_updateOk'){
        phNm = $('input[name="user_phonNum"]').val().trim()
        phNm_pat = /^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$/;
        if (phNm==""){
            $('#error_phNm').html("전화번호를 입력하세요")
            return false;
        }else if(!phNm_pat.test(phNm)){
            $('#error_phNm').html("전화번호 형식에 맞게 입력해주세요")
            return false;
        };
        return true;
    };
};

function check(){
    email = $('input[name="user_email"]').val().trim()
    phNm = $('input[name="user_phonNum"]').val().trim()
    email_pat = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
    phNm_pat = /^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$/;
    if (email==""){
        $('#error_email').html("이메일을 입력하세요")
        $('input[name="user_email"]').value = null
        return false;
    }else if(!email_pat.test(email)){
        $('#error_email').html("이메일 형식에 맞게 입력해주세요")
        return false;
    }
    end_update();
};