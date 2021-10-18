var url = "http://127.0.0.1:5000/countrieslist";
d3.json(url).then(function (data) {
    var countryList = data;
    console.log(countryList);
    var country_dropdown = document.getElementById("country");
    countryList.forEach(country => {
        country_dropdown.options.add(new Option(country, country));
    });
    country_dropdown.onchange = event => {
        console.log(event.target.value);
    };
});

var importUrl = 'http://127.0.0.1:5000/importvaluedata';
d3.json(importUrl).then(function (data){
  console.log(data);

  var table = new Tabulator("#example-table1", {
      data:data,
      height:"311px",
      layout:"fitColumns",
      columns:[ 
          {title:"Partner Country", field:"par_countries", width:150, headerFilter:"input"},   
          {title:"Year", field:"year", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
          {title:"Iteam", field:"item", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
          {title:"Value", field:"value", hozAlign:"center", sorter:"value",  headerFilter:"input"},
      ],
  });

});

var exportUrl = 'http://127.0.0.1:5000/exportvaluedata';
d3.json(exportUrl).then(function (data){
  console.log(data);

  var table = new Tabulator("#example-table2", {
      data:data,
      height:"311px",
      layout:"fitColumns",
      columns:[ 
          {title:"Partner Country", field:"par_countries", width:150, headerFilter:"input"},   
          {title:"Year", field:"year", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
          {title:"Iteam", field:"item", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
          {title:"Value", field:"value", hozAlign:"center", sorter:"value",  headerFilter:"input"},
      ],
  });

});






