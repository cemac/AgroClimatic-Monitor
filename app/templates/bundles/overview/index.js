// webpack --entry=./index.js --output-filename=./bundle.js --mode=production //-w


let d3 = require("d3");
let L = require("leaflet");


let what =  window.location.pathname.split('/overview/')[1] || 'RZSM'
//window.location.hash.replace("#", "") || "VHI";

if (what === "undefined") {
    what = "VHI";
}

// Create the map
var map = L.map("lmap", {
    center: [-62.31994628906251, -24.23757312392183].reverse(),
    zoom: 4,


    // dragging:false
});

map.doubleClickZoom.disable()
map.options.minZoom = 3;
map.options.maxZoom = 8;    

var w = L.tileLayer(
    // 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    "https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png",
    {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | &copy; <a href="https://carto.com/attributions">CARTO</a>|CEMAC',
        subdomains: "abcd",
        opacity: 1
    }
);
map.addLayer(w);


// [-33.8689056, 5.2842873].reverse(),
// [-73.9830625, -35.6341164].reverse()

var bounds = L.latLngBounds([
    [7, -33],
    [-36, -74]//y,x
]);

console.log(bounds)
var videoOverlay = L.videoOverlay(
    `/data/movies/${what}.webm`,
    bounds,
    
    { opacity: .8,preserveAspectRatio:"none" }
);

videoOverlay.addTo(map);

function sleep(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

// Usage!
sleep(500).then(() => {
    videoOverlay.getElement().play();
});

videoOverlay.on("load", function() {
    var MyPauseControl = L.Control.extend({
        onAdd: function() {
            var button = L.DomUtil.create("button");
            button.innerHTML = "⏸";
            L.DomEvent.on(button, "click", function() {
                videoOverlay.getElement().pause();
            });
            return button;
        }
    });
    var MyPlayControl = L.Control.extend({
        onAdd: function() {
            var button = L.DomUtil.create("button");
            button.innerHTML = "▶️";
            L.DomEvent.on(button, "click", function() {
                videoOverlay.getElement().play();
            });
            return button;
        }
    });

    var pauseControl = new MyPauseControl().addTo(map);
    var playControl = new MyPlayControl().addTo(map);
});

//////////////////////////////
///// overlay
/////////////////////////////

// function drawmap(map) {
//     var bbmap = document.getElementById("lmap").getBoundingClientRect();
//     var mapname = document.getElementById("mapname")
// 
//     var svg = d3
//         .select(map.getPanes().overlayPane)
//         .append("svg")
//         .classed("leaflet-interactive", true)
//         .attr("width", bbmap.width)
//         .attr("height", bbmap.height);
// 
//     var g = svg.append("g").attr("class", "leaflet-zoom-hide"); //
// 
// 
// 
//     d3.json("/data/geojson/web_simplified.geojson").then(onmapload);
// 
// 
// 
//     //colour()
// }
//drawmap(map);


d3.csv('/data/geojson/poly.csv/').then(e=>{
    // window.d3 = d3
    // window.e = e
    // console.log(e)
    // d3.polygonHull(points);
    
    polygons = e.map(q=>{
        var i = eval(q.poly)
        q.poly = d3.polygonHull(d3.zip(i[0],i[1]))
        return q    
    })
    // window.p = polygons

    
    function find(ev) {
       lat = ev.latlng.lat;
       lng = ev.latlng.lng;
       console.log(lat,lng)
       for (i = 0; i < polygons.length; i++) {
       if (d3.polygonContains(polygons[i].poly,    [lng,lat]) ) { 
              console.log('found',i,polygons[i])
              break; }
        }
        // console.log('end search')
        var select = polygons[i]
        document.getElementById('mapname').innerText=select.MESOREGIAO + ' - '+ select.MICROREGIA + ' - ' + select.id;
        return select
       
    }

    map.addEventListener('click', find);
    map.addEventListener('dblclick', (ev)=>{
        console.log('DOUBLE')
        window.location.href = `/${window.location.pathname.split('/')[1]}/individual/${find(ev).GEOCODIGO}`
        ;})
    
    
    
})

window.onresize = reload
window.onhashchange = reload

function reload() {
    window.location.reload();
};
