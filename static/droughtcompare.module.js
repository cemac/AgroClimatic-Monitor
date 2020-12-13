import {
    Runtime,
    Inspector
} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
import define from "https://api.observablehq.com/@wolfiex/reusable-brazil.js?v=3";



const main = new Runtime().module(define, name => {
    console.log(name)
    switch (name) {
        case "stateMap":
            return Inspector.into(".stateMap")();
        case "updatefill":
            return Inspector.into(".updatefill")();
        case "elements":
            return Inspector.into(".elements")();
            // case 'e':
            // return {
            //     fulfilled(value) { console.log(name, value); },
            //     rejected(error) { console.error(error); }
            //   };

    }
});







console.log(d3)

main.redefine("width", Math.min(window.innerWidth, window.innerHeight));


var year
var month
var alld;

document.getElementById('homeyear').addEventListener("click", function(e) {
    loadImage("hy_", e.path[0].getAttribute('value'))
    e.path[0].classList.toggle("activeimg")
});
document.getElementById('homemonth').addEventListener("click", function(e) {
    loadImage("hm_", e.path[0].getAttribute('value'))
    e.path[0].classList.toggle("activeimg")
});



d3.json('./plotdata/biindicate.json').then(function(data) {
        main.redefine("data", data);
        alld = data
        //console.log(data)
    }).then(() => {

            setTimeout(function() {
                
                year = year || [...document.querySelectorAll('#homeyear a')].pop().innerText
                
                month = Object.keys(alld).filter(d=>d.slice(0,4)===year).map(d=>d.slice(4)).sort((a, b) => b-a)[0]
                
                
                document.getElementById('hm_'+month).classList.toggle('activeimg')
                document.getElementById('hy_'+year).classList.toggle('activeimg')
                
                // month = month || [...document.querySelectorAll('#homemonth a')].pop().innerText
                
                console.log('updsat',year,month);
                loadImage('hm_',month)


            }, 300)
        
})





            function loadImage(type, num) {

                [...document.querySelectorAll(`.activeimg[id^="${type}"]`)].forEach(d => d.classList.toggle('activeimg'))


                if (type === 'hm_') {
                    month = '' + num
                } else {
                    year = '' + num
                }
                console.log(year, month)
                main.redefine('elements', alld[year + month])



            }