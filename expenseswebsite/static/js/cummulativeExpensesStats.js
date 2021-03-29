var ctx2 = document.getElementById('myExpensesChart2').getContext('2d');
// how to select random elements from an array
// const getRandomType = () => {
//     console.log("I am in the random function")
//     const types= [
//             "bar","horizontalBar","pie","line","radar","doughnut",
//         ];
//     return types[Math.floor(Math.random() * types.length)];
// };
const renderChart2 = (data, labels) => {
    var myChart = new Chart(ctx2, {  
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label : 'Last 3~4 months Expenses',
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
                    'rgba(153, 102, 255,1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }],
        },
        options: {
            title: {
                display: true,
                text: 'Category Cummulative Comparison (Last 3~4 momths)',
                responsive: true,
            },

        },
    });

};
const getChartData2=()=>{
    console.log("fetching started")
    fetch('/category-cummulative-comparison')
    .then(res=>res.json())
    .then ((results) =>{
        console.log("results",results);
        const category_data=results.expense_cummulative_data;
        const [labels,data]=[
            Object.keys(category_data),
            Object.values(category_data),
        ];
        renderChart2(data,labels);
        console.log(labels)
    });
};

document.onload = getChartData2() ;// load the chart