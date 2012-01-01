
// create date ranges from midnight - midnight local time
var now = new Date();
var date_end = new Date(now.getFullYear(), now.getMonth(), now.getDate());
date_end.setDate(date_end.getDate() + 2);
var date_start = new Date(date_end);
date_start.setDate(date_start.getDate() - 3);

// pachube url
// the iso dates are on UTC
var url = "http://api.pachube.com/v2/feeds/43073/datastreams/01.json?"
        + "start=" + d3.time.format.iso(date_start)
        + "&end=" + d3.time.format.iso(date_end)
        + "&interval=900";

console.log(url);

var headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"};

jQuery.ajax({
    url: url,
    headers: headers,
    success: function (data) {
        console.log(data);
        var times = [],
            ydata = [];
        for (i in data.datapoints) {
            data.datapoints[i].value = data.datapoints[i].value / 4096 * 1.8 * 100;
            times[i] = new Date(data.datapoints[i].at);
            data.datapoints[i].at = times[i];
            ydata[i] = data.datapoints[i].value;
        }
        console.log(d3.time.format.iso(d3.max(times)));
        var range_round = 1,
            yrange_max = Math.ceil(d3.max(ydata) / range_round) * range_round,
            yrange_min = Math.floor(d3.min(ydata) / range_round) * range_round,
            w = 1000,
            h = 500,
            p = 50,
            x = d3.time.scale.utc()
                .domain([date_start, date_end])
                .range([0, w]),
            y = d3.scale.linear()
                .domain([yrange_min, yrange_max])
                .range([h, 0]);

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
            .attr("class", "line")
            .attr("d", d3.svg.line()
             // d is some magic that iterates over the d3values object
                .x(function (d) { return x(d.at); })
                .y(function (d) { return y(d.value); }));

        // data points as circles
        vis.selectAll("circle.line")
            .data(data.datapoints)
            .enter().append("svg:circle")
            .attr("class", "line")
            .attr("cx", function (d) { return x(d.at); })
            .attr("cy", function (d) { return y(d.value); })
            .attr("r", 2);
        var vrules = vis.selectAll("g.vrule")
                .data(x.ticks(d3.time.hours, 12))
                .enter().append("svg:g")
                .attr("class", "rule");

        //vertical grid lines
        vrules.append("svg:line")
            //.attr("class", function (d,i) {return i ? null : "axis";})
            .attr("x1", x)
            .attr("x2", x)
            .attr("y1", 0)
            .attr("y2", h - 1);
        //x tick text
        vrules.append("svg:text")
            .attr("x", x)
            .attr("y", h + 20)
            .attr("dy", ".71em")
            .attr("text-anchor", "middle")
            //.text(x.tickFormat(d3.time.hours, 2));
            .text(d3.time.format('%m-%d %H:%M'));

        //vertical axis line
        //right now this is redundant since a line gets inked for each data element
        vrules.append("svg:line")
            // axis has different stroke in css
            .attr("class", "axis")
            .attr("x1", x(date_start))
            .attr("x2", x(date_start))
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
            .attr("x1", x(date_start))
            .attr("x2", x(date_end))
            .attr("y1", y)
            .attr("y2", y);

        // horizontal axis line
        hrules.append("svg:line")
            .attr("class", "axis")
            .attr("x1", x(date_start))
            .attr("x2", x(date_end))
            .attr("y1", y(yrange_min))
            .attr("y2", y(yrange_min));


    }
});

