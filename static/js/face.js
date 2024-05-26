document.addEventListener("DOMContentLoaded", function () {
    var video = document.getElementById('video');
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var start = document.getElementById('start');
    var stop = document.getElementById('stop');
    var snap = document.getElementById('snap');
    var sendCapture = document.getElementById('sendCapture');
    var stream;

    start.addEventListener("click", function() {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(mediaStream) {
            stream = mediaStream;
            video.srcObject = stream;
            start.style.display = "none";
            stop.style.display = "block";
            snap.style.display = "block";
        })
        .catch(function(error) {
            console.log("Ha ocurrido un error: ", error);
            alert(error);
        });
    });

    stop.addEventListener("click", function() {
        if (stream) {
            let tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            stream = null;
        }
        video.srcObject = null;
        start.style.display = "block";
        stop.style.display = "none";
        snap.style.display = "none";
        sendCapture.style.display = "none";
    });

    snap.addEventListener("click", function() {
        context.drawImage(video, 0, 0, 640, 480);
        sendCapture.style.display = "block";
    });

    sendCapture.addEventListener("click", function() {
        var imageData = canvas.toDataURL('image/png');
        var dni = document.getElementById('cedula').value;
        console.log("Cedula:", dni)
        sendImage(imageData, dni);
        sendCapture.style.display = 'none';
    });

    function sendImage(imageData, dni) {
        console.log("Cedula:", dni)
        console.log("Imagen capturada y enviada:", imageData);
    }
});