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

        if ( isNaN(dni) ) {
            alert("Ingrese una cédula correcta!")
            return
        }

        if (dni.length != 10){
            alert("La cédula debe tener 10 digitos!")
            return
        }

        sendImage(imageData, dni);
        sendCapture.style.display = 'none';
        document.getElementById('cedula').value = ''
        
    });

    function sendImage(imageData, dni) {
        fetch('/face/', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                image: imageData,
                dni : dni
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const result = data.success
            const dni = data.dni
            render_table(result, dni)

        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function render_table(result, dni) {
        var table = document.querySelector('table').getElementsByTagName('tbody')[0];
        var newRow = table.insertRow(0);

        var date = newRow.insertCell(0)
        var new_dni = newRow.insertCell(1)
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
        new_dni.innerHTML = dni
        new_result.innerHTML = result ? 'Registrado' : 'No Registrado'
    }
});