
var THREE = require("three");
//var OrbitControls = require("three-orbit-controls")(THREE);

var scene, camera,renderer;


function init(dom) {
    scene = new THREE.Scene();
    camera = new THREE.OrthographicCamera( 0, width*2 , 0,height*2, 0, 1000 );

    // camera.position.z = 0;
    // camera.position.y = 0
    //camera.lookAt(scene.position);
    var helper = new THREE.CameraHelper( camera );
    scene.add( helper );
    
    renderer = new THREE.WebGLRenderer({antialias:true,alpha:true});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize( window.innerWidth, window.innerHeight ); 
    scene.background = null;
    dom.appendChild(renderer.domElement);
    
    return {renderer,scene}
}


function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

function drawmap(map){

d3.json("../data/web_simplified_2.geojson").then(onmapload);

function onmapload(topology) {
console.log(topology)
var counties = topology.features; //.slice(0,1300)
var chunks = 600;
d3.range(0, counties.length, chunks).forEach(i => {
    counties.slice(i, i + chunks + 1).forEach(t => {
        
        
        var pts = t.geometry.coordinates[0].map(c => {
            var px = map.latLngToLayerPoint(c.map(parseFloat));
            // console.log(x)
            return new THREE.Vector2(px.x, px.y);
        });

        var shape = new THREE.Shape(pts);
        //console.log(pts)
        var geometry = new THREE.ShapeGeometry(shape);
        var material = new THREE.MeshBasicMaterial({ color: 0xffff00 });
        var mesh = new THREE.Mesh(geometry, material);
        
        
        var extrudeSettings = {
            steps: 2,
            depth: Math.random() * 1,
            bevelEnabled: true,
            bevelThickness: 1,
            bevelSize: 1,
            bevelOffset: 0,
            bevelSegments: 3,
        };
        
        var geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
        var material = new THREE.MeshBasicMaterial({ wireframe:false,color: 0x00ffff });
        mesh = new THREE.Mesh(geometry, material);
        
        // 
        
        mesh.name = t.properties.NOME
        mesh.centre = map.latLngToLayerPoint([t.properties.Cen_X,t.properties.Cen_Y])
        scene.add(mesh);

    });
    //console.log(scene)
    renderer.render(scene, camera)
});
console.log('loaded all')
}
}

module.exports = {init,animate,drawmap}