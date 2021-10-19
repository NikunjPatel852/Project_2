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

d3.selectAll("body").on("change", updatePlotly);

function updatePlotly() {
    // Use D3 to select the dropdown menu
    var dropdownMenu = d3.select("#country");
    // Assign the value of the dropdown menu option to a variable
    var dataset = dropdownMenu.node().value;

    var importUrl = `http://127.0.0.1:5000/${dataset}/importvaluedata`;
    // d3.json(url).then(function(data) {
    //     console.log(data)
    // })

    d3.json(importUrl).then(function (data){
        console.log(data);

            var table = new Tabulator("#example-table1", {
                data:data,
                height:"311px",
                layout:"fitColumns",
                columns:[ 
                    {title:"Partner Country", field:"par_countries", width:150, headerFilter:"input"},
                    {title:"Element", field:"element", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},   
                    {title:"Year", field:"year", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
                    {title:"Iteam", field:"item", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
                    {title:"Unit", field:"unit", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
                    {title:"Value", field:"value", hozAlign:"center", sorter:"number", bottomCalc:"sum", bottomCalcParams:{precision:3}},
                ],
        })
        
    });

    var exportUrl = `http://127.0.0.1:5000/${dataset}/exportvaluedata`
    d3.json(exportUrl).then(function (data){
    console.log(data);

    var table = new Tabulator("#example-table2", {
        data:data,
        height:"311px",
        layout:"fitColumns",
        columns:[ 
            {title:"Partner Country", field:"par_countries", width:150, headerFilter:"input"},
            {title:"Element", field:"element", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},   
            {title:"Year", field:"year", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
            {title:"Iteam", field:"item", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
            {title:"Unit", field:"unit", editor:"input", headerFilter:"select", headerFilterParams:{values:true}},
            {title:"Value", field:"value", hozAlign:"center", sorter:"number", bottomCalc:"sum", bottomCalcParams:{precision:3}},
        ],
    });

    //trigger download of data.csv file
    document.getElementById("download-csv").addEventListener("click", function(){
        table.download("csv", "data.csv");
    });

    //trigger download of data.json file
    document.getElementById("download-json").addEventListener("click", function(){
        table.download("json", "data.json");
    });

    //trigger download of data.xlsx file
    document.getElementById("download-xlsx").addEventListener("click", function(){
        table.download("xlsx", "data.xlsx", {sheetName:"My Data"});
    });

    //trigger download of data.pdf file
    document.getElementById("download-pdf").addEventListener("click", function(){
        table.download("pdf", "data.pdf", {
            orientation:"portrait", //set page orientation to portrait
            title:"Example Report", //add title to report
        });
    });

    //trigger download of data.html file
    document.getElementById("download-html").addEventListener("click", function(){
        table.download("html", "data.html", {style:true});
    });


    });


     var total = `http://127.0.0.1:5000/${dataset}/importtotalvalue`;
 
     d3.json(total).then(function(data) {
         console.log(data)

        //  var valueTotal = unpack[data.value];
        //  var totalYears = unpack[data.year];
         
         var trace1 = {
             data:data,
             x: "year",
             y: "value",
             type: 'scatter'
           };
           
           var data = [trace1];
           
           Plotly.newPlot('plot', data);
         
     });

}

updatePlotly();
















