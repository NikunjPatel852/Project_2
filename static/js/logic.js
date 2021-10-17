// fetch('http://127.0.0.1:5000/api/v1.0/countrieslist')
//     .than(response => {
//         return response.json();
//     })
//     .than(users => {
//         console.log(countrieslist)
//     });



var url = "http://127.0.0.1:5000/countrieslist";
d3.json(url).then(function(data) {
    var countryList = data;
    console.log(countryList);
    var country_dropdown = document.getElementById("country");
    countryList.forEach(country => {
        country_dropdown.options.add(new Option(country,country))
    });
    country_dropdown.onchange = function (event){
        console.log(event.target.value)
    }
});
//Initial connection to api. 
var countryUrl='http://127.0.0.1:5000/countrieslist';
d3.json(countryUrl).then(function(data){
    var countryName = [data];
    console.log(countryName);
}); 
var yearurl='http://127.0.0.1:5000/yearslist';
d3.json(yearurl).then(function(data){
    var yearslist = [data];
    console.log(yearslist)
}); 

// var exporturl='http://127.0.0.1:5000/exportdata2011';
// d3.json(exporturl).then(function(data){
//     var exportHomeCountry = [data.rep_countries];
//     console.log(exportHomeCountry);
//     var exportPartCountry = [data.par_countries];
//     console.log(exportPartCountry);
//     var exportItem = [data.item];
//     console.log(exportItem);
//     var exportValue = [data.value];
//     console.log(exportValue);
//     buildTable(exportHomeCountry, exportPartCountry, exportItem, exportValue)
// }); 

var importUrl='http://127.0.0.1:5000/importdata2011';
d3.json(importUrl).then(function(data){
    var importdata2011 = [data];
    // console.log(importdata2011);
    const obj = Object.assign({}, importdata2011);
    // console.log(obj);

  var importHomeCountry = obj[0].rep_countries;
  // console.log(importHomeCountry);
  var importPartCountry = obj[0].par_countries;
  // console.log(importPartCountry);
  var importItem = obj[0].item;
  // console.log(importItem);
  var importValue = obj[0].value;
  console.log(importValue);
  buildTable(importHomeCountry, importPartCountry,importItem, importValue);

  function buildTable(importHomeCountry, importPartCountry,importItem, importValue) {
    var table = d3.select("#ufo-table");
    var tbody = table.select("tbody");
    var trow;
    for (var i = 0; i < 12; i++) {
      trow = tbody.append("tr");
      trow.append("td").text(importHomeCountry[i]);
      trow.append("td").text(importPartCountry[i]);
      trow.append("td").text(importItem[i]);
      trow.append("td").text(importValue[i]);
    }
  }

  function buildGraph(importHomeCountry, importPartCountry,importItem, importValue) {
    var trace1 = {
      x: obj.map(row => row.value),
      y: obj.map(row => row.item),
      text: obj.map(row => row.),
      name: "Greek",
      type: "bar",
      orientation: "h"
    };
  
    // data
    var chartData = [trace1];
  
    // Apply the group bar mode to the layout
    var layout = {
      title: "Greek gods search results",
      margin: {
        l: 100,
        r: 100,
        t: 100,
        b: 100
      }
    };
  
    // Render the plot to the div tag with id "plot"
    Plotly.newPlot("plot", chartData, layout);


  }

  
}); 



