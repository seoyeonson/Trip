var mapProp;

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
function list_choice(){
    var ch_lat = document.getElementsByName("li_lat").value
    var ch_lng = document.getElementsByName("li_lng").value
    document.getElementsByName("lat").value = ch_lat 
    document.getElementsByName("lng").value = ch_lng 

    return  document.getElementsByName("lat").value,  document.getElementsByName("lat").value
}
function list_first_page(){
    document.getElementById("table_list_1").style.display = 'block';
    document.getElementById("table_list_2").style.display = 'none';
    document.getElementById("table_list_3").style.display = 'none';
    document.getElementById("table_list_4").style.display = 'none';
    document.getElementById("table_list_5").style.display = 'none';
} 
function list_second_page(){
    document.getElementById("table_list_1").style.display = 'none';    
    document.getElementById("table_list_2").style.display = 'block';
    document.getElementById("table_list_3").style.display = 'none';
    document.getElementById("table_list_4").style.display = 'none';
    document.getElementById("table_list_5").style.display = 'none';
} 
function list_third_page(){
    document.getElementById("table_list_1").style.display = 'none';    
    document.getElementById("table_list_2").style.display = 'none';
    document.getElementById("table_list_3").style.display = 'block';
    document.getElementById("table_list_4").style.display = 'none';
    document.getElementById("table_list_5").style.display = 'none';
} 
function list_fourth_page(){
    document.getElementById("table_list_1").style.display = 'none';    
    document.getElementById("table_list_2").style.display = 'none';
    document.getElementById("table_list_3").style.display = 'none';
    document.getElementById("table_list_4").style.display = 'block';
    document.getElementById("table_list_5").style.display = 'none';
} 
function list_fiveth_page(){
    document.getElementById("table_list_1").style.display = 'none';    
    document.getElementById("table_list_2").style.display = 'none';
    document.getElementById("table_list_3").style.display = 'none';
    document.getElementById("table_list_4").style.display = 'none';
    document.getElementById("table_list_5").style.display = 'block';
} 
function list_before_page(){
    if (document.getElementById("table_list_2").style.display == 'block') {
        document.getElementById("table_list_1").style.display = 'block';    
        document.getElementById("table_list_2").style.display = 'none' ;   
  
    }
    else if(document.getElementById("table_list_3").style.display == 'block') {
        document.getElementById("table_list_2").style.display = 'block' ;   
        document.getElementById("table_list_3").style.display = 'none' ;   
    }
    else if(document.getElementById("table_list_4").style.display == 'block') {
        document.getElementById("table_list_3").style.display = 'block' ;   
        document.getElementById("table_list_4").style.display = 'none' ;     
    }
    else if(document.getElementById("table_list_5").style.display == 'block') {  
        document.getElementById("table_list_4").style.display = 'block' ;   
        document.getElementById("table_list_5").style.display = 'none' ;   
    }
} 
function list_next_page(){
    if (document.getElementById("table_list_1").style.display == 'block') {
        document.getElementById("table_list_1").style.display = 'none' ;   
        document.getElementById("table_list_2").style.display = 'block' ;   
    }
    else if(document.getElementById("table_list_2").style.display == 'block') {  
        document.getElementById("table_list_3").style.display = 'block' ;   
        document.getElementById("table_list_2").style.display = 'none' ;     
    }
    else if(document.getElementById("table_list_3").style.display == 'block') {;   
        document.getElementById("table_list_4").style.display = 'block' ;   
        document.getElementById("table_list_3").style.display = 'none' ;    
    }
    else if(document.getElementById("table_list_4").style.display == 'block') {
        document.getElementById("table_list_5").style.display = 'block';      
        document.getElementById("table_list_4").style.display = 'none' ;     
    }
} 

$(document).ready(function() {
    // 회원가입 pattern
    var emailPat = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
    var phonePat = /^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$/;
    var idPat = /[a-zA-Z0-9_-]{5,20}/;
    var pwPat = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;

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
        // Stop acting like a button
        e.preventDefault();
        // Get the field name
        fieldName = $(this).attr('data-field');
        // Get its current value
        var currentVal = parseInt($('input[name='+fieldName+']').val());
        // If it isn't undefined or its greater than 0
        if (!isNaN(currentVal) && currentVal > 1) {
            // Decrement one
            $('input[name='+fieldName+']').val(currentVal - 1);
            $('.people').html(currentVal - 1 + '명');
        } else {
            // Otherwise put a 0 there
            $('input[name='+fieldName+']').val(1);
        }
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

    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    var myPos = {lat: lat, lng: lng};
	var marker = new google.maps.Marker({position: myPos});
    marker.setMap(map);
}


function choice_people() {
    $('.hotel_reserve_people').css('display', 'block');
    $('.hotel_room_select').css('display', 'none');
    $('.hotel_reserve_people').toggleClass('');
}

function choice_room() {
    $('.hotel_room_select').css('display', 'block');
    $('.hotel_reserve_people').css('display', 'none');
}

function hotel_room_select(text){
    $('.hotel_room_select').css('display', 'none');
    value = $(text).text();
    $(".room").html(value);
}

