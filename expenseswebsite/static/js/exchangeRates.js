console.log("This is for exchange rates API");
const API_KEY = document.querySelector("api").getAttribute("key");
const exchangeRatesArea=document.querySelector(".exchangeRatesArea");
var e = document.querySelector("#inputGroupSelect04");
var currencySelected_Str=(e.options[e.selectedIndex].value);
var currencySelected = currencySelected_Str.substring(0,3)
const tableBody = document.querySelector(".table-body");

const getData=()=>{
    console.log("fetching started");
    var YOUR_API_KEY = API_KEY;
    fetch(`https://v6.exchangerate-api.com/v6/${YOUR_API_KEY}/latest/${currencySelected}`,{
        method:"GET",
    })
    .then(res=>res.json())
    .then ((results) =>{
            data=results.conversion_rates;
            for (const [country,value] of Object.entries(data)){
                console.log(country,value);
                tableBody.innerHTML+=`
                <tr>
                <td>${country}</td>
                <td>${value}</td>
                </tr>`;
            } 
    });
};
document.onload = getData() ;// load the chart