var d3 = require("d3");

function drawmap(map) {
    var svg = d3
        .select(map.getPanes().overlayPane)
        .append("svg")
        .classed('leaflet-interactive',true)
        .attr("width", width)
        .attr("height", height);

    var g = svg.append("g").attr("class", "leaflet-zoom-hide"); //

    d3.json("../data/web_simplified.geojson").then(onmapload);

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
            .append("path");

        feature
            .attr("d", path)
            .attr("stroke", "whitesmoke")
            .attr("fill-opacity", 0.6)
            .attr("fill", "none")
            .attr("id", t => t.properties.NOME)
            .attr('transform-origin',t=>{var pt = map.latLngToLayerPoint([t.properties.Cen_Y,t.properties.Cen_X]);
                return `${pt.x}px ${pt.y}px`})//transform-origin: 20% 40%;
            .on('mouseover',d=>{d3.select(event.path[0]).attr( 'fill', 'green' )})


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

        //
        // counties.forEach(t => {
        //
        //
        //     var pts = t.geometry.coordinates[0].map(c => {
        //         var px = map.latLngToContainerPoint(c.map(parseFloat).reverse());
        //         // console.log(x)
        //         return [px.x,px.y];
        //     });
        //
        //     var path = d3.line()(pts)
        //     //console.log(path.length,path)
        //
        //     g.append('path').attr('d',path).attr('stroke','red').attr('fill','none').attr('id',t.properties.NOME)
        //
        //     // mesh.name = t.properties.NOME
        //     // mesh.centre = map.latLngToLayerPoint([t.properties.Cen_X,t.properties.Cen_Y])
        //
        // });
    }
    
    //colour()
    
}


function get_data(){
    d3.csv('../processed/vhi_group.csv').then(function(d){
        console.log(d)
        var scale = d3.scaleLinear().domain(d3.extent(d.map(e=>e.median)))
        var col = d3.interpolateViridis
        d.forEach(e=>{
            var i = document.getElementById(e.name)
            // console.log(i,e.name)
            // i.style.fill = col(scale(e.median))
              //i.style['fill-opacity']= 1
            //console.log(i,col(scale(e.median)))
            d3.select(i).style('fill',col(scale(e.median)))
            i.style.stroke = col(scale(e.median))
            i.style['stroke-opacity']=.9
            i.style['stroke-width']=.4
        })
        
        //console.log(scale,d)
        
    })
    
    
}


function colour(){
    var col = d3.interpolateViridis
    d3.selectAll('path').style('fill',d=>col(Math.random()))
}


module.exports = { drawmap ,colour,get_data};
