function handleSubmit() {
    // Prevent the page from refreshing
    d3.event.preventDefault();
  
    // Select the input value from the form
    var stock = d3.select("#country").node().value;
    console.log(stock);

    // Build the plot with the new stock
    buildPlot(stock);
}


function buildPlot(stock) {

    var url = `http://127.0.0.1:5000/${stock}/importvaluedata`;

    d3.json(url).then(function(data) {
        console.log(data)
    })


}
