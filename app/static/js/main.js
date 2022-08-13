$(function(){
    $("#currentLocationBtn").click(function(){
        if ("geolocation" in navigator){ //check geolocation available
            //try to get user current location using getCurrentPosition() method
            console.log("current location");
            navigator.geolocation.getCurrentPosition(function(position){
                console.log("xxxx");
                $("#geoText").val(position.coords.latitude+","+position.coords.longitude );

            });
        }else{
            console.log("Browser doesn't support geolocation!");
        }
    });
});
