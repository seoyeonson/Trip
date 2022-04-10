$(document).ready(function(){
    if (document.getElementsByName("lat")[0].value == 0 && document.getElementsByName("lng")[0].value == 0){
        document.getElementById("map_none").style.display = 'block';
        document.getElementById("googleMap").style.display = 'none';
    }
    else{
        document.getElementById("map_none").style.display = 'none';
        document.getElementById("googleMap").style.display = 'block';
    }

    var startDate = $('input[name=start_date]').val();
    var endDate = $('input[name=end_date]').val();
    var today = new Date();
    var minDate = today.getFullYear() + '-' + ("0" + (1 + today.getMonth())).slice(-2) + '-' + ("0" + today.getDate()).slice(-2);
    if(startDate == 0 && endDate == 0){
        startDate = minDate;
        endDate = minDate;
    }
    
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
            }
        }, 
        function(start, end, label) {
            // console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
            startDate = start.format('YYYY-MM-DD');
            endDate = end.format('YYYY-MM-DD');
        });
    });

    $('[name="date_choice"]').click(function(e) {
        $('.date_pick').css('display', 'none');
        $('#chk_in').html(startDate);
        $('#chk_out').html(endDate);
        $('input[name=start_date]').attr('value', startDate);
        $('input[name=end_date]').attr('value', endDate);
    });

    $('.chk_form').click(function(){
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
});
// $(document).ready(function(){
//     if ()
// });
marker=undefined;
function search_choice(e){
    if (marker){
        marker.setMap(null)
    }    

    
    // var xxx = e.getElementById('aa');
    // var ch_lat = e.getElementsByName("li_lat")[0].value
    // var ch_lng = e.getElementsByName("li_lng")[0].value
    var ch_lat = Number(e.children[0].value);
    var ch_lng = Number(e.children[1].value);
    document.getElementsByName("lat")[0].value = ch_lat 
    document.getElementsByName("lng")[0].value = ch_lng 

    if (document.getElementsByName("lat")[0].value == 0 && document.getElementsByName("lng")[0].value == 0){
        document.getElementById("map_none").style.display = 'block';
        document.getElementById("googleMap").style.display = 'none';
    }
    else{
        document.getElementById("map_none").style.display = 'none';
        document.getElementById("googleMap").style.display = 'block';
    }
    
    // return  document.getElementsByName("lat").value,  document.getElementsByName("lat").value;
    
    map.setCenter({lat: ch_lat, lng: ch_lng});
    myPos = {lat: ch_lat, lng: ch_lng};
	marker = new google.maps.Marker({position: myPos});
    
    marker.setMap(map);
}



