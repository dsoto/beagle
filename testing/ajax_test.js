document.writeln("hello");

var now = new Date;
//console.log(now);
var time_end = now.getTime();
//console.log(time_end);
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


//document.writeln(url);

jQuery.ajax({
    url: url,
    headers:headers,
    success: function(data){
                var times = [];
                var ydata = [];
                for (i in data.datapoints) {
                    // date object
                    times[i] = new Date(data.datapoints[i].at);
                    data.datapoints[i].at = times[i];
                    console.log(times[i].toString());
                    ydata[i] = data.datapoints[i].value;
                 }
                 //console.log(times);
                 //console.log(ydata);
                 var w = 500,
                     h = 500,
                     p = 50,
                     x = d3.time.scale.utc()
                                .domain([d3.min(times),d3.max(times)])
                                .range([0,w]),
                     y = d3.scale.linear()
                                 .domain([d3.min(ydata),d3.max(ydata)])
                                 .range([h,0]);

                 // create axes
                 var vis = d3.select("body")
                             .data([data.datapoints])
                             .append("svg:svg")
                             .attr("width", w + p * 2)
                             .attr("height", h + p * 2)
                             .append("svg:g")
                             .attr("transform", "translate(" + p + "," + p + ")");

                 // line path
                 vis.append("svg:path")
                    .attr("class","line")
                    .attr("d", d3.svg.line()
                     // d is some magic that iterates over the d3values object
                    .x( function(d) { return x(d.at);} )
                    .y( function(d) { return y(d.value);} ));

                // data points as circles
                vis.selectAll("circle.line")
                    .data(data.datapoints)
                    .enter().append("svg:circle")
                    .attr("class","line")
                    .attr("cx", function(d) { return x(d.at);})
                    .attr("cy", function(d) { return y(d.value);})
                    .attr("r", 2);

        }
    });

