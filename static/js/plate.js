async function processStream(url) {
    const response = await fetch(url);
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    
    while (true) {

        const { done, value } = await reader.read();
        if (done) {
            console.log('Break')
            break
        };
        
        console.log(value)
        buffer +=  decoder.decode(value, { stream: true });

        let parts = buffer.split('--');

        for (let i = 0; i < parts.length - 1; i++) {
            const part = parts[i];

            if (part.includes('Content-Type: image/jpeg')) {
                const imgPart = part.split('Content-Type: image/jpeg\r\n\r\n')[1];
                if (imgPart) {
                    const imgContent = imgPart.split('\r\n\r\n')[0];
                    // console.log(imgContent)
                    // Falta el renderizado del frame en tiempo real
                }
            }


            if (part.includes('Content-Type: text/plain')) {
                const textPart = part.split('Content-Type: text/plain\r\n\r\n')[1];
                if (textPart) {
                    const textContent = textPart.split('\r\n\r\n')[0];

                        handleText(textContent)

                }
            }
        }
        buffer = parts[parts.length - 1];
    }
}



function handleText(text) {
    appendToTable(text);
}

function appendToTable(text) {
    var table = document.querySelector('table').getElementsByTagName('tbody')[0];
    
    var lastRow = table.rows[0];

    if (text == '') {
        return
    }
    
    if (lastRow && lastRow.cells[1].textContent === text) {
        return;
    }
    
    var newRow = table.insertRow(0);
    

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

    var date = newRow.insertCell(0);
    var textCell = newRow.insertCell(1);

    date.innerHTML = dateSpanish;
    textCell.textContent = text;
}

document.addEventListener('DOMContentLoaded', function() {
    
    processStream("/video_stream/");

    // var video = document.getElementById('video');

    // navigator.mediaDevices.getUserMedia({ video: true })
    // .then(function(stream) {
    //     video.srcObject = stream;
        
    // })
    // .catch(function(error) {
    //     console.log("Ha ocurrido un error: ", error);
    //     alert(error)
    // });
    
    
});
