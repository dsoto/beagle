document.writeln("hello");

var now = new Date;
console.log(now);
var time_end = now.getTime();
var time_start = time_end - 0.5 * 24 * 60 * 60 * 1000;

// nimbits url
url =  "http://app.nimbits.com/service/series?"
       + "email=drdrsoto@gmail.com"
       + "&secret=01787ade-c6d6-4f9b-8b86-20850af010d9"
       + "&point=603_Test_Stream"
       + "&sd=" + time_start
       + "&ed=" + time_end;



document.writeln(url);

jQuery.ajax({
    url: url,
    success: function(data){
        console.log(data);}
    });