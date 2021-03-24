let d3 = require("d3");
let L = require("leaflet");
// center of the map

let what = 'VHI'


// Create the map
var map = L.map("lmap", {
    center: [-62.31994628906251, -24.23757312392183].reverse(),
    zoom: 4
    // dragging:false
});
var CyclOSM = L.tileLayer(
    "https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png",
    {
        maxZoom: 20,
        attribution: '<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | CEMAC '
    }
);
// map.addLayer(CyclOSM);


var w =  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 19,
    opacity:.8
});
map.addLayer(w);

var bounds = L.latLngBounds([[-50.31994628906251, -15.23757312392183].reverse(),[-70.31994628906251, -30.23757312392183].reverse()]);




var videoOverlay = L.videoOverlay( `../processed/movies/${what}.webm`, bounds, {opacity: 1})

videoOverlay.addTo(map);

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

// Usage!
sleep(500).then(() => {
    videoOverlay.getElement().play()
    console.log('dsf')
});



console.log('hil')


//     // leaflet
//     var polygonPoints = data.geox.map((d, i) => {
//         return new L.LatLng(data.geoy[i], d);
//     });
//     var polygon = new L.Polygon(polygonPoints);
//     var polymap = map.addLayer(polygon);
//     // map.setView(data.center.reverse())
//     map.fitBounds(polygon.getBounds(), { padding: [50, 50] });
// });
// 

//////////////////////////////
///// functions
/////////////////////////////



















window.onresize = function () {window.location.reload()}