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
