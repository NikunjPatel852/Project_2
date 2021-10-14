// fetch('http://127.0.0.1:5000/api/v1.0/countrieslist')
//     .than(response => {
//         return response.json();
//     })
//     .than(users => {
//         console.log(countrieslist)
//     });

// let request = new XMLHttpRequest();
// request.open("GET","http://127.0.0.1:5000/api/v1.0/countrieslist");
// request.send();
// request.onload = () => {
//     console.log(request);
//     if (request.status == 200) {
//         console.log(JSON.parse(request.response));
//     } else {
//         console.log(`error ${request.status} ${request.statusText}`)
//     }
// }

var url = "http://127.0.0.1:5000/countrieslist";
d3.json(url).then(function(data) {
    var countryList = [data];
    console.log(countryList);
});
