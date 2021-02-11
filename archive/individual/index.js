let d3 = require("d3");

const plotheight = 140;

var hash = "1100049";



// svg.style("background-color", "whitesmoke");

var bar = d3.select("#bar")
var svg = d3.select("#svg"),
    margin = {
        top: 20,
        right: 20,
        bottom: 110,
        left: 40
    },
    // margin2 = {top: 430, right: 20, bottom: 30, left: 40},
    width = +window.innerWidth - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;
// height2 = +svg.attr("height") - margin2.top - margin2.bottom;
const defs = svg.append("defs")
const parseDate = function(x) {
    return x.map(y => d3.timeParse("%Y-%m")(y));
};

var x = d3.scaleTime().range([0, width]);
var x2 = d3.scaleTime().range([0, width]),
    // y = d3.scaleLinear().range([height, 0]),
    y2 = d3.scaleLinear().range([20, 0]);

var xAxis2 = d3.axisBottom(x2);

const color = '003049-d62828-f77f00-fcbf49-eae2b7'.split('-').map(d=>'#'+d)//.reverse()

//box
var brush = d3.brushX().extent([[0, 10], [width, 70]]);
// .on("brush end", brushed);

var zoom = d3
    .zoom()
    .scaleExtent([1, Infinity])
    .translateExtent([[0, 0], [width, height]])
    .extent([[0, 0], [width, height]])
    .on("zoom", update);

var line2 = d3
    .line()
    .x(function(d) {
        return x2(+d.Date);
    })
    .y(function(d) {
        return y2(+d.Air_Temp);
    });

var clip = bar
    .append("defs")
    .append("svg:clipPath")
    .attr("id", "clip")
    .append("svg:rect")
    .attr("width", width)
    .attr("height", 100)
    .attr("x", 0)
    .attr("y", 0);


var context = bar
    .append("g")
    .attr("class", "context")
    .attr("transform", "translate(" + margin.left + "," + 0 + ")");


var allcharts = [];

////////
d3.json(`../processed/muncipalities/file_${hash}.json`).then(function(data) {
    window.d = data;

    var dates = [];

    Object.values(data).forEach(d => {
        dates = dates.concat(d.x).concat(d.px);
    });
    dates = parseDate(dates);

    window.e = dates;
    // x2.domain(x.domain());
    // y2.domain(y.domain());
    x.domain(d3.extent(dates));
    x2.domain(x.domain());
    y2.domain([0, 8]);

//////////////
    function indicator(item, whatami) {
        
        console.log("item", item);
        
        
        var areadir = item.lim[0]<item.lim[1]
        
        item.allx = item.x.concat(item.px);
        item.ally = item.y.concat(item.py);

        item.x = parseDate(item.x);
        item.px = parseDate(item.px);
        item.allx = parseDate(item.allx);

        item.x.push(item.x[item.x.length-1])
        item.x.push(item.x[item.x.length-1])
        
        item.y.push(item.lim[0])
        item.y.push(item.lim[1])
        
        id = allcharts.length;
        start = id * plotheight;
        console.log(id, start);
        
        var y = d3.scaleLinear().range([start + plotheight - 50, start]).domain(item.lim||d3.extent(item.ally));




         var linearGradient = defs
                    .append("linearGradient")
                    .attr('gradientUnits',"userSpaceOnUse")
                    .attr("id", "gradient_"+whatami)
                    .attr("gradientTransform", "rotate(90)");

                    linearGradient.append("stop")
                        .attr("offset",0)
                        .attr("stop-color", color[0]);


                item.catlims.reverse().forEach((q,l)=>{
                    
                    console.log(q,l,y(q),(plotheight*6), y(q)/(plotheight*6))
                    
                    linearGradient.append("stop")
                        .attr("offset",y(q)/(plotheight*6+100))//,Math.abs((item.lim[1]+q)/(item.lim[0]-item.lim[1]))))
                        .attr("stop-color", color[l+1]);
                    
                    
                })
                
                linearGradient.append("stop")
                    .attr("offset",1)
                    .attr("stop-color", color[color.length]);


                // 
                // linearGradient.append("stop")
                //     .attr("offset", "25%")
                //     .attr("stop-color", color[2]);
                // 
                // linearGradient.append("stop")
                //     .attr("offset", "100%")
                //     .attr("stop-color", color[3]);
                // 
                // linearGradient.append("stop")
                //     .attr("offset", "75%")
                //     .attr("stop-color", color(4));
                // 
                // linearGradient.append("stop")
                //     .attr("offset", "100%")
                //     .attr("stop-color", color(5));
                // 
                // 
                    




        var line = d3
            .line()
            .x(function(d) {
                return x(d[0]);
            })
            .y(function(d) {
                return y(+d[1]);
            })
             .curve(d3.curveCatmullRom.alpha(0.1))
            
        var area = d3.area()
          .x(function(d) { return x(d[0]) })
          .y0(function(d) { 
              var lim = y.domain()[1]; 

              return (d[1]<lim)? y(d[1]) : y.range()[1]
          })
          .y1(function(d) { 
              var lim = y.domain()[0]; 
              // return y(d[2])
              return (d[2]>lim)? y(d[1]) : y.range()[0]
          })
          //.defined(true)
           .curve(d3.curveCatmullRom.alpha(0.5))

        var Line_chart = svg
            .append("g")
            .attr("class", "focus")
            .attr(
                "transform",
                "translate(" + margin.left + "," + margin.top + ")"
            )
            .attr("clip-path", "url(#clip)");

        Line_chart.append("path")
            //.datum(item)
            .datum(d3.zip(item.x, item.y))
            .attr("class", "line")
            
            .attr("d",line)
            .style('stroke',`url(#gradient_${whatami})`)
            
            
//////// AREAS 
            var areadata = (areadir)? d3.zip(item.px, item.pt, item.pb): d3.zip(item.px, item.pb, item.pt)
            Line_chart.append("path")
                //.datum(item)
                .datum(areadata)
                .attr("class", "area")
          .style("fill", "#cce5df")
          .style("stroke", "none")
          .style('opacity',.8)
          .attr("d", d=>area(d))
          
            
            // prediction line
            Line_chart.append("path")
                //.datum(item)
                .datum(d3.zip(item.px, item.py))
                .attr("class", "line")
                .attr("d",line)
                .style('opacity',.6)
                .style('stroke', 'green')   
                .style("stroke-dasharray", ("3, 3")) 
            
            

        var xAxis = d3.axisBottom(x), yAxis = d3.axisLeft(y).ticks(5);

        var focus = svg
            .append("g")
            .attr("class", "focus")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        focus
            .append("g")
            .attr("class", "axis axis--x")
            .attr(
                "transform",
                "translate(0," + ((1 + id) * plotheight - 50) + ")"
            )
            .call(xAxis);

        focus.append("g").attr("class", "axis axis--y").call(yAxis);
        
                svg.append("text")
                    .attr("x", width+35)
                    .attr("y", start+11)
                    .attr("dy", ".35em")
                    .style('text-anchor','end')
                    .text(whatami.replace('_',' ').toUpperCase());





        return {
            y,
            line,
            area,
            Line_chart,
            focus,
            xAxis,
            yAxis,
            whatami
        };
    }

    var keys = ["VHI", "SPI", "spi_01", "spi_03", "spi_06", "spi_12"]; //"IIS3",'RZSM'

    //Object.keys(data)

    keys.forEach(e => {
        console.log(e);
        var de = data[e]
        if (de) allcharts.push(indicator(de, e));
    });

    endplots = plotheight * allcharts.length;

    svg.attr("height", endplots + 100);
    clip.attr("height", endplots + 100);

    //
    // context.append("path")
    //     .datum(data)
    //     .attr("class", "line")
    //     .attr("d", line2);

    context
        .append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + 70 + ")")
        .call(xAxis2);

    context
        .append("g")
        .attr("class", "brush")
        .call(brush)
        .call(brush.move, x2.range());

    svg
        .append("rect")
        .attr("class", "zoom")
        .attr("width", width)
        .attr("height", endplots)
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .call(zoom)
        .attr("fill", "red");

    update({type:"brush"});
});




function update(e){
    
    switch (e.type){
        case 'brush':
        
        var s = e.selection || x2.range();

        allcharts.forEach(c => {
            console.log(c);
            x.domain(s.map(x2.invert, x2));
            c.Line_chart.selectAll(".line").attr("d", c.line);
            c.Line_chart.selectAll(".area").attr("d", c.area);
            c.focus.select(".axis--x").call(c.xAxis);
        });

        svg
            .select(".zoom")
            .call(
                zoom.transform,
                d3.zoomIdentity.scale(width / (s[1] - s[0])).translate(-s[0], 0)
            );
        break
        
        
        case 'zoom':
        var t = e.transform;

        allcharts.forEach(c => {
            x.domain(t.rescaleX(x2).domain());
            c.Line_chart.selectAll(".line").attr("d", c.line);
            c.Line_chart.selectAll(".area").attr("d", c.area);
            c.focus.select(".axis--x").call(c.xAxis);
            context.select(".brush").call(brush.move, x.range().map(t.invertX, t));
        });
    }
    
    
    
    
    
    
}















