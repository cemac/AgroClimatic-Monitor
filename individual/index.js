let d3 = require('d3')

const plotheight = 200


var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 110, left: 40},
    margin2 = {top: 430, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    height2 = +svg.attr("height") - margin2.top - margin2.bottom;
    

var parseDate = d3.timeParse("%m/%d/%Y %H:%M");

// var x = d3.scaleTime().range([0, width]),
var     x2 = d3.scaleTime().range([0, width]),
    // y = d3.scaleLinear().range([height, 0]),
    y2 = d3.scaleLinear().range([height2, 0]);

var xAxis2 = d3.axisBottom(x2)

var brush = d3.brushX()
    .extent([[0, 0], [width, height2]])
    // .on("brush end", brushed);

var zoom = d3.zoom()
    .scaleExtent([1, Infinity])
    .translateExtent([[0, 0], [width, height]])
    .extent([[0, 0], [width, height]])
    .on("zoom", zoomed);



    var line2 = d3.line()
        .x(function (d) { return x2(+d.Date); })
        .y(function (d) { return y2(+d.Air_Temp); });

    var clip = svg.append("defs").append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("width", width)
        .attr("height", height)
        .attr("x", 0)
        .attr("y", 0); 



    var focus = svg.append("g")
        .attr("class", "focus")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var context = svg.append("g")
    .attr("class", "context")
    .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

svg.style('background-color','whitesmoke')


var allcharts=[];





////////
d3.csv("data.tsv").then(function (data) {
  data = data.map(function type(d) {
    d.Date = parseDate(d.Date);
    d.Air_Temp = +d.Air_Temp;
    return d;
  })
  window.d = data
  // x2.domain(x.domain());
  // y2.domain(y.domain());
  x2.domain(d3.extent(data, function(d) { return d.Date; }));
  y2.domain([0, d3.max(data, function (d) { return d.Air_Temp; })]);
  
  
  function indicator(){
      id = allcharts.length
      start = id*plotheight 
      console.log(id,start)
      var x = d3.scaleTime().range([0, width]),
          y = d3.scaleLinear().range([start+plotheight-50, start]);
  
  var line = d3.line()
      .x(function (d) { return x(d.Date); })
      .y(function (d) { return y(+d.Air_Temp); });
      
  x.domain(d3.extent(data, function(d) { return d.Date; }));
  y.domain([0, d3.max(data, function (d) { return d.Air_Temp; })]);

  var Line_chart = svg.append("g")
      .attr("class", "focus")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .attr("clip-path", "url(#clip)");



  Line_chart.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", d=>{console.log('dsf',d);line(d);});

      var xAxis = d3.axisBottom(x),
          yAxis = d3.axisLeft(y);
    
          focus.append("g")
              .attr("class", "axis axis--x")
              .attr("transform", "translate(0," + ((1+id)*plotheight-50) + ")")
              .call(xAxis);

          focus.append("g")
              .attr("class", "axis axis--y")
              .call(yAxis);

    
    
    return {x,y,line,Line_chart,xAxis,yAxis}
      
    }

    allcharts.push(indicator())
    allcharts.push(indicator())

    endplots= plotheight*allcharts.length
    
    svg.attr('height', endplots+100)
    clip.attr('height',endplots+100)
    
    
    context.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line2);


  context.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height2 + ")")
      .call(xAxis2);

      context.append("g")
          .attr("class", "brush")
          .call(brush)
          .call(brush.move, x2.range());


  svg.append("rect")
      .attr("class", "zoom")
      .attr("width", width)
      .attr("height", endplots)
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .call(zoom)
      .attr('fill','red')
      


brushed('loading')

});











/////// brush functions
function brushed(e) {
    console.log(e)    
  if (e.type === "zoom") return; // ignore brush-by-zoom
  
  var s = e.selection || x2.range();

  allcharts.forEach(c=>{
  console.log(c)
  c.x.domain(s.map(x2.invert, x2));
  c.Line_chart.select(".line").attr("d", c.line);
focus.select(".axis--x").call(c.xAxis);
  })
  
   
  
  svg.select(".zoom").call(zoom.transform, d3.zoomIdentity
      .scale(width / (s[1] - s[0]))
      .translate(-s[0], 0));
}

function zoomed(e) {
  if (e.type === "brush") return; // ignore zoom-by-brush
  var t = e.transform;
  
    allcharts.forEach(c=>{
  c.x.domain(t.rescaleX(x2).domain());
  c.Line_chart.select(".line").attr("d", c.line);
  focus.select(".axis--x").call(c.xAxis);
  context.select(".brush").call(brush.move, c.x.range().map(t.invertX, t));
})
}


