var mapProp;

// main 호텔 검색
function search_hotel() {
    document.getElementById("hotel_search").style.display ='block';
    document.getElementById("vacation_search").style.display ='none';
    document.getElementById("vacation_location").style.display = 'none';
}
// main 여행지 검색
function search_vacation() {
    document.getElementById("hotel_search").style.display ='none';
    document.getElementById("vacation_search").style.display ='block';
    document.getElementById("hotel_location").style.display = 'none';
    document.getElementById("date_pick").style.display = 'none';
}

//
function search_location() {
    document.getElementById("hotel_location").style.display ='block';
    document.getElementById("date_pick").style.display ='none';
}

function choice_people() {
    $('.date_pick').css('display', 'none');
    $('.hotel_reserve_people').css('display', 'block');
    $('.hotel_room_select').css('display', 'none');
    $('.hotel_reserve_people').toggleClass('');
}

function choice_room() {
    $('.date_pick').css('display', 'none');
    $('.hotel_room_select').css('display', 'block');
    $('.hotel_reserve_people').css('display', 'none');
}

function hotel_room_select(text){
    $('.hotel_room_select').css('display', 'none');
    value = $(text).text();
    $(".room").html(value);
    $('input[name=reserve_room]').attr('value', value);
}

function hotel_lo_select(text){
    $('.hotel_location').css('display', 'none');
    value = $(text).text();
    $('#lo_text').html(value);
}

function choice_date(){
    $('.date_pick').css('display', 'block');
    $('.hotel_reserve_people').css('display', 'none');
    $('.hotel_room_select').css('display', 'none');
}

function vacation_choice_people(){
    $('.vacation_reserve_people').css('display', 'block');
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


$(document).ready(function() {
    // 회원가입 pattern
    var emailPat = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
    var phonePat = /^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$/;
    var idPat = /[a-zA-Z0-9_-]{5,20}/;
    var pwPat = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;

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

    // 로그인 체크
    $('#logInCheck').click(function(){
        console.log("들어옴");
        var id = $('[name="id"]').val().trim();
        var pw = $('[name="pw"]').val().trim();
        
        // 아이디 체크
        if(id == ""){
            $('[name="id"]').focus();
            return false;
        }
        // 비밀번호 체크
        if(pw == ""){
            $('[name="pw"]').focus();
            return false;
        } 
        return true;
    });

    // 회원가입 체크
    $('#joinCheck').click(function(){
        var id = $('[name="id"]').val().trim();
        var pw = $('[name="pw"]').val().trim();
        var pwCheck = $('[name="pwCheck"]').val().trim();
        var memberNm = $('[name="memberNm"]').val().trim();
        var phonenum = $('[name="phonenum"]').val().trim();
        var email = $('[name="email"]').val().trim();
        
        // 이름 체크
        if(memberNm == ""){
            $("#errorMsgNm").html("이름을 입력하세요.");
            $('[name="memberNm"]').focus();
            return false;
        }else{
            $("#errorMsgNm").html("");
        }

        // 아이디 체크
        if(id == ""){
            $("#errorMsgId").html("아이디를 입력하세요.");
            $('[name="id"]').focus();
            return false;
        }else if(!idPat.test(id)){
            $("#errorMsgId").html("5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.");
            $('[name="id"]').focus();
            return false;
        }else{
            $("#errorMsgId").html("");
        }

        // 비밀번호 체크
        if(pw == ""){
            $("#errorMsgPw").html("비밀번호를 입력하세요.");
            $('[name="pw"]').focus();
            return false;
        }else if(!pwPat.test(pw)){
            $("#errorMsgPw").html("8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.");
            $('[name="pw"]').focus();
            return false;
        }else{
            $("#errorMsgPw").html("");
        }

        // 비밀번호 재확인
        if(pwCheck == ""){
            $("#errorMsgPwCheck").html("비밀번호를 확인해주세요.");
            $('[name="pwCheck"]').focus();
            return false;
        }else if(pw != pwCheck){
            $("#errorMsgPwCheck").html("입력하신 비밀번호와 맞지 않습니다.");
            $('[name="pwCheck"]').focus();
            return false;
        }else{
            $("#errorMsgPwCheck").html("");
        }
        
        // 전화번호 체크
        if(phonenum == ""){
            $("#errorMsgPhonenum").html("전화번호를 입력하세요.");
            $('[name="phonenum"]').focus();
            return false;
        }else if(!phonePat.test(phonenum)){
            $("#errorMsgPhonenum").html("전화번호 형식에 맞게 입력해주세요.");
            $('[name="phonenum"]').focus();
            return false;
        }else{
            $("#errorMsgPhonenum").html("");
        }

        // 이메일체크
        if(email == ""){
            $("#errorMsgEmail").html("이메일을 입력하세요.");
            $('[name="email"]').focus();
            return false;
        }else if(!emailPat.test(email)){
            $("#errorMsgEmail").html("이메일 형식에 맞게 입력해주세요.");
            $('[name="email"]').focus();
            return false;
        }else{
            $("#errorMsgEmail").html("");
        }

        alert("가입을 완료했습니다!");
        return true;
    });

    // detail_reserve_people button
    $('[data-quantity="plus"]').click(function(e){
        e.preventDefault();
        // Get the field name
        fieldName = $(this).attr('data-field');
        // Get its current value
        var currentVal = parseInt($('input[name='+fieldName+']').val());
        // If is not undefined
        if (!isNaN(currentVal)) {
            // Increment
            $('input[name='+fieldName+']').val(currentVal + 1);
            $('.people').html(currentVal + 1 + '명');
        } else {
            // Otherwise put a 0 there
            $('input[name='+fieldName+']').val(1);
        }
    });
    // This button will decrement the value till 0
    $('[data-quantity="minus"]').click(function(e) {
        let date;
        // Stop acting like a button
        e.preventDefault();
        // Get the field name
        fieldName = $(this).attr('data-field');
        // Get its current value
        var currentVal = parseInt($('input[name='+fieldName+']').val());
        // If it isn't undefined or its greater than 0
        if (!isNaN(currentVal) && currentVal > 1) {
            // Decrement one
            data = $('input[name='+fieldName+']').val(currentVal - 1);
            $('.people').html(currentVal - 1 + '명');
        } else {
            // Otherwise put a 0 there
            data = $('input[name='+fieldName+']').val(1);
        }

        // $.ajax({
        //     type:'POST',
        //     url:'/option_change/',
        //     data: {
        //         'hotel_reserve_people' : data,
        //     },
        //     success:function(json){
        //         console.log("data pass success",json);
        //     },
        //     error : function(xhr,errmsg,err) {
        //     console.log(xhr.status + ": " + xhr.responseText); 
        //     }
        // });
    });

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

    $('[name="reserve_date_choice"]').click(function(e) {
        $('.date_pick').css('display', 'none');
        $('.hotel_detail_reserve_checkin').html('<i class="fas fa-calendar-alt"></i><span class="icon_before">'+startDate);
        $('.hotel_detail_reserve_checkout').html(endDate);
        $('input[name=start_date]').attr('value', startDate);
        $('input[name=end_date]').attr('value', endDate);
        console.log("startDate", startDate, "endDate", endDate);
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


// 구글맵
function myMap() {
    var lat = Number($('[name="lat"]').val());
    var lng = Number($('[name="lng"]').val());
    var myLatlng = new google.maps.LatLng(lat, lng);
    var mapProp = {
        center: myLatlng,
        zoom: 17,
    };

    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    var myPos = {lat: lat, lng: lng};
	var marker = new google.maps.Marker({position: myPos});
    marker.setMap(map);
}

