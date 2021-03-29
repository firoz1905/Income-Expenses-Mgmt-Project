var ctx = document.getElementById('incomeVsExpensesChart').getContext('2d');
// how to select random elements from an array
// const getRandomType = () => {
//     console.log("I am in the random function")
//     const types= [
//             "bar","horizontalBar","pie","line","radar","doughnut",
//         ];
//     return types[Math.floor(Math.random() * types.length)];
// };
const renderChart = (data, labels) => {
    var myChart = new Chart(ctx, {  
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label : '',
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
                text: 'Income Vs Expenses',
                responsive: true,
            },
            

        },
    });

};
const getChartData=()=>{
    console.log("fetching started")
    fetch('/income/income-vs-expenses-stats')
    .then(res=>res.json())
    .then ((results) =>{
        console.log("results",results);
        const category_data_total_expense=results.income_expense_data.total_expense;
        const category_data_total_income=results.income_expense_data.total_income;
        const [labels,data]=[
            [Object.keys(category_data_total_expense),Object.keys(category_data_total_income)],
            [Object.values(category_data_total_expense),Object.values(category_data_total_income)],
        ];
        console.log(data)
        renderChart(data,labels);
    });
};

document.onload = getChartData() ;// load the chart