$(document).ready(function(){
    var startDate = $('input[name=start_date]');
    var endDate = $('input[name=end_date]');
    var today = new Date();
    var minDate = today.getFullYear() + '-' + ("0" + (1 + today.getMonth())).slice(-2) + '-' + ("0" + today.getDate()).slice(-2);
    if(startDate == 0 && endDate == 0){
        startDate = minDate;
        endDate = minDate;
    } 
    
    $(function() {
        console.log(startDate, endDate, minDate);
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
            }
        }, 
        function(start, end, label) {
            // console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
            startDate = start.format('YYYY-MM-DD');
            endDate = end.format('YYYY-MM-DD');
        });
    });

    $('.chk_va_form').click(function(){
        var SIGUN_NM = $('input[id=va_lo_text]').val();

        if(SIGUN_NM == ''){
            alert('위치를 선택해주세요.');
            return false;
        }
        return true;
    });

    $('.chk_ho_form').click(function(){
        var SIGUN_NM = $('input[name=SIGUN_NM]').val();
        var start_date = $('input[name=start_date]').val();

        if(SIGUN_NM == ''){
            alert('위치를 선택해주세요.');
            return false;
        }
        if(start_date == ''){
            alert('체크인・체크아웃 날짜를 선택해주세요.');
            return false;
        }
    });

    $('[name="date_choice"]').click(function(e) {
        $('.date_pick').css('display', 'none');
        $('#chk_in').html(startDate);
        $('#chk_out').html(endDate);
        $('input[name=start_date]').attr('value', startDate);
        $('input[name=end_date]').attr('value', endDate);
        console.log("startDate", startDate, "endDate", endDate);
    });
});