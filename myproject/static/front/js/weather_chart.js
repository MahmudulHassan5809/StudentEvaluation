var forecastData = {
  highTemp: [],
  lowTemp: []
}


let latt;
let long;

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  latt =  position.coords.latitude;
  long = position.coords.longitude;
  $.ajax({
    type: "GET",
    url: "https://api.darksky.net/forecast/c15e25c81f934b7545c371389692db04/" + latt + "," + long,
    dataType: "jsonp",
    success: function(data) {
    // console.log(data);

    for (i = 0; i < data.daily.data.length; i++) {
      forecastData.highTemp[i] = data.daily.data[i].apparentTemperatureMax;
      forecastData.lowTemp[i] = data.daily.data[i].apparentTemperatureMin;
    }

    // Instalize Chart.js
    var ctx = document.getElementById("myChart");
    var chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        datasets: [
        {
          label: "Low Temp",
          data: forecastData.lowTemp,
            // fill: false,
            backgroundColor: "rgba(79,117,180,0.95)",
            borderColor: "rgba(49,85,144,1)",
            borderWidth: 1,
            lineTension: 0,
          },
          {
            label: "High Temp",
            data: forecastData.highTemp,
            // fill: false,
            backgroundColor: "rgba(211,96,96,0.95)",
            borderColor: "rgba(223,53,53,1)",
            borderWidth: 1,
            lineTension: 0,
          }
          ]
        },
        options: {
          title: {
            display: true,
            text: "7-Day Forecast"
          },
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true
              }
            }]
          }
        }
      });
  },
  error: function(error) {
    console.log(error);
  }
});
}

function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
    console.log("User denied the request for Geolocation.");
    break;
    case error.POSITION_UNAVAILABLE:
    console.log("Location information is unavailable.");
    break;
    case error.TIMEOUT:
    console.log("The request to get user location timed out.");
    break;
    case error.UNKNOWN_ERROR:
    console.log("An unknown error occurred.");
    break;
  }
}

getLocation()




