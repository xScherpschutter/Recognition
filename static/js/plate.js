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

            if (part.includes('Content-Type: text/plain')) {
                const textPart = part.split('Content-Type: text/plain\r\n\r\n')[1];
                if (textPart) {
                    const text = textPart.split('\r\n\r\n')[0];
                    const textContent = text.split('|')[0];
                    const dateSpanish = text.split('|')[1];
                    const registerContent = text.split('|')[2];
                    appendToTable(textContent, dateSpanish, registerContent)

                }
            }
        }
        buffer = parts[parts.length - 1];
    }
}


function appendToTable(text, date_format, register) {
    var table = document.querySelector('table').getElementsByTagName('tbody')[0];
    var lastRow = table.rows[0];

    if (text == '') {
        return
    }
    
    if (lastRow && lastRow.cells[1].textContent === text) {
        return;
    }
    
    var newRow = table.insertRow(0);
    
    var date = newRow.insertCell(0);
    var textCell = newRow.insertCell(1);
    var registerCell = newRow.insertCell(2);

    date.innerHTML = date_format;
    textCell.textContent = text;
    registerCell.innerHTML = register;
}

document.addEventListener('DOMContentLoaded', function() {
    
    processStream("/video_stream/");
 
});
