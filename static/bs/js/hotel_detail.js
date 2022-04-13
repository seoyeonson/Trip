var pk;
var hotel_reserve_people;
var start_date;
var end_date;
var html;

$(document).ready(function(){
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
            },
        }, 
        function(start, end, label) {
            // console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
            startDate = start.format('YYYY-MM-DD');
            endDate = end.format('YYYY-MM-DD');
        });
    });

    // 인원수 선택
    $('[data-quantity="ho_plus"]').click(function(e){
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

        pk = $('input[name=hotel_pk]').val();
        hotel_reserve_people = $('input[name=hotel_reserve_people]').val();
        start_date = $('input[name=start_date]').val();
        end_date = $('input[name=end_date]').val();
        html = ""

        $.ajax({ // <새로고침> 없이 ajax로 서버와 통신하겠다.
        type: "POST", // 데이터를 전송하는 방법을 지정
        url: "/option_change/"+ pk +"/", // 통신할 url을 지정
        data: {'pk': '{{ hotel.hotel_id }}', 'hotel_reserve_people': hotel_reserve_people, 'start_date' : start_date, 'end_date': end_date}, // 서버로 데이터 전송시 옵션
        dataType: "json", 
            success:function(json){
                console.log("성공");
                if(json['reserve_pos'].length == 0){
                    html += '<a class="select"><li class="hotel_room_select">예약 가능한 방이 없습니다.</li></a>'
                }else{
                    for (var i=0;i<json['reserve_pos'].length;i++){
                        console.log("들어옴");
                        console.log(json['reserve_pos']);
                        console.log(json['reserve_pos'][i]['room_type']);
                        html += '<a onclick="hotel_room_select(this)" class="select" data-value="'+ json['reserve_pos'][i]['room_type'] + '"><li id="'+ json['reserve_pos'][i]['room_type'] + '" class="hotel_room_select" value="'+ json['reserve_pos'][i]['room_id'] + '">'+ json['reserve_pos'][i]['room_type'] + '</li></a>'
                    }
                }
                $('.hotel_room_type').html(html);       
            },
            error : function(xhr,errmsg,err) {
                console.log(xhr)
                    console.log(errmsg)
                    console.log(err)
                console.log("실패"); 
            }
        });
    });

    $('[data-quantity="ho_minus"]').click(function(e) {
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

        pk = $('input[name=hotel_pk]').val();
        hotel_reserve_people = $('input[name=hotel_reserve_people]').val();
        start_date = $('input[name=start_date]').val();
        end_date = $('input[name=end_date]').val();
        html = ""

        $.ajax({ // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
            type: "POST", // 데이터를 전송하는 방법을 지정
            url: "/option_change/"+ pk +"/", // 통신할 url을 지정
            data: {'pk': '{{ hotel.hotel_id }}', 'hotel_reserve_people': hotel_reserve_people, 'start_date' : start_date, 'end_date': end_date}, // 서버로 데이터 전송시 옵션
            dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
                success:function(json){
                    console.log("성공");
                    if(json['reserve_pos'].length == 0){
                        html += '<a class="select"><li class="hotel_room_select">예약 가능한 방이 없습니다.</li></a>'
                    }else{
                        for (var i=0;i<json['reserve_pos'].length;i++){
                            console.log("들어옴");
                            console.log(json['reserve_pos']);
                            console.log(json['reserve_pos'][i]['room_type']);
                            html += '<a onclick="hotel_room_select(this)" class="select" data-value="'+ json['reserve_pos'][i]['room_type'] + '"><li id="'+ json['reserve_pos'][i]['room_type'] + '" class="hotel_room_select" value="'+ json['reserve_pos'][i]['room_id'] + '">'+ json['reserve_pos'][i]['room_type'] + '</li></a>'
                        }
                    }
                    $('.hotel_room_type').html(html);
                },
                error:function(xhr,errmsg,err) {
                    console.log("실패"); 
                }
        });
    });

    $('[name="reserve_date_choice"]').click(function(e) {
        $('.date_pick').css('display', 'none');
        $('.hotel_detail_reserve_checkin').html('<i class="fas fa-calendar-alt"></i><span class="icon_before">'+startDate);
        $('.hotel_detail_reserve_checkout').html(endDate);
        $('input[name=start_date]').attr('value', startDate);
        $('input[name=end_date]').attr('value', endDate);
        console.log("startDate", startDate, "endDate", endDate);

        pk = $('input[name=hotel_pk]').val();
        hotel_reserve_people = $('input[name=hotel_reserve_people]').val();
        start_date = $('input[name=start_date]').val();
        end_date = $('input[name=end_date]').val();
        html = ""

        $.ajax({ // <새로고침> 없이 ajax로 서버와 통신하겠다.
            type: "POST", // 데이터를 전송하는 방법을 지정
            url: "/option_change/"+ pk +"/", // 통신할 url을 지정
            data: {'pk': '{{ hotel.hotel_id }}', 'hotel_reserve_people': hotel_reserve_people, 'start_date' : start_date, 'end_date': end_date}, // 서버로 데이터 전송시 옵션
            dataType: "json", 
                success:function(json){
                    console.log("성공");
                    if(json['reserve_pos'].length == 0){
                        html += '<a class="select"><li class="hotel_room_select">예약 가능한 방이 없습니다.</li></a>'
                    }else{
                        for (var i=0;i<json['reserve_pos'].length;i++){
                            console.log("들어옴");
                            console.log(json['reserve_pos']);
                            console.log(json['reserve_pos'][i]['room_type']);
                            html += '<a onclick="hotel_room_select(this)" class="select" data-value="'+ json['reserve_pos'][i]['room_type'] + '"><li id="'+ json['reserve_pos'][i]['room_type'] + '" class="hotel_room_select" value="'+ json['reserve_pos'][i]['room_id'] + '">'+ json['reserve_pos'][i]['room_type'] + '</li></a>'
                        }
                    }
                    $('.hotel_room_type').html(html);
                },
                error : function(xhr,errmsg,err) {
                    console.log(xhr)
                    console.log(errmsg)
                    console.log(err)
                    console.log("실패"); 
                }
            });
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