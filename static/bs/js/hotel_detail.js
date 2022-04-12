$(document).ready(function(){
    console.log(test)
    var startDate = $('input[name=start_date]').val();
    var endDate = $('input[name=end_date]').val();
    var today = new Date();
    var minDate = today.getFullYear() + '-' + ("0" + (1 + today.getMonth())).slice(-2) + '-' + ("0" + today.getDate()).slice(-2);
    if(startDate == 0 && endDate == 0){
        startDate = minDate;
        endDate = minDate;
    } 

    var a = moment("2022-04-22");
    var b = moment("2022-04-23");
    var x = moment("2022-04-25");
    var y = moment("2022-05-02");

    $(function() {
        $('input[name="daterange"]').daterangepicker({
            "startDate": startDate,
            "endDate": endDate,
            "minDate" : minDate,
            opens: 'center',
            locale: {
                "applyLabel": "Apply",
                "cancelLabel": "Cancel",
                "format": 'YYYY-MM-DD',
                "daysOfWeek": ["일", "월", "화", "수", "목", "금", "토"], 
                "monthNames": ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
            },
            isInvalidDate: function (date) {
                    if (date >= a && date <= b) {
                        return true;
                    }
                    if(date >= x && date <= y) {
                        return true;
                    }
                    return false;
                }
        }, 
        function(start, end, label) {
            // console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
            startDate = start.format('YYYY-MM-DD');
            endDate = end.format('YYYY-MM-DD');
        });
    });

    $('[name="reserve_date_choice"]').click(function(e) {
        $('.date_pick').css('display', 'none');
        $('.hotel_detail_reserve_checkin').html('<i class="fas fa-calendar-alt"></i><span class="icon_before">'+startDate);
        $('.hotel_detail_reserve_checkout').html(endDate);
        $('input[name=start_date]').attr('value', startDate);
        $('input[name=end_date]').attr('value', endDate);
        console.log("startDate", startDate, "endDate", endDate);
    });

    $('button[type=submit]').click(function(){
        var room_type = $('input[name=reserve_room]').val();
        
        if(room_type == ''){
            alert('방을 선택해주세요.');
            return false;
        }
        return true;
    });
})

function choice_room() {
    $('.date_pick').css('display', 'none');
    $('.hotel_room_select').css('display', 'block');
    $('.hotel_reserve_people').css('display', 'none');
}

function hotel_room_select(text){
    $('.hotel_room_select').css('display', 'none');
    value = $(text).text();
    value_room_pk = $('.hotel_room_select').val();
    $(".room").html(value);
    $('input[name=reserve_room]').attr('value', value);
    $('input[name=hotel_room_pk]').attr('value', value_room_pk);
}