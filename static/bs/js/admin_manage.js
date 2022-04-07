$(document).ready(function(){
    $('#date').on("input",block_word);
    $('#date').on("change",fix_date);
    // $('.search_btn').on("click", show_reserve);

    
});

function block_word(){
    $('#date').val($('#date').val().replace(/[^0-9|-]/, ''))
}

function fix_date(){
    var newDate = $('#date').val().replace(/[^0-9]/g, "").replace(/(\d{4})(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])/, "$1-$2-$3");
    $('#date').val(newDate);
}

// function show_reserve(){
//     $("")
// }