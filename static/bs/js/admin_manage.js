$(document).ready(function(){
    $('#date').off().on("input",block_word);
    $('#date').off().on("change",fix_date);
    // $('.search_btn').on("click", show_reserve);
    $('.choice').off().on("click", choice_place);
    $('#del_reserve').off().on("click", function(){
        r = confirm('해당 예약 건을 삭제하시겠습니까?')
        if (r){
            $('#del_reserve')
        }
    })
    
});

function block_word(){
    $('#date').val($('#date').val().replace(/[^0-9|-]/, ''))
}

function fix_date(){
    var newDate = $('#date').val().replace(/[^0-9]/g, "").replace(/(\d{4})(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])/, "$1-$2-$3");
    $('#date').val(newDate);
}

function choice_place(){    
    choice = $(this).val().trim()
    if (choice=='vacation'){
        $('.cv').addClass('clicked_btn')
        $('.ch').removeClass('clicked_btn')
        $('#choice_vacation').css("display", "block");
        $('#choice_hotel').css("display", "none");
        $('#choice').val(choice)
    }else{
        $('#choice_vacation').css("display", "none");
    }
    
    if (choice=='hotel'){
        $('.cv').removeClass('clicked_btn')
        $('.ch').addClass('clicked_btn')
        $('#choice_hotel').css("display", "block");
        $('#choice_vacation').css("display", "none");
        $('#choice').val(choice)
    }else{
        $('#choice_hotel').css("display", "none");
    }
}

// function show_reserve(){
//     $("")
// }