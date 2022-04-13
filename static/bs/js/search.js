$(document).ready(function(){
    if (document.getElementsByName("lat")[0].value == 0 && document.getElementsByName("lng")[0].value == 0){
        document.getElementById("map_none").style.display = 'block';
        document.getElementById("googleMap").style.display = 'none';
    }
    else{
        document.getElementById("map_none").style.display = 'none';
        document.getElementById("googleMap").style.display = 'block';
    }

    $(function() {
            
        if(document.getElementsByName("price[]").length == 0) {
            min_price=0;
            min_price= Number(min_price); 
        }   else{
            let min_price=document.getElementsByClassName("table_list")[0].children[4].children[0].value;   
            for (var j=0; j<document.getElementsByClassName("table_list")[0].children[4].children.length; j++){
                if (document.getElementsByClassName("table_list")[0].children[4].children[j].value<min_price){
                    min_price = document.getElementsByClassName("table_list")[0].children[4].children[j].value;
                }
            min_price= Number(min_price);   
            }
        min_price= min_price.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById("fn_price1").innerText = min_price;
        }

            
        if(document.getElementsByName("price[]").length == 0) {
            min_price=0;
            min_price= Number(min_price); 
        }   else{
            let min_price=document.getElementsByClassName("table_list")[1].children[4].children[0].value;   
            for (var j=0; j<document.getElementsByClassName("table_list")[1].children[4].children.length; j++){
                if (document.getElementsByClassName("table_list")[1].children[4].children[j].value<min_price){
                    min_price = document.getElementsByClassName("table_list")[1].children[4].children[j].value;
                }
            min_price= Number(min_price);   
            }
        min_price= min_price.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById("fn_price2").innerText = min_price;
        }
        if(document.getElementsByName("price[]").length == 0) {
            min_price=0;
            min_price= Number(min_price); 
        }   else{
            let min_price=document.getElementsByClassName("table_list")[2].children[4].children[0].value;   
            for (var j=0; j<document.getElementsByClassName("table_list")[2].children[4].children.length; j++){
                if (document.getElementsByClassName("table_list")[2].children[4].children[j].value<min_price){
                    min_price = document.getElementsByClassName("table_list")[2].children[4].children[j].value;
                }
            min_price= Number(min_price);   
            }
        min_price= min_price.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById("fn_price3").innerText = min_price;
        }
        if(document.getElementsByName("price[]").length == 0) {
            min_price=0;
            min_price= Number(min_price); 
        }   else{
            let min_price=document.getElementsByClassName("table_list")[3].children[4].children[0].value;   
            for (var j=0; j<document.getElementsByClassName("table_list")[3].children[4].children.length; j++){
                if (document.getElementsByClassName("table_list")[3].children[4].children[j].value<min_price){
                    min_price = document.getElementsByClassName("table_list")[3].children[4].children[j].value;
                }
            min_price= Number(min_price);   
            }
        min_price= min_price.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById("fn_price4").innerText = min_price;
        }
        if(document.getElementsByName("price[]").length == 0) {
            min_price=0;
            min_price= Number(min_price); 
        }   else{
            let min_price=document.getElementsByClassName("table_list")[4].children[4].children[0].value;   
            for (var j=0; j<document.getElementsByClassName("table_list")[4].children[4].children.length; j++){
                if (document.getElementsByClassName("table_list")[4].children[4].children[j].value<min_price){
                    min_price = document.getElementsByClassName("table_list")[4].children[4].children[j].value;
                }
            min_price= Number(min_price);   
            }
        min_price= min_price.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById("fn_price5").innerText = min_price;
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



