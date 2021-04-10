// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily =
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#292b2c";

// Bar Chart Example
function buildBarChart() {
  var url = "/dashboard/chart_data/";
  let order_data = [];
  fetch(url, {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify({ timeseries: "monthly" }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const orders = data["orders"];
      order_data = [Object.keys(orders), Object.values(orders)];
      var ctx = document.getElementById("myBarChart");
      var myLineChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: order_data[0],
          datasets: [
            {
              label: "Revenue",
              backgroundColor: "rgba(2,117,216,1)",
              borderColor: "rgba(2,117,216,1)",
              data: order_data[1],
            },
          ],
        },
        options: {
          scales: {
            xAxes: [
              {
                time: {
                  unit: "month",
                },
                gridLines: {
                  display: false,
                },
                ticks: {
                  maxTicksLimit: 6,
                },
              },
            ],
            yAxes: [
              {
                ticks: {
                  min: 0,
                  max: 15000,
                  maxTicksLimit: 5,
                },
                gridLines: {
                  display: true,
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

buildBarChart();
