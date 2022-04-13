$(document).ready(function(){

    $("#cancel_btn").click(function(){
        location.href = "/admin_hotel/"
    });

    $(".add_row").off().on("click", addRow)
});


function sample4_execDaumPostcode() {
    new daum.Postcode({
        oncomplete: function(data) {
            // 도로명 주소의 노출 규칙에 따라 주소를 표시한다.
            // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
            var roadAddr = data.roadAddress; // 도로명 주소 변수
            var extraRoadAddr = ''; // 참고 항목 변수

            // 법정동명이 있을 경우 추가한다. (법정리는 제외)
            // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
            if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
                extraRoadAddr += data.bname;
            }
            // 건물명이 있고, 공동주택일 경우 추가한다.
            if(data.buildingName !== '' && data.apartment === 'Y'){
               extraRoadAddr += (extraRoadAddr !== '' ? ', ' + data.buildingName : data.buildingName);
            }
            // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
            if(extraRoadAddr !== ''){
                extraRoadAddr = ' (' + extraRoadAddr + ')';
            }

            // 우편번호와 주소 정보를 해당 필드에 넣는다.
            document.getElementById('sample4_postcode').value = data.zonecode;
            document.getElementById("sample4_roadAddress").value = roadAddr;
            
            // 참고항목 문자열이 있을 경우 해당 필드에 넣는다.


            
            if(roadAddr !== ''){
                document.getElementById("sample4_extraAddress").value = extraRoadAddr;
            } else {
                document.getElementById("sample4_extraAddress").value = '';
            }
            var geocoder = new kakao.maps.services.Geocoder();
            geocoder.addressSearch(roadAddr, function(result,status){
                if (status === kakao.maps.services.Status.OK) {
                    document.getElementById("lat").value = result[0].y;
                    document.getElementById("lng").value = result[0].x;
               }
            });
            var sigun = data.sigungu.split(' ')[0]
            document.getElementById("hotel_area").value=sigun
        }
    }).open()
}
   

function addRow(){
    room_table =  $('#room_table').append('<tr>'
        + '<td><input type="text" name="room_type[]" value="{{ hotel_room.room_type }}" placeholder="객실타입 입력"></td>'
        + '<td><input type="number" name="room_price[]" value="{{ hotel_room.room_price }}" placeholder="객실가격 입력"></td>'
        + '<td><input type="number" name="room_people[]" value="{{ hotel_room.room_people }}" placeholder="객실인원 입력"></td>'
        + '</tr>');
};



