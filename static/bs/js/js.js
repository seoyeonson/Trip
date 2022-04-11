var mapProp;

// main 호텔 검색
function search_hotel() {
    document.getElementById("hotel_search").style.display ='block';
    document.getElementById("vacation_search").style.display ='none';
    document.getElementById("vacation_location").style.display = 'none';
    $('.vacation_reserve_people').css('display', 'none');
}

// main 여행지 검색
function search_vacation() {
    document.getElementById("hotel_search").style.display ='none';
    document.getElementById("vacation_search").style.display ='block';
    document.getElementById("hotel_location").style.display = 'none';
    document.getElementById("date_pick").style.display = 'none';
    $('.hotel_reserve_people').css('display', 'none');
}

function search_location() {
    $('#hotel_location').css('display', 'block');
    $('#date_pick').css('display', 'none');
    $('.hotel_reserve_people').css('display', 'none');
}

function choice_people() {
    $('#hotel_location').css('display', 'none');
    $('#date_pick').css('display', 'none');
    $('.hotel_reserve_people').css('display', 'block');
    $('.hotel_room_select').css('display', 'none');
}

function hotel_lo_select(text){
    $('.hotel_location').css('display', 'none');
    value = $(text).text();
    $('#lo_text').html(value);
    $('input[name=SIGUN_NM]').attr('value', value);
}

function choice_date(){
    $('.date_pick').css('display', 'block');
    $('.hotel_reserve_people').css('display', 'none');
    $('.hotel_room_select').css('display', 'none');
}

function vacation_choice_people(){
    $('.vacation_location').css('display', 'none');
    $('.vacation_reserve_people').css('display', 'block');
}

function search_va_location() {
    $('.vacation_reserve_people').css('display', 'none');
    document.getElementById("vacation_location").style.display ='block';
}

function vacation_lo_select(text) {
    $('.vacation_location').css('display', 'none');
    value = $(text).text();
    $('#va_lo_text').html(value);
    $('input[id=va_lo_text]').attr('value', value);
}

function get_date() {
    document.getElementById("date_pick").style.display ='block';
    document.getElementById("hotel_location").style.display ='none';
    $('.hotel_reserve_people').css('display', 'none');
}

$(document).ready(function() {
    // 회원가입 pattern
    var emailPat = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
    var phonePat = /^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$/;
    var idPat = /[a-zA-Z0-9_-]{5,20}/;
    var pwPat = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;

    // $("#submit_day").click(function() {
    //     $("#chk_in").html(start_day);
    //     $("#chk_out").html(end_day);
    // });

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

    // 인원수 선택
    $('[data-quantity="plus"]').click(function(e){
        e.preventDefault();
        fieldName = $(this).attr('data-field');
        var currentVal = parseInt($('input[name='+fieldName+']').val());
        if (!isNaN(currentVal)) {
            $('input[name='+fieldName+']').val(currentVal + 1);
            if(fieldName == 'hotel_reserve_people'){
                $('.people').html(currentVal + 1 + '명');
            }else{
                $('.va_people').html(currentVal + 1 + '명');
            }
        } else {
            $('input[name='+fieldName+']').val(1);
        }

        var pk = $('input[name=hotel_pk]').val();
        var hotel_reserve_people = $('input[name=hotel_reserve_people]').val();
        var start_date = $('input[name=start_date]').val();
        var end_date = $('input[name=end_date]').val();
        var html ="";

        $.ajax({ // <새로고침> 없이 ajax로 서버와 통신하겠다.
        type: "POST", // 데이터를 전송하는 방법을 지정
        url: "/option_change/"+ pk +"/", // 통신할 url을 지정
        data: {'pk': '{{ hotel.hotel_id }}', 'hotel_reserve_people': hotel_reserve_people, 'start_date' : start_date, 'end_date': end_date, 'csrfmiddlewaretoken': '{{ csrf_token }}'}, // 서버로 데이터 전송시 옵션
        dataType: "json", 
            success:function(json){
                console.log("성공");
                for (var i=0;i<json['hotel_room'].length;i++){
                    // console.log("들어옴");
                    // console.log(json['hotel_room']);
                    // console.log(json['hotel_reserve_people']);
                    // console.log(json['hotel_room'][i]['room_people']);
                    if(json['hotel_reserve_people'] <= json['hotel_room'][i]['room_people']){
                        html += '<a onclick="hotel_room_select(this)" class="select" data-value="'+ json['hotel_room'][i]['room_type'] + '"><li id="'+ json['hotel_room'][i]['room_type'] + '" class="hotel_room_select" value="'+ json['hotel_room'][i]['room_id'] + '">'+ json['hotel_room'][i]['room_type'] + '</li></a>'
                    }
                }
                $('.hotel_room_type').html(html);
            },
            error : function(xhr,errmsg,err) {
                console.log("실패"); 
            }
        });
    });

    $('[data-quantity="minus"]').click(function(e) {
        e.preventDefault();
        fieldName = $(this).attr('data-field');
        var currentVal = parseInt($('input[name='+fieldName+']').val());
        if (!isNaN(currentVal) && currentVal > 1) {
            $('input[name='+fieldName+']').val(currentVal - 1);
            if(fieldName == 'hotel_reserve_people'){
                $('.people').html(currentVal - 1 + '명');
            }else{
                $('.va_people').html(currentVal - 1 + '명');
            }
        } else {
            $('input[name='+fieldName+']').val(1);
        }

        var pk = $('input[name=hotel_pk]').val();
        var hotel_reserve_people = $('input[name=hotel_reserve_people]').val();
        var start_date = $('input[name=start_date]').val();
        var end_date = $('input[name=end_date]').val();
        var html = "";

        $.ajax({ // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
            type: "POST", // 데이터를 전송하는 방법을 지정
            url: "/option_change/"+ pk +"/", // 통신할 url을 지정
            data: {'pk': '{{ hotel.hotel_id }}', 'hotel_reserve_people': hotel_reserve_people, 'start_date' : start_date, 'end_date': end_date, 'csrfmiddlewaretoken': '{{ csrf_token }}'}, // 서버로 데이터 전송시 옵션
            dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
                success:function(json){
                    console.log("성공");
                    for (var i=0;i<json['hotel_room'].length;i++){
                        // console.log("들어옴");
                        // console.log(json['hotel_room']);
                        // console.log(json['hotel_reserve_people']);
                        // console.log(json['hotel_room'][i]['room_people']);
                        if(json['hotel_reserve_people'] <= json['hotel_room'][i]['room_people']){
                            html += '<a onclick="hotel_room_select(this)" class="select" data-value="'+ json['hotel_room'][i]['room_type'] + '"><li id="'+ json['hotel_room'][i]['room_type'] + '" class="hotel_room_select" value="'+ json['hotel_room'][i]['room_id'] + '">'+ json['hotel_room'][i]['room_type'] + '</li></a>'
                        }
                    }
                    $('.hotel_room_type').html(html);
                },
                error:function(xhr,errmsg,err) {
                    console.log("실패"); 
                }
        });
    });

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

// hotel_detail room 선택
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