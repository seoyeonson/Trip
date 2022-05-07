$(document).ready(function(){
    $('.reviewstar').off().on('click', star_rating);
    $('.review_modal_open').off().on('click', function(){
        $(this).siblings('.review_modal').css('display','block')
    })
    $('.review_cancel').off().on('click', function(){
        $(this).parent().parent('.review_modal').css('display', 'none');
    });
});

function star_rating(){
    $(this).removeClass('no_star');
    $(this).prevAll().removeClass('no_star');
    $(this).nextUntil().addClass('no_star');
    var rate = 5 - ($(this).siblings('.reviewstar.no_star').length);
    $('#rate').val(rate)
    // $(this).css('color', 'var(--icon-color)');
}