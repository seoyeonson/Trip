$(document).ready(function(){
    var today = new Date();

    // main vacation date
    var startDate = $('input[name=vacation_date]').val();
    var today = new Date();
    var minDate = today.getFullYear() + '-' + ("0" + (1 + today.getMonth())).slice(-2) + '-' + ("0" + today.getDate()).slice(-2);
    if(startDate == 0){
        startDate = minDate;
    }

    $(function() {
        console.log("main.js 실행")
        $('input[name="va_daterange"]').daterangepicker({
            "singleDatePicker": true,
            "startDate" : startDate,
            "minDate" : minDate,
            opens: 'center',
            locale: {
                "applyLabel": "Apply",
                "cancelLabel": "Cancel",
                "format": 'YYYY-MM-DD',
                "daysOfWeek": ["일", "월", "화", "수", "목", "금", "토"], 
                "monthNames": ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
            },

        }, 
        function(start, end, label) {
            startDate = start.format('YYYY-MM-DD');
            console.log(startDate);
        });
    });

    $('[name="va_date_choice"]').click(function(e) {
        console.log("js.js 실행")
        $('.vacation_date_pick').css('display', 'none');
        $('#vacation_date').html(startDate);
        $('input[name=vacation_date]').attr('value', startDate);
    });
});