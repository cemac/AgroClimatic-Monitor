
let d3 = require("d3");
let L = require('leaflet')
// center of the map

var hash = "1100015";

var pkeys = ["VHI", "spi_01", "spi_03",]// "spi_06", "spi_12","IIS3",'RZSM']


// Create the map
var map = L.map('lmap',{
    center: [-62.31994628906251, -24.23757312392183].reverse(),
    zoom: 4,
    // dragging:false
});
var CyclOSM = L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
	maxZoom: 20,
	attribution: '<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | CEMAC '
});
map.addLayer(CyclOSM)

// colours 
const color = '003049-d62828-f77f00-fcbf49-eae2b7'.split('-').map(d=>'#'+d)

// date 
const parseDate = function(x) {
    return x.map(y => d3.timeParse("%Y-%m")(y));
};

 


// PLOTTING
var allplots = document.getElementById('allplot')
var allsize = allplots.getBoundingClientRect()

console.log(allsize)
const psvg = d3.select(allplots).append('svg')
psvg.attr('width',allsize.width ).attr('height',allsize.height)
// lineplot
var x = d3.scaleTime().range([0, allsize.width-20]);
var caty;

var format = d3.format('.3f')








d3.json(`../processed/muncipalities/file_${hash}.json`).then(function(data) {
    window.d = data;

    var dates = [];

    Object.values(data).forEach(d => {
        dates = dates.concat(d.x)
    })
    dates = parseDate(dates);
    x.domain(d3.extent(dates))

    window.e = data;

    // console.log(data,d3.extent(dates))

var lscale = []

pkeys.forEach(name=>{
    console.log(name)
data[name].t = parseDate(data[name].x)
var item = data[name]
data[name].t = parseDate(item.x)

var ylen =  item.catlims.length+2


caty = caty || d3.range(ylen).map(d=>allsize.height*(1-d/ylen)-20)
var y = d3.scaleLinear()
.range(caty)
.domain([item.lim[0]].concat(item.catlims).concat(item.lim[1]));


// console.log(allsize.height, y.domain(), y.range(), y(40))

var line = d3
    .line()
    .x(d=> x(d[0]))
    .y(d=> y(+d[1]))
     .curve(d3.curveCatmullRom.alpha(0.1))
     
     var ind = psvg
       .append("g")
       .attr("class", name).attr(
           "transform",
           "translate(10,0)")
      
      ind.append("path")
      .attr("class", "line "+name)
      .attr("d", line(d3.zip(item.t,item.y)))
      .attr('stroke','#5a5c69')



data[name].ys= y



})





//// MOUSE INTERACTION
  var bisect = d3.bisector(d=>d).right;

  function mousemove(event) {
      var coords = d3.pointer( event );

      var x0 = x.invert(coords[0]);
      
// FOR EACH 
pkeys.forEach(name=>{
      var i = bisect(data[name].t, x0,1);
      var yval = data[name].y[i]
      var pc = 100-100*(data[name].ys(yval)/allsize.height)
      document.getElementById(name+'val').innerText=format(yval)
      document.getElementById(name+'cat').innerText=data[name].cat[i]
      document.getElementById(name+'pc').style.width=pc +'%'
      
      
      console.log(x0,yval,i,name,pc)
  })
}
psvg.on('touchmove mousemove',mousemove);



// dahsed lines
var hline = psvg
.selectAll(".hline")
.data(caty)
.enter()

hline.append("path")

        .attr("class", "hline")
        .style('stroke',(d,i)=>color[i-1])
        .style('stroke-width',1)
        .style('opacity',.6)
        .style("stroke-dasharray", ("6, 6,3,6"))  // <== This line here!!
        .attr("d", d=>`M ${x.range()[0]+10} ${d-20} H ${x.range()[1]+10} `)
        
hline.append('text')
                     
                     .attr('text-anchor', 'left')
                     .style('stroke','none')
                     .style('fill',(d,i)=>color[i-1])
                      .attr("x", 10)
                      .attr('dy',d=>d-30)
                     .attr("y", ".35em")
                     .text((d,i)=> 'Drought category:' +i)


// These move with teh mouseover
// cicles (change data when recomputed) 
// shift names adn circles to x 
// flip names when needed


///axis
psvg.append("g")
.attr("class", "axis axis--x")
.attr(
    "transform",
    "translate(10," + (allsize.height-30) + ")"
)
.call(d3.axisBottom(x));







// leaflet
        var polygonPoints = data.geox.map((d,i)=>{return new L.LatLng(data.geoy[i],d)})
        
        var polygon = new L.Polygon(polygonPoints);
        var polymap = map.addLayer(polygon);

        // map.setView(data.center.reverse())
        map.fitBounds(polygon.getBounds(),{ padding: [50, 50] })


        
})