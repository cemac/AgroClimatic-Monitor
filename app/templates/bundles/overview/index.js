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
    
    { opacity: 1,preserveAspectRatio:"none" }
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
            .classed('cpoly',true)
            .attr("stroke", "#AAA9AD")
            .attr('stroke-opacity',.4)
            .attr("opacity", 0.36)
            .attr("fill", "steelblue")
            .attr('fill-opacity',0)
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
                d3.selectAll('.cpoly').attr('fill-opacity',0)
                var el = d3.select(d.toElement)
                mapname.innerText=el.attr('id')
                el.attr('fill-opacity',1)
                
                // console.log(d.toElement);
            })
            // .on("mouseout", d => {
            //     d3.select(d.toElement).attr('fill-opacity',0)
            // 
            //     // console.log(d.toElement);
            // })
            .on("dblclick", d => {
                window.location.href = d3.select(d.toElement).attr('geoid')
                
            });

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
