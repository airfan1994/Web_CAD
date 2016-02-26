    $(function() {  
        setInterval("GetTime()", 1000);  
    });  
  
    function GetTime() {  
        var mon, day, now, hour, min, ampm, time, str, tz, end, beg, sec;  

        mon = new Array("1", "2", "3", "4", "5", "6", "7", "8",  
                "9", "10", "11", "12");  
        day = new Array("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");  

        now = new Date();  
        hour = now.getHours();  
        min = now.getMinutes();  
        sec = now.getSeconds();  
        if (hour < 10) {  
            hour = "0" + hour;  
        }  
        if (min < 10) {  
            min = "0" + min;  
        }  
        if (sec < 10) {  
            sec = "0" + sec;  
        }  
        $("#Timer").html(  
                "<nobr>" + day[now.getDay()] + ", " + now.getFullYear() + "-" + mon[now.getMonth()] + "-"  
                        + now.getDate() + ", "  + hour  
                        + ":" + min + ":" + sec + "</nobr>");  
    };
 