document.writeln("hello");

var now = new Date;
console.log(now);
var time_end = now.getTime();
console.log(time_end);
var time_start = time_end - 2.0 * 24 * 60 * 60 * 1000;

// nimbits url
url =  "http://app.nimbits.com/service/series?"
       + "email=drdrsoto@gmail.com"
       + "&secret=01787ade-c6d6-4f9b-8b86-20850af010d9"
       + "&point=603_Test_Stream"
       + "&sd=" + time_start
       + "&ed=" + time_end;

// pachube url
url =   "http://api.pachube.com/v2/feeds/43073/datastreams/01.json?"
      + "start=2011-12-31T17:00:00Z&"
      + "end=2011-12-31T23:00:00Z&"
      + "interval=0";

headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"}


document.writeln(url);

jQuery.ajax({
    url: url,
    headers:headers,
    success: function(data){
        console.log(data.datapoints);}
    });