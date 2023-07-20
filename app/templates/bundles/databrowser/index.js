let d3 = require("d3");
let L = require("leaflet");
var currentfile = ''
var last;
// const fall = require('/allfiles')
d3.json('/allfiles').then(fall => {
  const keys = Object.keys(fall)

  // cemaccam: select instead latest entry as default
  // currentfile = '/data/plotdata/' + fall[keys[0]][0] + '/'
  // currentfile = '/data/plotdata/' + fall[keys[0]][fall[keys[0]].length-1] + '/'
  //////////////////////
  //// leaflet
  //////////////////
  // Create the map
  var mymap = L.map("lmap", {
    center: [-62.31994628906251, -24.23757312392183].reverse(),
    zoom: 4
    // dragging:false
  });

  // added crossOrigin anonymous use-credentials null/false
  var w = L.tileLayer(
    //'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    //opacity: 0.9,//
    'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | &copy; <a href="https://carto.com/attributions">CARTO</a>|CEMAC',
      subdomains: "abcd",
      crossOrigin: "anonymous"
    }
  );
  mymap.addLayer(w);
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

  // load first image in first allfiles.json entry by default
  // cemaccam: select instead latest entry as default
  currentfile = '/data/plotdata/' + fall[keys[0]][fall[keys[0]].length - 1] + '/'  // cemaccam: duplicate of line 11
  const image = L.imageOverlay(currentfile, bounds, {
    preserveAspectRatio: "none",
    opacity: .8
  })
  image.addTo(mymap);
  /*
  add borders
  currentfile2 = '/data/plotdata/br-02.png'
  const image2 = L.imageOverlay(currentfile2, bounds, {
    preserveAspectRatio: "none",
    opacity: .9
  })
  image2.addTo(mymap);
  */
  mymap.doubleClickZoom.disable()
  mymap.options.minZoom = 3;
  mymap.options.maxZoom = 8;

  d3.csv('/data/geojson/poly.csv/').then(e => {
    // window.d3 = d3
    // window.e = e
    // console.log(e)
    // d3.polygonHull(points);
    // Create array of polygons corresponding to regions
    polygons = e.map(q => {
      var i = eval(q.poly)  // i will contain an array of the polygon points
      q.poly = d3.polygonHull(d3.zip(i[0], i[1]))  // create polygon from the x array (i[0]) & y array (i[i])
      return q
    })
    window.p = polygons  // cemaccam: uncommented, to confirm what it contains.


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

    // respond to single and double clicks on map
    mymap.addEventListener('click', find);
    mymap.addEventListener('dblclick', (ev) => {
      console.log('DOUBLE')
      window.location.href = `/${window.location.pathname.split('/')[1]}/individual/${find(ev).GEOCODIGO}`;
    })

  })
  ////////////////
  ///Summary
  ///////////////
  // var color = d3.interpolateViridis
  // d3.scaleOrdinal(d3.range(keys.length).map(i=>d3.interpolateViridis(i/(keys.length-1))))
  const pt = d3.timeParse("%Y-%m")  // Year-month time parse function
  const re = new RegExp('(\\d{4}-\\d{2})');  // match 4 digits followed by dash, then 2 digits.
  const sp = document.getElementById('sp')  // summary title
  var allplots = document.getElementById("summary");  // summary plot
  var allsize = allplots.getBoundingClientRect();
  const psvg = d3.select(allplots).append("svg");  // set up vector graphic
  psvg.attr("width", allsize.width).attr("height", allsize.height);
  
  // cemaccam: TODO: change so that, by default, shows only months of most
  // recent year:
  // cemaccam: find latest year.
  // first, collect all unique dates (cf https://stackoverflow.com/a/44906207)
  var allDates = Object.values(fall).flat().map(d => pt(re.exec(d)[0])).filter(
    (date, index, self) => self.findIndex(value => value.getTime() === date.getTime()) === index
    );
  // all unique years
  var years = [...new Set(allDates.map(d => d.getFullYear()))];

  // cemaccam: populate year selector drop-down, with default being latest
  var thisYear = d3.max(years)
  var yearSelector = document.getElementById("year")
  var option
  years.reverse().map(d => {
    option = document.createElement('option')
    option.text = d
    option.value = d
    yearSelector.add(option)
  })
  yearSelector.selectedIndex = 0
  yearSelector.onchange = function() {
    thisYear = yearSelector.value

    // console.log(thisYear)
  }
  
  // function datesInYear(dateArray, year) {
  //   return dateArray.filter(d => d.getFullYear() == year)
  // }
  
  // thisYearDates = datesInYear(allDates, lastYear)
  // console.log(thisYearDates)
  // console.log(keys[0] + ' : ' + fall[keys[0]].filter(f => pt(re.exec(f)[0]).getFullYear() == thisYear))

  // cemaccam: get subsets of fall corresponding to these dates
  var thisYearDates = allDates.filter(d => d.getFullYear() == thisYear)

  // Then find first & last months listed for latest year.
  // Then set time scale according to [min yyyymm, max yyyymm].
  // Replace fall with a dictionary whose values cover only the desired range.
  // var x = d3.scaleTime().range([100, allsize.width - 20]).domain(d3.extent(Object.values(fall).flat().map(d => pt(re.exec(d)[0]))))  // on each element of allfiles.json, run time parser on first (only) regex match, then set timescale to match the min & max of these yyyymm time-points. x is a function converting timepoints to x-coordinates on screen.
  // var x = d3.scaleTime().range([100, allsize.width - 20]).domain(d3.extent(thisYearDates))  // on each element of allfiles.json, run time parser on first (only) regex match, then set timescale to match the min & max of these yyyymm time-points. x is a function converting timepoints to x-coordinates on screen.
  var x = d3.scaleTime().range([100, allsize.width - 20]).domain([new Date(`${thisYear}-01-01`), new Date(`${thisYear}-12-31`)]).nice()  // scale months of a year to screen coordinates
  var y = d3.scaleLinear().range([allsize.height - 50, 0]).domain([0, 7])  // 7 types of plot = 7 keys in allfiles.json
  // var bisect = d3.bisector(d => d).right;  // cemaccam: bisect is never used
  // psvg.on("touchmove mousemove", mousemove);
  psvg
    .append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + (allsize.height - 30) + ")")
    .call(d3.axisBottom(x));


  // for each key in allfiles.json (plot type), add a row of month markers,
  // adding in reverse order so first appears at top.

  // array.map creates a new array populated with results of calling provided
  // function on every element of original array (works as a lambda function).
  // d here is the relevant key; i is the corresponding index.
  
  // cemaccam: TODO: should be adjusted to correspond to timeframe
  // selected (default = latest year's months).
  // Easiest way to do this is to replace fall with a subarray matching the
  // desired year.

  keys.reverse().map((d, i) => {
    
    // 'g' is a group element.
    // Not sure what selectAll("d") is doing. It seems it's essentially allowing
    // all subsequent methods in the chain to be applied to a virtual "d" 
    // element.
    // fall[d] is the file list associated with key d.
    // d.target.__data__ is the specific value in the fall[d] array, i.e.
    // file name.

    // cemaccam: TODO: tidy up ticks to better fit (up to) 1 year of data.
    psvg.append('g')
      .selectAll("d") // create an empty selection
      // .data(fall[d])  // fill the selected virtual "d" elements with selected data
      .data(fall[d].filter(f => pt(re.exec(f)[0]).getFullYear() == thisYear))  // fill the selected virtual "d" elements with selected data
      .enter()  // contains elements needing to be added to contain data
      .append("circle")
      .classed('circle', true)
      .attr("cx", function(d) {
        return x(pt(re.exec(d)[0]));
      })  // d here is the value from fall[d]
      .attr("cy", y(i))
      .attr("r", 6)
      .style("fill", i % 2 == 0 ? d3.color('whitesmoke').darker(.2) : '#999') //color(i%2==0?.6:.8))  // different shading for every 2nd line
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


    // Give caption at start of row
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

/*
  NOTE ON Easy Print

  The code below adds a save image button to the leadlet map

  I've had to dump the whole of easy print code into the code here in order to load
  in the code because it rewrites leaflets L function. so L would require two
  modules and I couldn't find a smoother way to to get this to work

  Code from
  https://github.com/rowanwins/leaflet-easyPrint
*/
var domtoimage = require('dom-to-image');
var fileSaver = require('file-saver');

L.Control.EasyPrint = L.Control.extend({
  options: {
    title: 'Print map',
    position: 'topleft',
    sizeModes: ['Current'],
    filename: 'map',
    exportOnly: false,
    hidden: false,
    tileWait: 500,
    hideControlContainer: true,
    hideClasses: [],
    customWindowTitle: window.document.title,
    spinnerBgCOlor: '#0DC5C1',
    customSpinnerClass: 'epLoader',
    defaultSizeTitles: {
      Current: 'Current Size',
      A4Landscape: 'A4 Landscape',
      A4Portrait: 'A4 Portrait'
    }
  },

  onAdd: function () {
    this.mapContainer = this._map.getContainer();
    this.options.sizeModes = this.options.sizeModes.map(function (sizeMode) {
      if (sizeMode === 'Current') {
        return {
          name: this.options.defaultSizeTitles.Current,
          className: 'CurrentSize'
        }
      }
      if (sizeMode === 'A4Landscape') {
        return {
          height: this._a4PageSize.height,
          width: this._a4PageSize.width,
          name: this.options.defaultSizeTitles.A4Landscape,
          className: 'A4Landscape page'
        }
      }
      if (sizeMode === 'A4Portrait') {
        return {
          height: this._a4PageSize.width,
          width: this._a4PageSize.height,
          name: this.options.defaultSizeTitles.A4Portrait,
          className: 'A4Portrait page'
        }
      };
      return sizeMode;
    }, this);

    var container = L.DomUtil.create('div', 'leaflet-control-easyPrint leaflet-bar leaflet-control');
    if (!this.options.hidden) {
      this._addCss();

      L.DomEvent.addListener(container, 'mouseover', this._togglePageSizeButtons, this);
      L.DomEvent.addListener(container, 'mouseout', this._togglePageSizeButtons, this);

      var btnClass = 'leaflet-control-easyPrint-button'
      if (this.options.exportOnly) btnClass = btnClass + '-export'

      this.link = L.DomUtil.create('a', btnClass, container);
      this.link.id = "leafletEasyPrint";
      this.link.title = this.options.title;
      this.holder = L.DomUtil.create('ul', 'easyPrintHolder', container);

      this.options.sizeModes.forEach(function (sizeMode) {
        var btn = L.DomUtil.create('li', 'easyPrintSizeMode', this.holder);
        btn.title = sizeMode.name;
        var link = L.DomUtil.create('a', sizeMode.className, btn);
        L.DomEvent.addListener(btn, 'click', this.printMap, this);
      }, this);

      L.DomEvent.disableClickPropagation(container);
    }
    return container;
  },

  printMap: function (event, filename) {
    if (filename) {
      this.options.filename = filename
    }
    if (!this.options.exportOnly) {
      this._page = window.open("", "_blank", 'toolbar=no,status=no,menubar=no,scrollbars=no,resizable=no,left=10, top=10, width=200, height=250, visible=none');
      this._page.document.write(this._createSpinner(this.options.customWindowTitle, this.options.customSpinnerClass, this.options.spinnerBgCOlor));
    }
    this.originalState = {
      mapWidth: this.mapContainer.style.width,
      widthWasAuto: false,
      widthWasPercentage: false,
      mapHeight: this.mapContainer.style.height,
      zoom: this._map.getZoom(),
      center: this._map.getCenter()
    };
    if (this.originalState.mapWidth === 'auto') {
      this.originalState.mapWidth = this._map.getSize().x  + 'px'
      this.originalState.widthWasAuto = true
    } else if (this.originalState.mapWidth.includes('%')) {
      this.originalState.percentageWidth = this.originalState.mapWidth
      this.originalState.widthWasPercentage = true
      this.originalState.mapWidth = this._map.getSize().x  + 'px'
    }
    this._map.fire("easyPrint-start", { event: event });
    if (!this.options.hidden) {
      this._togglePageSizeButtons({type: null});
    }
    if (this.options.hideControlContainer) {
      this._toggleControls();
    }
    if (this.options.hideClasses) {
      this._toggleClasses(this.options.hideClasses);
    }
    var sizeMode = typeof event !== 'string' ? event.target.className : event;
    if (sizeMode === 'CurrentSize') {
      return this._printOpertion(sizeMode);
    }
    this.outerContainer = this._createOuterContainer(this.mapContainer)
    if (this.originalState.widthWasAuto) {
      this.outerContainer.style.width = this.originalState.mapWidth
    }
    this._createImagePlaceholder(sizeMode)
  },

  _createImagePlaceholder: function (sizeMode) {
    var plugin = this;
    domtoimage.toPng(this.mapContainer, {
        width: parseInt(this.originalState.mapWidth.replace('px')),
        height: parseInt(this.originalState.mapHeight.replace('px'))
      })
      .then(function (dataUrl) {
        plugin.blankDiv = document.createElement("div");
        var blankDiv = plugin.blankDiv;
        plugin.outerContainer.parentElement.insertBefore(blankDiv, plugin.outerContainer);
        blankDiv.className = 'epHolder';
        blankDiv.style.backgroundImage = 'url("' + dataUrl + '")';
        blankDiv.style.position = 'absolute';
        blankDiv.style.zIndex = 1011;
        blankDiv.style.display = 'initial';
        blankDiv.style.width = plugin.originalState.mapWidth;
        blankDiv.style.height = plugin.originalState.mapHeight;
        plugin._resizeAndPrintMap(sizeMode);
      })
      .catch(function (error) {
          console.error('oops, something went wrong!', error);
      });
  },

  _resizeAndPrintMap: function (sizeMode) {
    this.outerContainer.style.opacity = 0;
    var pageSize = this.options.sizeModes.filter(function (item) {
      return item.className.indexOf(sizeMode) > -1;
    });
    pageSize = pageSize[0]
    this.mapContainer.style.width = pageSize.width + 'px';
    this.mapContainer.style.height = pageSize.height + 'px';
    if (this.mapContainer.style.width > this.mapContainer.style.height) {
      this.orientation = 'portrait';
    } else {
      this.orientation = 'landscape';
    }
    this._map.setView(this.originalState.center);
    this._map.setZoom(this.originalState.zoom);
    this._map.invalidateSize();
    if (this.options.tileLayer) {
      this._pausePrint(sizeMode)
    } else {
      this._printOpertion(sizeMode)
    }
  },

  _pausePrint: function (sizeMode) {
    var plugin = this
    var loadingTest = setInterval(function () {
      if(!plugin.options.tileLayer.isLoading()) {
        clearInterval(loadingTest);
        plugin._printOpertion(sizeMode)
      }
    }, plugin.options.tileWait);
  },

  _printOpertion: function (sizemode) {
    var plugin = this;
    var widthForExport = this.mapContainer.style.width
    if (this.originalState.widthWasAuto && sizemode === 'CurrentSize' || this.originalState.widthWasPercentage && sizemode === 'CurrentSize') {
      widthForExport = this.originalState.mapWidth
    }
    domtoimage.toPng(plugin.mapContainer, {
        width: parseInt(widthForExport),
        height: parseInt(plugin.mapContainer.style.height.replace('px'))
      })
      .then(function (dataUrl) {
          var blob = plugin._dataURItoBlob(dataUrl);
          if (plugin.options.exportOnly) {
            fileSaver.saveAs(blob, plugin.options.filename + '.png');
          } else {
            plugin._sendToBrowserPrint(dataUrl, plugin.orientation);
          }
          plugin._toggleControls(true);
          plugin._toggleClasses(plugin.options.hideClasses, true);

          if (plugin.outerContainer) {
            if (plugin.originalState.widthWasAuto) {
              plugin.mapContainer.style.width = 'auto'
            } else if (plugin.originalState.widthWasPercentage) {
              plugin.mapContainer.style.width = plugin.originalState.percentageWidth
            }
            else {
              plugin.mapContainer.style.width = plugin.originalState.mapWidth;
            }
            plugin.mapContainer.style.height = plugin.originalState.mapHeight;
            plugin._removeOuterContainer(plugin.mapContainer, plugin.outerContainer, plugin.blankDiv)
            plugin._map.invalidateSize();
            plugin._map.setView(plugin.originalState.center);
            plugin._map.setZoom(plugin.originalState.zoom);
          }
          plugin._map.fire("easyPrint-finished");
      })
      .catch(function (error) {
          console.error('Print operation failed', error);
      });
  },

  _sendToBrowserPrint: function (img, orientation) {
    this._page.resizeTo(600, 800);
    var pageContent = this._createNewWindow(img, orientation, this)
    this._page.document.body.innerHTML = ''
    this._page.document.write(pageContent);
    this._page.document.close();
  },

  _createSpinner: function (title, spinnerClass, spinnerColor) {
    return `<html><head><title>`+ title + `</title></head><body><style>
      body{
        background: ` + spinnerColor + `;
      }
      .epLoader,
      .epLoader:before,
      .epLoader:after {
        border-radius: 50%;
      }
      .epLoader {
        color: #ffffff;
        font-size: 11px;
        text-indent: -99999em;
        margin: 55px auto;
        position: relative;
        width: 10em;
        height: 10em;
        box-shadow: inset 0 0 0 1em;
        -webkit-transform: translateZ(0);
        -ms-transform: translateZ(0);
        transform: translateZ(0);
      }
      .epLoader:before,
      .epLoader:after {
        position: absolute;
        content: '';
      }
      .epLoader:before {
        width: 5.2em;
        height: 10.2em;
        background: #0dc5c1;
        border-radius: 10.2em 0 0 10.2em;
        top: -0.1em;
        left: -0.1em;
        -webkit-transform-origin: 5.2em 5.1em;
        transform-origin: 5.2em 5.1em;
        -webkit-animation: load2 2s infinite ease 1.5s;
        animation: load2 2s infinite ease 1.5s;
      }
      .epLoader:after {
        width: 5.2em;
        height: 10.2em;
        background: #0dc5c1;
        border-radius: 0 10.2em 10.2em 0;
        top: -0.1em;
        left: 5.1em;
        -webkit-transform-origin: 0px 5.1em;
        transform-origin: 0px 5.1em;
        -webkit-animation: load2 2s infinite ease;
        animation: load2 2s infinite ease;
      }
      @-webkit-keyframes load2 {
        0% {
          -webkit-transform: rotate(0deg);
          transform: rotate(0deg);
        }
        100% {
          -webkit-transform: rotate(360deg);
          transform: rotate(360deg);
        }
      }
      @keyframes load2 {
        0% {
          -webkit-transform: rotate(0deg);
          transform: rotate(0deg);
        }
        100% {
          -webkit-transform: rotate(360deg);
          transform: rotate(360deg);
        }
      }
      </style>
    <div class="`+spinnerClass+`">Loading...</div></body></html>`;
  },

  _createNewWindow: function (img, orientation, plugin) {
    return `<html><head>
        <style>@media print {
          img { max-width: 98%!important; max-height: 98%!important; }
          @page { size: ` + orientation + `;}}
        </style>
        <script>function step1(){
        setTimeout('step2()', 10);}
        function step2(){window.print();window.close()}
        </script></head><body onload='step1()'>
        <img src="` + img + `" style="display:block; margin:auto;"></body></html>`;
  },

  _createOuterContainer: function (mapDiv) {
    var outerContainer = document.createElement('div');
    mapDiv.parentNode.insertBefore(outerContainer, mapDiv);
    mapDiv.parentNode.removeChild(mapDiv);
    outerContainer.appendChild(mapDiv);
    outerContainer.style.width = mapDiv.style.width;
    outerContainer.style.height = mapDiv.style.height;
    outerContainer.style.display = 'inline-block'
    outerContainer.style.overflow = 'hidden';
    return outerContainer;
  },

  _removeOuterContainer: function (mapDiv, outerContainer, blankDiv) {
    if (outerContainer.parentNode) {
      outerContainer.parentNode.insertBefore(mapDiv, outerContainer);
      outerContainer.parentNode.removeChild(blankDiv);
      outerContainer.parentNode.removeChild(outerContainer);
    }
  },

  _addCss: function () {
    var css = document.createElement("style");
    css.type = "text/css";
    css.innerHTML = `.leaflet-control-easyPrint-button {
      background-image: url(data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTYuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjE2cHgiIGhlaWdodD0iMTZweCIgdmlld0JveD0iMCAwIDUxMiA1MTIiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDUxMiA1MTI7IiB4bWw6c3BhY2U9InByZXNlcnZlIj4KPGc+Cgk8cGF0aCBkPSJNMTI4LDMyaDI1NnY2NEgxMjhWMzJ6IE00ODAsMTI4SDMyYy0xNy42LDAtMzIsMTQuNC0zMiwzMnYxNjBjMCwxNy42LDE0LjM5OCwzMiwzMiwzMmg5NnYxMjhoMjU2VjM1Mmg5NiAgIGMxNy42LDAsMzItMTQuNCwzMi0zMlYxNjBDNTEyLDE0Mi40LDQ5Ny42LDEyOCw0ODAsMTI4eiBNMzUyLDQ0OEgxNjBWMjg4aDE5MlY0NDh6IE00ODcuMTk5LDE3NmMwLDEyLjgxMy0xMC4zODcsMjMuMi0yMy4xOTcsMjMuMiAgIGMtMTIuODEyLDAtMjMuMjAxLTEwLjM4Ny0yMy4yMDEtMjMuMnMxMC4zODktMjMuMiwyMy4xOTktMjMuMkM0NzYuODE0LDE1Mi44LDQ4Ny4xOTksMTYzLjE4Nyw0ODcuMTk5LDE3NnoiIGZpbGw9IiMwMDAwMDAiLz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8L3N2Zz4K);
      background-size: 16px 16px;
      cursor: pointer;
    }
    .leaflet-control-easyPrint-button-export {
      background-image: url(data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTYuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjE2cHgiIGhlaWdodD0iMTZweCIgdmlld0JveD0iMCAwIDQzMy41IDQzMy41IiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCA0MzMuNSA0MzMuNTsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8Zz4KCTxnIGlkPSJmaWxlLWRvd25sb2FkIj4KCQk8cGF0aCBkPSJNMzk1LjI1LDE1M2gtMTAyVjBoLTE1M3YxNTNoLTEwMmwxNzguNSwxNzguNUwzOTUuMjUsMTUzeiBNMzguMjUsMzgyLjV2NTFoMzU3di01MUgzOC4yNXoiIGZpbGw9IiMwMDAwMDAiLz4KCTwvZz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8L3N2Zz4K);
      background-size: 16px 16px;
      cursor: pointer;
    }
    .easyPrintHolder a {
      background-size: 16px 16px;
      cursor: pointer;
    }
    .easyPrintHolder .CurrentSize{
      background-image: url(data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMTZweCIgdmVyc2lvbj0iMS4xIiBoZWlnaHQ9IjE2cHgiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgNjQgNjQiPgogIDxnPgogICAgPGcgZmlsbD0iIzFEMUQxQiI+CiAgICAgIDxwYXRoIGQ9Ik0yNS4yNTUsMzUuOTA1TDQuMDE2LDU3LjE0NVY0Ni41OWMwLTEuMTA4LTAuODk3LTIuMDA4LTIuMDA4LTIuMDA4QzAuODk4LDQ0LjU4MiwwLDQ1LjQ4MSwwLDQ2LjU5djE1LjQwMiAgICBjMCwwLjI2MSwwLjA1MywwLjUyMSwwLjE1NSwwLjc2N2MwLjIwMywwLjQ5MiwwLjU5NCwwLjg4MiwxLjA4NiwxLjA4N0MxLjQ4Niw2My45NDcsMS43NDcsNjQsMi4wMDgsNjRoMTUuNDAzICAgIGMxLjEwOSwwLDIuMDA4LTAuODk4LDIuMDA4LTIuMDA4cy0wLjg5OC0yLjAwOC0yLjAwOC0yLjAwOEg2Ljg1NWwyMS4yMzgtMjEuMjRjMC43ODQtMC43ODQsMC43ODQtMi4wNTUsMC0yLjgzOSAgICBTMjYuMDM5LDM1LjEyMSwyNS4yNTUsMzUuOTA1eiIgZmlsbD0iIzAwMDAwMCIvPgogICAgICA8cGF0aCBkPSJtNjMuODQ1LDEuMjQxYy0wLjIwMy0wLjQ5MS0wLjU5NC0wLjg4Mi0xLjA4Ni0xLjA4Ny0wLjI0NS0wLjEwMS0wLjUwNi0wLjE1NC0wLjc2Ny0wLjE1NGgtMTUuNDAzYy0xLjEwOSwwLTIuMDA4LDAuODk4LTIuMDA4LDIuMDA4czAuODk4LDIuMDA4IDIuMDA4LDIuMDA4aDEwLjU1NmwtMjEuMjM4LDIxLjI0Yy0wLjc4NCwwLjc4NC0wLjc4NCwyLjA1NSAwLDIuODM5IDAuMzkyLDAuMzkyIDAuOTA2LDAuNTg5IDEuNDIsMC41ODlzMS4wMjctMC4xOTcgMS40MTktMC41ODlsMjEuMjM4LTIxLjI0djEwLjU1NWMwLDEuMTA4IDAuODk3LDIuMDA4IDIuMDA4LDIuMDA4IDEuMTA5LDAgMi4wMDgtMC44OTkgMi4wMDgtMi4wMDh2LTE1LjQwMmMwLTAuMjYxLTAuMDUzLTAuNTIyLTAuMTU1LTAuNzY3eiIgZmlsbD0iIzAwMDAwMCIvPgogICAgPC9nPgogIDwvZz4KPC9zdmc+Cg==)
    }
    .easyPrintHolder .page {
      background-image: url(data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTguMS4xLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4PSIwcHgiIHk9IjBweCIgdmlld0JveD0iMCAwIDQ0NC44MzMgNDQ0LjgzMyIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgNDQ0LjgzMyA0NDQuODMzOyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgd2lkdGg9IjUxMnB4IiBoZWlnaHQ9IjUxMnB4Ij4KPGc+Cgk8Zz4KCQk8cGF0aCBkPSJNNTUuMjUsNDQ0LjgzM2gzMzQuMzMzYzkuMzUsMCwxNy03LjY1LDE3LTE3VjEzOS4xMTdjMC00LjgxNy0xLjk4My05LjM1LTUuMzgzLTEyLjQ2N0wyNjkuNzMzLDQuNTMzICAgIEMyNjYuNjE3LDEuNywyNjIuMzY3LDAsMjU4LjExNywwSDU1LjI1Yy05LjM1LDAtMTcsNy42NS0xNywxN3Y0MTAuODMzQzM4LjI1LDQzNy4xODMsNDUuOSw0NDQuODMzLDU1LjI1LDQ0NC44MzN6ICAgICBNMzcyLjU4MywxNDYuNDgzdjAuODVIMjU2LjQxN3YtMTA4LjhMMzcyLjU4MywxNDYuNDgzeiBNNzIuMjUsMzRoMTUwLjE2N3YxMzAuMzMzYzAsOS4zNSw3LjY1LDE3LDE3LDE3aDEzMy4xNjd2MjI5LjVINzIuMjVWMzR6ICAgICIgZmlsbD0iIzAwMDAwMCIvPgoJPC9nPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+Cjwvc3ZnPgo=);
    }
    .easyPrintHolder .A4Landscape {
      transform: rotate(-90deg);
    }
    .leaflet-control-easyPrint-button{
      display: inline-block;
    }
    .easyPrintHolder{
      margin-top:-31px;
      margin-bottom: -5px;
      margin-left: 30px;
      padding-left: 0px;
      display: none;
    }
    .easyPrintSizeMode {
      display: inline-block;
    }
    .easyPrintHolder .easyPrintSizeMode a {
      border-radius: 0px;
    }
    .easyPrintHolder .easyPrintSizeMode:last-child a{
      border-top-right-radius: 2px;
      border-bottom-right-radius: 2px;
      margin-left: -1px;
    }
    .easyPrintPortrait:hover, .easyPrintLandscape:hover{
      background-color: #757570;
      cursor: pointer;
    }`;
    document.body.appendChild(css);
  },

  _dataURItoBlob: function (dataURI) {
    var byteString = atob(dataURI.split(',')[1]);
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    var ab = new ArrayBuffer(byteString.length);
    var dw = new DataView(ab);
    for(var i = 0; i < byteString.length; i++) {
        dw.setUint8(i, byteString.charCodeAt(i));
    }
    return new Blob([ab], {type: mimeString});
  },

  _togglePageSizeButtons: function (e) {
    var holderStyle = this.holder.style
    var linkStyle = this.link.style
    if (e.type === 'mouseover') {
      holderStyle.display = 'block';
      linkStyle.borderTopRightRadius = '0'
      linkStyle.borderBottomRightRadius = '0'
    } else {
      holderStyle.display = 'none';
      linkStyle.borderTopRightRadius = '2px'
      linkStyle.borderBottomRightRadius = '2px'
    }
  },

  _toggleControls: function (show) {
    var controlContainer = document.getElementsByClassName("leaflet-control-container")[0];
    if (show) return controlContainer.style.display = 'block';
    controlContainer.style.display = 'none';
  },
  _toggleClasses: function (classes, show) {
    classes.forEach(function (className) {
      var div = document.getElementsByClassName(className)[0];
      if (show) return div.style.display = 'block';
      div.style.display = 'none';
    });
  },

  _a4PageSize: {
    height: 715,
    width: 1045
  }

});

L.easyPrint = function(options) {
  return new L.Control.EasyPrint(options);
};

L.easyPrint({
      		tileLayer: w,
      		sizeModes: ['Current'],
      		filename: 'AgroClimaticMontitor',
      		exportOnly: true,
          position: 'topright'
		}).addTo(mymap);

})
