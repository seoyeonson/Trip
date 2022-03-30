function search_hotel() {
    document.getElementById("hotel_search").style.display ='block';
    document.getElementById("vacation_search").style.display ='none';
    document.getElementById("vacation_location").style.display = 'none';
}

function search_vacation() {
    document.getElementById("hotel_search").style.display ='none';
    document.getElementById("vacation_search").style.display ='block';
    document.getElementById("hotel_location").style.display = 'none';
    document.getElementById("date_pick").style.display = 'none';
}

function search_location() {
    document.getElementById("hotel_location").style.display ='block';
    document.getElementById("date_pick").style.display ='none';
}

function hotel_lo_select() {
    document.getElementById("hotel_location").style.display ='none';
}

function search_va_location() {
    document.getElementById("vacation_location").style.display ='block';
}

function vacation_lo_select() {
    document.getElementById("vacation_location").style.display ='none';
}

function get_date() {
    document.getElementById("date_pick").style.display ='block';
    document.getElementById("hotel_location").style.display ='none';
}

function input_date() {
    start_day = document.querySelector("#start_day").value.slice(5,10);
    end_day = document.querySelector("#end_day").value.slice(5,10);
    if(start_day > end_day) {
        temp = start_day;
        start_day = end_day;
        end_day = temp;
    }

    document.getElementById("date_pick").style.display = 'none';
    
}

// $(function() {
//     $('input[name="daterange"]').daterangepicker({
//       opens: 'left'
//     }, function(start_day, end_day, label) {
//       console.log(start_day.format('MM-DD') + ' to ' + end_day.format('MM-DD'));
//     });
// });

$(document).ready(function() {
    $("#hotel_lo_select1").click(function() {
        $("#lo_text").html("서울");
    });
    $("#hotel_lo_select2").click(function() {
        $("#lo_text").html("경기");
    });
    $("#hotel_lo_select3").click(function() {
        $("#lo_text").html("인천");
    });

    $("#vacation_lo_select1").click(function() {
        $("#va_lo_text").html("서울");
    });
    $("#vacation_lo_select2").click(function() {
        $("#va_lo_text").html("경기");
    });
    $("#vacation_lo_select3").click(function() {
        $("#va_lo_text").html("인천");
    });

    $("#submit_day").click(function() {
        $("#chk_in").html(start_day);
        $("#chk_out").html(end_day);
    });
});