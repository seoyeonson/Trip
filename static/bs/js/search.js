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

    
    // return  document.getElementsByName("lat").value,  document.getElementsByName("lat").value;
    
    map.setCenter({lat: ch_lat, lng: ch_lng});
    myPos = {lat: ch_lat, lng: ch_lng};
	marker = new google.maps.Marker({position: myPos});
    
    marker.setMap(map);
}