$(document).ready(function(){
    if (document.getElementsByName("lat")[0].value == 0 && document.getElementsByName("lng")[0].value == 0){
        document.getElementById("map_none").style.display = 'block';
        document.getElementById("googleMap").style.display = 'none';
    }
    else{
        document.getElementById("map_none").style.display = 'none';
        document.getElementById("googleMap").style.display = 'block';
    }

    // $(function() {
    //     var a = document.getElementsByName("price[]")[0].value;
    //     var b = document.getElementsByName("price[]")[1].value;
    //     var c = document.getElementsByName("price[]").length;
    //     console.log(a)
    //     console.log(b)
    //     console.log(c) //2
        
    //     if(document.getElementsByName("price[]").length == 0) {
    //         min_price=0;
    //         min_price= Number(min_price); 
    //     }   else{
    //         let min_price=document.getElementsByName("price[]")[0].value;   
    //         for (var i=0; i<document.getElementsByName("price[]").length; i++){
    //             if (document.getElementsByName("price[]")[i].value<min_price){
    //                 min_price = document.getElementsByName("price[]")[i].value;
    //             }
    //         min_price= Number(min_price);   
    //         }
    //     min_price= min_price.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    //     document.getElementById("fn_price").innerText = min_price;
    //     }
    // });
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



