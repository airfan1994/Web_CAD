var url = "http://127.0.0.1:8080";

		var latestid=0;
	


function makegetdata()
       {
	$.getJSON(url.concat("/stat/speed"), function(websites){
        
	var curtime= (new Date().getHours())+":"+(new Date().getMinutes())+":"+(new Date().getSeconds());
 	    myLiveChart.addData([websites.up,websites.down], curtime);
		 $("#upspeed").text(websites.up+"kB/s");
		 $("#downspeed").text(websites.down+"kB/s");
	});
	}


setInterval(function(){
	alert("123");
  // Add two random numbers for each dataset
  makegetdata();
  latestid=latestid+1;
   if (latestid>20)
   {
     myLiveChart.removeData();
    }
  // Remove the first point so we dont just add values forever
  //
}, 5000);



