$(document).ready(function(){

    $("#cancel_btn").click(function(){
        location.href = "/admin_hotel/"
    });

    $(".add_row").off().on("click", addRow)
});

function addRow(){
    room_table =  $('#room_table').append('<tr><td><input type="text" name="room_type[]" placeholder="객실타입 입력"></td><td><input type="number" name="room_price[]" placeholder="객실가격 입력"></td><td><input type="number" name="room_people[]" placeholder="객실인원 입력"></td></tr>');
};


