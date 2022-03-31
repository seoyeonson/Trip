function search_hotel() {
    document.getElementById("hotel_search").style.display ='block';
    document.getElementById("vacation_search").style.display ='none';
    document.getElementById("vacation_location").style.display = 'none';
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