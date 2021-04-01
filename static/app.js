window.addEventListener('load', main);
function main() {
  function getAPIData() {
    var http = new XMLHttpRequest();
   
    http.onreadystatechange = function() {
        if(this.readyState === 4 && this.status === 200) {
          update(JSON.parse(this.responseText));
        }
    }
   
    http.open("GET", "/api", true);
    http.send();
  }
 
  function update(apiData) {
    var tempC = document.getElementById("tempC");
    var humidity = document.getElementById("humidity");
   
    tempC.innerHTML = parseFloat(apiData.temperature).toFixed(2) + "°C";
    humidity.innerHTML = parseFloat(apiData.humidity).toFixed(2) + " %";
  }

  getAPIData(); 
}
