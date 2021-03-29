// webpack --entry=./index.js --output-filename=./bundle.js --mode=production //-w


let d3 = require("d3");
let L = require("leaflet");
var currentfile=''
var last;
// const fall = require('/allfiles')

d3.json('/allfiles').then(fall=>{



const keys = Object.keys(fall)

currentfile= '/data/plotdata/'+fall[keys[0]][0]+'/'
//////////////////////
//// leaflet
//////////////////



// Create the map
var map = L.map("lmap", {
    center: [-62.31994628906251, -24.23757312392183].reverse(),
    zoom: 4
    // dragging:false
});

var w = L.tileLayer(
    //'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    "https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png",
    {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | &copy; <a href="https://carto.com/attributions">CARTO</a>|CEMAC',
        subdomains: "abcd",
        opacity: 0.8
    }
);
map.addLayer(w);
// 


// [5.2842873,-33.8689056,-35.6341164,-73.9830625]

// var bounds = L.latLngBounds([
//     [-33.8689056, 5.2842873].reverse(),
//     [-73.9830625, -35.6341164].reverse()
// ]);

var bounds = L.latLngBounds([
    [-33.8689056, 5.2842873].reverse(),
    [-73.9700625, -35.6331164].reverse()
]);


currentfile= '/data/plotdata/'+fall[keys[0]][0]+'/'
const image = L.imageOverlay(currentfile,bounds,{preserveAspectRatio:"none",})
image.addTo(map);






////////////////
///Summary
///////////////


var color = d3.interpolateViridis

 // d3.scaleOrdinal(d3.range(keys.length).map(i=>d3.interpolateViridis(i/(keys.length-1))))

const pt = d3.timeParse("%Y-%m")
const re = new RegExp('(\\d{4}-\\d{2})');
const sp = document.getElementById('sp')

var allplots = document.getElementById("summary");
var allsize = allplots.getBoundingClientRect();
const psvg = d3.select(allplots).append("svg");
psvg.attr("width", allsize.width).attr("height", allsize.height);
var x = d3.scaleTime().range([100, allsize.width - 20]).domain(d3.extent(Object.values(fall).flat().map(d=>pt(re.exec(d)[0]))))

var y = d3.scaleLinear().range([allsize.height-50,0]).domain([0,7])

    var bisect = d3.bisector(d => d).right;
    psvg.on("touchmove mousemove", mousemove);
    
    
    psvg
        .append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + (allsize.height - 30) + ")")
        .call(d3.axisBottom(x));


keys.reverse().map((d,i)=>{
    
    psvg.append('g')
   .selectAll("d")
   .data(fall[d])
   .enter()
   .append("circle")
     .classed('circle',true)
     .attr("cx", function (d) { return x(pt(re.exec(d)[0])); } )
     .attr("cy", y(i))
     .attr("r", 5)
     .style("fill", i%2==0?'#222':'#777')//color(i%2==0?.6:.8))
     .style('stroke','whitesmoke')
     .style('stroke-width',2)
     .style('stroke-opacity',.6)
     .on('mouseover',d=>{
         console.log(d.target.__data__)
         currentfile = '/data/plotdata/'+d.target.__data__+'/'
         image.setUrl(currentfile)
         
         d3.select('#imlink').attr('href',currentfile)
         
         d3.selectAll('.circle').style('stroke','whitesmoke')
         d3.select(d.target).style('stroke','red')
     })

    psvg.append("text")
    .attr("x", 0)
    .attr("y", y(i))
    .attr("dy", ".35em")
    .text(d);
    
})

















    
    function mousemove(event) {
        var coords = d3.pointer(event);
        var x0 = x.invert(coords[0]);
        var shift = `translate(${coords[0] + 30}, ${allsize.height - 30} )`;
        var mid = coords[0] > allsize.width / 2;

        d3
            .selectAll(".linetext text")
            .attr("x", coords[0] + (mid ? -20 : 20))
            .attr("text-anchor", mid ? "end" : "start");

        d3.selectAll(".vline").attr("transform", shift);

    }






//////////////////////////////
///// overlay
/////////////////////////////

function drawmap(map) {
    var bbmap = document.getElementById("lmap").getBoundingClientRect();
    var mapname = document.getElementById("mapname")

    var svg = d3
        .select(map.getPanes().overlayPane)
        .append("svg")
        .classed("leaflet-interactive", true)
        .attr("width", bbmap.width)
        .attr("height", bbmap.height);

    var g = svg.append("g").attr("class", "leaflet-zoom-hide"); //

    d3.json("/data/geojson/web_simplified.geojson").then(onmapload);

    function onmapload(topology) {
        console.log(topology);
        //var counties = topology.features; //.slice(0,1300)
        var chunks = 600;

        function projectPoint(x, y) {
            var point = map.latLngToLayerPoint(new L.LatLng(y, x));
            this.stream.point(point.x, point.y);
        }

        var transform = d3.geoTransform({ point: projectPoint }),
            path = d3.geoPath().projection(transform);

        var feature = g
            .selectAll("path")
            .data(topology.features)
            .enter()
            .append("path")
            .attr("style", "pointer-events: all;");//auto

        feature
            .attr("d", path)
            .attr("stroke", "gunmetal")
            .attr('stroke-width','2px')
            .classed('cpath',true)
            .attr("opacity", 90)
            .attr("fill", "none")
            .attr("id", t => t.properties.NOME)
            .attr("geoid", t => t.properties.GEOCODIGO)
            .attr("transform-origin", t => {
                var pt = map.latLngToLayerPoint([
                    t.properties.Cen_Y,
                    t.properties.Cen_X
                ]);
                return `${pt.x}px ${pt.y}px`;
            }) //transform-origin: 20% 40%;
            .on("mouseover", d => {
                // try{
                // last.attr('opacity',0)}
                // catch(e){}
                var last = d3.select(d.toElement)
                last.attr('opacity',.8)
                
                
                mapname.innerText=
                currentfile.split('/')[3].replace('.png','').replace('_',' ') + ' - '+
                lat.attr('id') 
                // console.log(d.toElement);
            })
            .on("click", d => {
                
                // d3.event.preventDefault(d);
                window.location.href = d3.select(d.toElement).attr('geoid')
                console.log('double',d3.select(d.toElement).attr('geoid'))
            });
        
        map.doubleClickZoom.disable()
        map.options.minZoom = 3;
        map.options.maxZoom = 8;
        map.on("zoom", resetSVG);
        resetSVG();

        // Reposition the SVG to cover the features.
        function resetSVG() {
            //console.log(path.bounds(topology), bounds, topology);

            (bounds = path.bounds(topology)), (topLeft =
                bounds[0]), (bottomRight = bounds[1]);

            svg
                .attr("width", bottomRight[0] - topLeft[0])
                .attr("height", bottomRight[1] - topLeft[1])
                .style("left", topLeft[0] + "px")
                .style("top", topLeft[1] + "px");

            g.attr(
                "transform",
                "translate(" + -topLeft[0] + "," + -topLeft[1] + ")"
            );

            feature.attr("d", path);
        }
    }

    //colour()
}

drawmap(map);

window.onresize = reload
window.onhashchange = reload

function reload() {
    window.location.reload();
};

})