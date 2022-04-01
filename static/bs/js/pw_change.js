$(document).ready(function(){
    $('.update_btn').click(check_form)
});

function check_form(){
    check = $('[name=pw_change] [name=current_pw]').val()

}