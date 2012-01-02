var now = new Date;
var time_end = now.getTime();
var time_start = time_end - 4.0 * 24 * 60 * 60 * 1000;

url =  "http://app.nimbits.com/service/series?"
       + "email=drdrsoto@gmail.com"
       + "&secret=01787ade-c6d6-4f9b-8b86-20850af010d9"
       + "&point=603_Test_Stream"
       // date ranges in unix epoch milliseconds
       + "&sd=" + time_start
       + "&ed=" + time_end;

jQuery.getJSON(
    url,
    {format:"json"},
    function(data) {
        // these arrays are to get min and max ranges
        var times = new Array();
        var ydata = new Array();
        for (i in data) {
            data[i].d = data[i].d/4096.0*1.8*100;
            // date object
            times[i] = new Date(data[i].timestamp);
            ydata[i] = data[i].d;
         }
         var range_round = 1,
             yrange_max = Math.ceil(d3.max(ydata) / range_round) * range_round,
             yrange_min = Math.floor(d3.min(ydata) / range_round) * range_round,
             w = 1000,
             h = 500,
             p = 50,
             x = d3.time.scale()
                        .domain([d3.min(times),d3.max(times)])
                        .range([0,w]),
             y = d3.scale.linear()
                         .domain([yrange_min, yrange_max])
                         .range([h,0]);

         // create axes
         var vis = d3.select("#graph")
                     .data([data])
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
            .x( function(d) { return x(d.timestamp);} )
            .y( function(d) { return y(d.d);} ));

        // data points as circles
        vis.selectAll("circle.line")
            .data(data)
            .enter().append("svg:circle")
            .attr("class","line")
            .attr("cx", function(d) { return x(d.timestamp);})
            .attr("cy", function(d) { return y(d.d);})
            .attr("r", 2);

         var vrules = vis.selectAll("g.vrule")
             .data(x.ticks(d3.time.hours, 12))
             .enter().append("svg:g")
             .attr("class", "rule");

         // vertical grid lines
         vrules.append("svg:line")
             //.attr("class", function (d,i) {return i ? null : "axis";})
             .attr("x1", x)
             .attr("x2", x)
             .attr("y1", 0)
             .attr("y2", h - 1);

         // x tick text
         vrules.append("svg:text")
             .attr("x", x)
             .attr("y", h + 20)
             .attr("dy", ".71em")
             .attr("text-anchor", "middle")
             //.text(x.tickFormat(d3.time.hours, 2));
             .text(d3.time.format('%m-%d %H:%M'));

        // vertical axis line
        // right now this is redundant since a line gets inked for each data element
        vrules.append("svg:line")
            // axis has different stroke in css
            .attr("class", "axis")
            .attr("x1", x(d3.min(times)))
            .attr("x2", x(d3.min(times)))
            .attr("y1", y(yrange_min))
            .attr("y2", y(yrange_max));

        var hrules = vis.selectAll("g.hrule")
            .data(y.ticks(10))
            .enter().append("svg:g")
            .attr("class", "rule");

        // y tick text
         hrules.append("svg:text")
             .attr("y", y)
             .attr("x", -10)
             .attr("dy", ".35em")
             .attr("text-anchor", "end")
             .text(y.tickFormat(10));
             //.text(String);

        // horizontal grid lines
         hrules.append("svg:line")
             .attr("x1", x(d3.min(times)))
             .attr("x2", x(d3.max(times)))
             .attr("y1", y)
             .attr("y2", y);

        // horizontal axis line
        hrules.append("svg:line")
            .attr("class", "axis")
            .attr("x1", x(d3.min(times)))
            .attr("x2", x(d3.max(times)))
            .attr("y1", y(yrange_min))
            .attr("y2", y(yrange_min));

    });
