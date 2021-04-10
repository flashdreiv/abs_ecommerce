// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily =
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#292b2c";

var url = "/dashboard/chart_data/";
var order_data;
function buildAreaChart() {
  fetch(url, {
    method: "GET",
    headers: {
      "Content-type": "application/json",
      "X-CSRFTOKEN": csrftoken,
    },
    // body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const orders = data["orders"];
      order_data = [Object.keys(orders), Object.values(orders)];

      // Area Chart Example
      var ctx = document.getElementById("myAreaChart");
      var myLineChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: order_data[0],
          datasets: [
            {
              label: "Sales",
              lineTension: 0.3,
              backgroundColor: "rgba(2,117,216,0.2)",
              borderColor: "rgba(2,117,216,1)",
              pointRadius: 5,
              pointBackgroundColor: "rgba(2,117,216,1)",
              pointBorderColor: "rgba(255,255,255,0.8)",
              pointHoverRadius: 5,
              pointHoverBackgroundColor: "rgba(2,117,216,1)",
              pointHitRadius: 50,
              pointBorderWidth: 2,
              data: order_data[1],
            },
          ],
        },
        options: {
          scales: {
            xAxes: [
              {
                time: {
                  unit: "date",
                },
                gridLines: {
                  display: false,
                },
                ticks: {
                  maxTicksLimit: 7,
                },
              },
            ],
            yAxes: [
              {
                ticks: {
                  min: 0,
                  max: 4000,
                  maxTicksLimit: 5,
                },
                gridLines: {
                  color: "rgba(0, 0, 0, .125)",
                },
              },
            ],
          },
          legend: {
            display: false,
          },
        },
      });
    });
}
buildAreaChart();
