let d3 = require("d3");
let L = require("leaflet");
var currentfile = ''
var last;
// const fall = require('/allfiles')
d3.json('/allfiles').then(fall => {
  const keys = Object.keys(fall)
  currentfile = '/data/plotdata/' + fall[keys[0]][0] + '/'
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
    "https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png", {
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

  currentfile = '/data/plotdata/' + fall[keys[0]][0] + '/'
  const image = L.imageOverlay(currentfile, bounds, {
    preserveAspectRatio: "none",
    opacity: .8
  })
  image.addTo(map);
  map.doubleClickZoom.disable()
  map.options.minZoom = 3;
  map.options.maxZoom = 8;
  d3.csv('/data/geojson/poly.csv/').then(e => {
    // window.d3 = d3
    // window.e = e
    // console.log(e)
    // d3.polygonHull(points);

    polygons = e.map(q => {
      var i = eval(q.poly)
      q.poly = d3.polygonHull(d3.zip(i[0], i[1]))
      return q
    })
    // window.p = polygons


    function find(ev) {
      lat = ev.latlng.lat;
      lng = ev.latlng.lng;
      console.log(lat, lng)
      for (i = 0; i < polygons.length; i++) {
        if (d3.polygonContains(polygons[i].poly, [lng, lat])) {
          console.log('found', i, polygons[i])
          break;
        }
      }
      // console.log('end search')
      var select = polygons[i]
      document.getElementById('mapname').innerText = select.id; //select.MESOREGIAO + ' - '+ select.MICROREGIA ;//+ ' - ' +
      return select

    }

    map.addEventListener('click', find);
    map.addEventListener('dblclick', (ev) => {
      console.log('DOUBLE')
      window.location.href = `/${window.location.pathname.split('/')[1]}/individual/${find(ev).GEOCODIGO}`;
    })



  })
  ////////////////
  ///Summary
  ///////////////
  // var color = d3.interpolateViridis
  // d3.scaleOrdinal(d3.range(keys.length).map(i=>d3.interpolateViridis(i/(keys.length-1))))
  const pt = d3.timeParse("%Y-%m")
  const re = new RegExp('(\\d{4}-\\d{2})');
  const sp = document.getElementById('sp')
  var allplots = document.getElementById("summary");
  var allsize = allplots.getBoundingClientRect();
  const psvg = d3.select(allplots).append("svg");
  psvg.attr("width", allsize.width).attr("height", allsize.height);
  var x = d3.scaleTime().range([100, allsize.width - 20]).domain(d3.extent(Object.values(fall).flat().map(d => pt(re.exec(d)[0]))))
  var y = d3.scaleLinear().range([allsize.height - 50, 0]).domain([0, 7])
  var bisect = d3.bisector(d => d).right;
  // psvg.on("touchmove mousemove", mousemove);
  psvg
    .append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + (allsize.height - 30) + ")")
    .call(d3.axisBottom(x));


  keys.reverse().map((d, i) => {

    psvg.append('g')
      .selectAll("d")
      .data(fall[d])
      .enter()
      .append("circle")
      .classed('circle', true)
      .attr("cx", function(d) {
        return x(pt(re.exec(d)[0]));
      })
      .attr("cy", y(i))
      .attr("r", 6)
      .style("fill", i % 2 == 0 ? d3.color('whitesmoke').darker(.2) : '#999') //color(i%2==0?.6:.8))
      .style('stroke', '#222')
      .style('stroke-width', 3)
      .style('stroke-opacity', .6)
      .on('click', d => {
        console.log(d.target.__data__)
        currentfile = '/data/plotdata/' + d.target.__data__ + '/'
        image.setUrl(currentfile)

        d3.select('#imlink').attr('href', currentfile)

        document.getElementById('sp').innerText = d.target.__data__.replace('.png', '').replace('_', ' ')

        d3.selectAll('.circle').style('stroke', 'whitesmoke')
        d3.select(d.target).style('stroke', 'red')
      })



    psvg.append("text")
      .attr("x", 0)
      .attr("y", y(i))
      .attr("dy", ".35em")
      .text(d.toUpperCase().replace('_', ' ').replace('0', '').replace('IIS3', 'IDI'));

  })

  window.onresize = reload
  window.onhashchange = reload

  function reload() {
    window.location.reload();
  };

})
