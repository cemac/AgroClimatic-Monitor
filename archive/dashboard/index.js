let d3 = require("d3");
let L = require("leaflet");
// center of the map

var hash = "1100015";

const pkeys = ["VHI", "SPI"]; //, "RZSM", "spi_01", "spi_03",]// "spi_06", "spi_12","IIS3",'RZSM']
const skeys = ["spi_01", "spi_03", "spi_06", "spi_12"];
const allkeys = pkeys.concat(skeys)

const dkeys = [
    "",
    "Normal",
    "Abnormally Dry",
    "Moderate Drought",
    "Severe Drought",
    "Extreme Drought",
    "Exceptional Drought",
    ""];
    const dnames = [
        "",
        "Normal",
        "Dry",
        "Moderate",
        "Severe",
        "Extreme",
        "Exceptional",
        ""];

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
map.addLayer(CyclOSM);

// colours
const color = "003049-d62828-f77f00-fcbf49-eae2b7".split("-").map(d => "#" + d);

// date
const parseDate = function(x) {
    return x.map(y => d3.timeParse("%Y-%m")(y));
};

// PLOTTING
var allplots = document.getElementById("allplot");
var allsize = allplots.getBoundingClientRect();

console.log(allsize);
const psvg = d3.select(allplots).append("svg");
psvg.attr("width", allsize.width).attr("height", allsize.height);
const ssvg = d3.select('#spiplot').append("svg");
ssvg.attr("width", allsize.width).attr("height", allsize.height);
// lineplot
var x = d3.scaleTime().range([0, allsize.width - 20]);
var caty;

var format = d3.format(".3f");


//// MOUSE INTERACTION
var bisect = d3.bisector(d => d).right;
psvg.on("touchmove mousemove", mousemove);
ssvg.on("touchmove mousemove", mousemove);




d3.json(`../processed/muncipalities/file_${hash}.json`).then(function(data) {
    window.d = data;

    var dates = [];

    Object.values(data).forEach(d => {
        dates = dates.concat(d.x);
    });
    dates = parseDate(dates);
    x.domain(d3.extent(dates));

    window.data = data;

    // console.log(data,d3.extent(dates))

    var lscale = [];
   
        draw(data,pkeys,psvg)
        draw(data,skeys,ssvg,true)
        
        indicators(psvg,pkeys)
        indicators(ssvg,skeys)
    



    // leaflet
    var polygonPoints = data.geox.map((d, i) => {
        return new L.LatLng(data.geoy[i], d);
    });
    var polygon = new L.Polygon(polygonPoints);
    var polymap = map.addLayer(polygon);
    // map.setView(data.center.reverse())
    map.fitBounds(polygon.getBounds(), { padding: [50, 50] });
});


//////////////////////////////
///// functions
/////////////////////////////

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

    // FOR EACH
    allkeys.forEach(name => {
        var i = bisect(data[name].t, x0, 1);
        var yval = data[name].y[i];
        var measure = data[name].ys(yval);
        var pc = 100 - 100 * (measure / allsize.height);
        document.getElementById(name + "val").innerText = format(yval);

        // console.log(name,i)  
        //
        document.getElementById(name + "cat").innerText = dkeys[data[name].cat[i]+1];
        document.getElementById(name + "pc").style.width = pc + "%";
        d3
            .select("#circle" + name)
            .attr("cy", measure)
            .attr("cx", coords[0]);

        // console.log(x0,yval,i,name,pc)
    });
}





function draw (data,keys,svg,smooth=false){
    keys.forEach(name => {
        console.log(name);
        data[name].t = parseDate(data[name].x);
        var item = data[name];
        data[name].t = parseDate(item.x);

        var ylen = item.catlims.length + 2;

        caty =
            caty ||
            d3.range(ylen).map(d => allsize.height * (1 - d / ylen) - 20);
        var y = d3
            .scaleLinear()
            .range(caty)
            .domain([item.lim[0]].concat(item.catlims).concat(item.lim[1]));

        // console.log(allsize.height, y.domain(), y.range(), y(40))

        var line = d3
            .line()
            .x(d => x(d[0]))
            .y(d => y(+d[1]))
            .curve((!smooth)?d3.curveStepBefore:d3.curveCatmullRom.alpha(0.1))

        var ind = svg
            .append("g")
            .attr("class", name)
            .attr("transform", "translate(10,0)");

        ind
            .append("path")
            .attr("class", "line " + name)
            .attr("d", line(d3.zip(item.t, item.y)))
            .attr("stroke", "#5a5c69");

        data[name].ys = y;
        
    })
        
    }; 




    function indicators (svg,ckeys){
        // vert line
        
        var linearGradient = svg.append('defs')
                   .append("linearGradient")
                   // .attr('gradientUnits',"userSpaceOnUse")
                   .attr("id", "drygrad")
                    .attr("gradientTransform", "rotate(90)");

                   // linearGradient.append("stop")
                   //     .attr("offset",0)
                   //     .attr("stop-color", color[0]);

               var nc = color.length
               d3.range(1,nc+1).forEach(l=>{
                   
                   // l = nc -l
                   console.log(l,l/nc*100, color[l])
                   linearGradient.append("stop")
                       .attr("offset",((l/(nc))*100)+'%')
                       .attr("stop-color", color[nc-l]);
                   
                   
               })
        
   

        console.log(linearGradient.node())

        var vline = svg.append("g").attr("class", "vline");
        vline
            .append("path")
            .attr("d", `M -30 0 V ${-allsize.height}`)
            .attr("stroke", "white")
            .attr("stroke-width", 17);

        vline
            .append("path")
            
            .attr("d", `M -29.5 0 L -28.999991 ${-allsize.height}`)// cant be perfectly vertical for a linear gradient to work
            // .style("stroke", "black")
            .attr("stroke-width", .5)
            .attr("opacity", 0.5)
            .style('stroke',`url(#drygrad)`)
            
        vline
            .append("path")
            .attr("d", `M -31.5 0 L -30.999991 ${-allsize.height}`)// cant be perfectly vertical for a linear gradient to work
            // .style("stroke", "black")
            .attr("stroke-width", .5)
            .attr("opacity", 0.5)
            .style('stroke',`url(#drygrad)`)

        svg
            .append("g")
            .selectAll("dot")
            .data(ckeys)
            .enter()
            .append("circle")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("class", name => "line " + name)
            .attr("id", d => "circle" + d)
            .attr("r", 3)
            .attr("fill", "none")
            

        // dahsed lines
        var hline = svg.selectAll(".hline").data(caty).enter();

        hline
            .append("path")
            .attr("class", "hline")
            .style("stroke", (d, i) => color[i - 1])
            .style("stroke-width", 1)
            .style("opacity", 0.6)
            .style("stroke-dasharray", "6, 6,3,6") // <== This line here!!
            .attr(
                "d",
                d => `M ${x.range()[0] + 10} ${d - 20} H ${x.range()[1] + 10} `
            );

        hline
            .append("g")
            .attr("class", "linetext")
            .append("text")
            .attr("text-anchor", "left")
            .style("stroke", "white")
            .style("stroke-width", 0.1)
            .style("fill", (d, i) => color[i - 1])
            .attr("x", 10)
            .attr("dy", d => d +10)
            .attr("y", ".35em")
            .text((d, i) => dnames[i]);


        // These move with teh mouseover
        // cicles (change data when recomputed)
        // shift names adn circles to x
        // flip names when needed

        ///axis
        svg
            .append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(10," + (allsize.height - 30) + ")")
            .call(d3.axisBottom(x));





    }


window.onresize = function () {window.location.reload()}