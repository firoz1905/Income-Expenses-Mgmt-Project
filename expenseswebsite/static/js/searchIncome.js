const searchField = document.querySelector('#searchField');

const tableOutput = document.querySelector('.table-output');
tableOutput.style.display = 'none';

const appTable = document.querySelector(".app-table");

const paginationContainer = document.querySelector(".pagination-container");

const noResults = document.querySelector(".no-results");

const tableBody = document.querySelector(".table-body");

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    if (searchValue.trim().length > 0) {
        tableBody.innerHTML= ""
        paginationContainer.style.display = 'none'
        console.log('searchValue', searchValue);

    //search_str=json.loads(request.body).get('searchText','')
    fetch("/income/search-income", {
            // This would make an api call to the url with input as body and method POST
            // Json.stringify - turns JS object to a json so we can send over network
            body: JSON.stringify({
                searchText: searchValue
            }),
            method: "POST",
            //fetch returns a promise so we write .then
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            appTable.style.display = 'none';
            tableOutput.style.display = 'block'; // show the table if results exists
            if (data.length === 0) {
                //noResults.style.display ="block"
                tableOutput.innerHTML = `No results found !`;
            } else{
                data.forEach(item=>{
                    // we re going to append the a row for each item we found in search results
                    tableBody.innerHTML +=`
                <tr>
                <td>${item.amount}</td>
                <td>${item.source}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>
                `
                })
                
            }
        });
    } else{
        tableOutput.style.display='none';
        appTable.style.display='block';
        paginationContainer.style.display='block';  
    }

});