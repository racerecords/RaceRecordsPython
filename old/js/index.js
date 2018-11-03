function reqListener () {
  res = JSON.parse(this.responseText);
  populateMeta(res);
  fetchRows();
}


function populateMeta (data) {
  var meta = [ "track","date","region","classes","ambientBefore",
              "groupNumber","reader","recorder","siteCertificationDate" ]
  var meter = ["factoryCalibrationDate","fieldCalibrationTime","batteryLevel","microphoneLocation"]
  var session = ["start","end"]
  var condition = ["temperature","humidity","barometer","weather","windSpeed","windDirection"]
  loop(meta, data);
  loop(session, data);
  loop(meter, data);
  loop(condition, data);
}

function loop (arr, data) {
  var i;
  for (i=0; i<arr.length; i++) {
    populateElement(arr[i], data[arr[i]]);
  }
}

function populateElement(key, value) {
  el = document.getElementById(key);
  el.innerHTML = value;
}

function buildRows () {
  res = JSON.parse(this.responseText).readings;
  console.log(res);
  table = document.getElementById('readingsTable');
  var i;
  for (i=0; i < res.length; i++) {
    table.appendChild(buildRow(res[i]));
  }
}

function buildRow (record) {
  row = document.createElement('tr'); 
  row.appendChild(buildData(record['number']));
  row.appendChild(buildData(record['carclass']));
  row.appendChild(buildData(record['reading']));
  return row;
}

function buildData (value) {
  td = document.createElement('td');
  td.innerText = value
  return td;
}

var path = 'https://6lw2dm239a.execute-api.us-east-1.amazonaws.com/test/records/1';

var oReq = new XMLHttpRequest();
oReq.addEventListener("load", reqListener);
oReq.open("POST", path);
oReq.send();

function fetchRows() {
  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", buildRows);
  oReq.open("POST", path + '/readings');
  oReq.send();
}
