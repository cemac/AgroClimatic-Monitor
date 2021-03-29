const TC = require('tiny-complete');
const d3 = require('d3')


d3.csv('/data/geojson/search.csv/').then(d=>{


const myData = d.map(e=>{return e.key +' - '+e.val})

myTC = new TC({
  id: 'isearch',
  listItems: myData,
  // onUserInput: onInputArray,
  onSelect: function(val) {
      
      console.log('search:',val)
      window.location.href = `/${window.location.pathname.split('/')[1]}/individual/${val.split(' - ')[1]}/`;
      },
  maxResults: 7
})

// document.getElementById('isearch').value=''
// console.clear()

})