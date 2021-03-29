var ctx1 = document.getElementById('myExpensesChart1').getContext('2d');
// how to select random elements from an array
// const getRandomType = () => {
//     console.log("I am in the random function")
//     const types= [
//             "bar","horizontalBar","pie","line","radar","doughnut",
//         ];
//     return types[Math.floor(Math.random() * types.length)];
// };
const renderChart = (data, labels) => {
    var myChart = new Chart(ctx1, {  
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label : 'Last 3 months Expenses',
                data  : data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }],
        },
        options: {
            title: {
                display: true,
                text: 'Distribution per Category (Last 3 momths)',
                responsive: true,
            },

        },
    });

};
const getChartData=()=>{
    console.log("fetching started")
    fetch('/expense-category-distribution')
    .then(res=>res.json())
    .then ((results) =>{
        console.log("results",results);
        const category_data=results.expense_category_data;
        const [labels,data]=[
            Object.keys(category_data),
            Object.values(category_data),
        ];
        console.log(labels)
        renderChart(data,labels);
    });
};

document.onload = getChartData() ;// load the chart