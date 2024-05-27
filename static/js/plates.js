function draw_boxes(objects, context) {
  console.log("boxes =>", objects)
  objects.forEach((obj) => {
    context.beginPath();
    context.rect(obj.x, obj.y, obj.width, obj.height);
    context.lineWidth = 2;
    context.strokeStyle = 'red';
    context.stroke();
  });
}

async function send_video(data) {
  console.log("send =>", data)
  const URL = 'http://localhost:8000/stream/';
  const form = new FormData();
  form.append('video', data);
  const response = await fetch(URL, {
    method: 'POST',
    body: form
  });
  console.log("response =>", response)
  return response.json();
}



function render_table(result, plate) {
  console.log("table =>", result, plate)
  var table = document.querySelector('table').getElementsByTagName('tbody')[0];
  var newRow = table.insertRow(0);

  var date = newRow.insertCell(0)
  var new_plate = newRow.insertCell(1)
  var new_result = newRow.insertCell(2)

  const new_date = new Date();
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric'
  };
  const dateSpanish = new_date.toLocaleDateString('es-ES', options);

  date.innerHTML = dateSpanish;
  new_plate.innerHTML = plate
  new_result.innerHTML = result ? 'Registrado' : 'No Registrado'
}

document.addEventListener("DOMContentLoaded", function() {
  var video = document.getElementById('video');
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');
  var stream;
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(mediaStream) {
      stream = mediaStream;
      video.srcObject = stream;
    })
    .catch(function(error) {
      console.log("Ha ocurrido un error: ", error);
      alert(error);
    });
  let recorder = new MediaRecorder(stream);
  recorder.ondataavailable = async (e) => {
    if (e.data.size > 0) {
      let resp = await send_video(e.data);
      console.log(resp);
      render_table(resp.result, resp.plate);
      draw_boxes(resp.objects, context);
    }
  }
  // let socket = new WebSocket('ws://localhost:8000/ws/video/');
  // socket.onopen = () => {
  //   console.log('Conectado');
  // };
  // socket.onmessage = (e) => {
  //   console.log(e.data);
  //   const data = JSON.parse(e.data);
  //   context.clearRect(0, 0, canvas.width, canvas.height);
  //   // data.objects.forEach((obj) => {
  //   //   context.beginPath();
  //   //   context.rect(obj.x, obj.y, obj.width, obj.height);
  //   //   context.lineWidth = 2;
  //   //   context.strokeStyle = 'red';
  //   //   context.stroke();
  //   // });
  //   //
  // }
  //

});
