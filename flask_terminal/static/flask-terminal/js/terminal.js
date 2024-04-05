function initializeTerminal() {
    const terminal = new Terminal();
    const terminalContainer = document.getElementById('terminal');
    window.addEventListener("beforeunload", (event) => {
        console.log('Window is closing...');
        stopTerminal();
    });

    terminal.open(terminalContainer);
    terminal.writeln('Welcome to Flask Terminal');

    let commandBuffer = '';
    let previousCommand = '';

    terminal.onData(data => {
        if (data === '\r') { // If the return key (Enter) is pressed
            sendInputToServer(commandBuffer);
            previousCommand = commandBuffer;
            commandBuffer = ''; // Reset the command buffer after sending
        } else if (data === '\b'  || data === '\x7F') { // If the backspace key is pressed
            
            if (commandBuffer.length > 0) {
                // Remove the last character from the command buffer
                commandBuffer = commandBuffer.slice(0, -1);
                // Move the cursor back, overwrite the last character with a space, then move back again
                terminal.write('\b \b');
            }
        } else {
            console.log('Data:', data);
            terminal.write(data); // Echo the typed character
            commandBuffer += data; // Add the typed character to the command buffer
        }
    });

    function startTerminal() {
        terminal.focus();
        fetch('/terminal/init')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Terminal started.');
            })
            .catch(error => {
                console.error('Error starting terminal:', error);
                terminal.write(`Error: ${error.message}\r\n`);
            });
    }

    function sendInputToServer(input) {
        fetch('/terminal/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: input }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Command sent to server.');
        })
        .catch(error => {
            console.error('Error sending input to server:', error);
            terminal.write(`Error: ${error.message}\r\n`);
        });
    }

    function pollServerForOutput() {
        fetch('/terminal/poll')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if(data.output) {
                    result = data.output.replace(previousCommand, '\r\n')
                    terminal.write(result);
                    console.log(result)
                }
            })
            .catch(error => {
                console.error('Polling error:', error);
            });

        setTimeout(pollServerForOutput, 1000);
    }

    function clearTerminal() {
        terminal.clear();
    }

    function resetTerminal() {
        clearTerminal();
        startTerminal();
    }

    function stopTerminal() {
        console.log('Stopping terminal...');

        fetch('/terminal/stop')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Terminal stopped.');
            })
            .catch(error => {
                console.error('Error stopping terminal:', error);
                terminal.write(`Error: ${error.message}\r\n`);
            });
    }
    
    startTerminal();
    pollServerForOutput();
  
}


