import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
import define from "https://api.observablehq.com/@wolfiex/reusable-brazil.js?v=3";



const main = new Runtime().module(define, name => {
  console.log(name)    
  switch (name){
  case "stateMap": return Inspector.into(".stateMap")();
  case "updatefill": return Inspector.into(".updatefill")();
  case "elements": return Inspector.into(".elements")();
  // case 'e':
  // return {
  //     fulfilled(value) { console.log(name, value); },
  //     rejected(error) { console.error(error); }
  //   };

}});

const menu = document.getElementById('homeSubmenu')


console.log(d3)

main.redefine("width", Math.min(window.innerWidth,window.innerHeight));


var date = '201911'
var alld;


 d3.json('./biindicate.json').then(function (data){
         main.redefine("data", data );
         alld=data
         console.log(data)
     }).then(
      async()=>{

         const sleep = m => new Promise(r => setTimeout(r, m))


         
         console.log('start')
         
          // (async () => {
              
         var keys = Object.keys(alld)
         console.log(keys)
         for (var i = 0; i < keys.length-3; i++) {
             
             
            var node=document.createElement("LI");
            var item=document.createElement('a')
            item.value = keys[i];
            item.innerText = keys[i].slice(0,4)+' '+keys[i].slice(4,6)
            node.appendChild(item);
            menu.appendChild(node);

            }
            
            
            
            
            menu.addEventListener("click",function(e) {
                    console.log('click',e.path[0].value)
                    main.redefine('elements',alld[e.path[0].value])

    });
            
            
         
}).then(()=>{
    
setTimeout(function(){ 
       console.log('updsat');
       [...document.querySelectorAll('#homeSubmenu li a')].pop().click()

}, 2000)
}
)


