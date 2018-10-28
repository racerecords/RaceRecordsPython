function reqListener () {
  res = JSON.parse(this.responseText);
  populateMeta(res['meta']);
  buildRows(res['readings']);
}


function populateMeta (data) {
  var meta = [ "track","date","region","classes","ambientBefore",
              "groupNumber","reader","recorder","siteCertificationDate" ]
  var meter = ["factoryCalibrationDate","fieldCalibrationTime","batteryLevel","microphoneLocation"]
  var session = ["start","end"]
  var condition = ["temperature","humidity","barometer","weather","windSpeed","windDirection"]
  loop(meta, data);
  loop(session, data['session']);
  loop(meter, data['meter']);
  loop(condition, data['condition']);
}

function loop (arr, data) {
  var i;
  for (i=0; i<arr.length; i++) {
    populateElement(arr[i], data[arr[i]]);
  }
}

function populateElement(key, value) {
  console.log(key)
  el = document.getElementById(key);
  el.innerHTML = value;
}

function buildRows (rows) {
  table = document.getElementById('readingsTable');
  var i;
  for (i=0; i < rows.length; i++) {
    table.appendChild(buildRow(rows[i]));
  }
}

function buildRow (record) {
  row = document.createElement('tr'); 
  row.appendChild(buildData(record['carNumber']));
  row.appendChild(buildData(record['class']));
  row.appendChild(buildData(record['reading']));
  return row;
}

function buildData (value) {
  td = document.createElement('td');
  td.innerText = value
  return td;
}

var oReq = new XMLHttpRequest();
oReq.addEventListener("load", reqListener);
oReq.open("GET", "http://localhost:8000/js/report.json");
oReq.send();



