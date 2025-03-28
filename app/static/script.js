const API_BASE = '/api';

console.log("Using API:", API_BASE); // Debugging log

function updateMemory(address, value) {
    fetch(`${API_BASE}/update_memory`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: address, value: value.trim() }) // Trim spaces
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Log success
            fetchMemory(); // Refresh memory UI after update
        })
        .catch(error => console.error('Error updating memory:', error));
}

function fetchMemory() {
    fetch(`${API_BASE}/get_memory?nocache=${new Date().getTime()}`)
        .then(response => response.json())
        .then(data => {
            fetchStatus().then(statusData => {
                let memoryContainer = document.getElementById('memoryContainer');
                memoryContainer.innerHTML = "";  // Clear old memory view

                data.memory.forEach((value, index) => {
                    let memoryCell = document.createElement('div');
                    memoryCell.classList.add('memory-cell');

                    let label = document.createElement('span');
                    label.textContent = `Mem[${index}]: `;

                    let input = document.createElement('input');
                    input.type = "text";
                    input.value = value;
                    input.classList.add('memory-input');
                    input.setAttribute("data-index", index);

                    // Update memory when input loses focus
                    input.addEventListener("blur", function () {
                        updateMemory(index, this.value);
                    });

                    memoryCell.appendChild(label);
                    memoryCell.appendChild(input);
                    memoryContainer.appendChild(memoryCell);

                    fetchStatus();  // Fetch status after memory update

                    // Highlight the current instruction pointer
                    if (index === statusData.instruction_pointer) {
                        memoryCell.classList.add('highlight');
                    }
                });
            });
        })
        .catch(error => console.error('Error fetching memory:', error));
}

function fetchStatus() {
    return fetch(`${API_BASE}/get_status?nocache=${new Date().getTime()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('accumulator').innerText = data.accumulator;
            document.getElementById('instruction-pointer').innerText = data.instruction_pointer;
            return data; // Return the status so fetchMemory() can use it
        })
        .catch(error => console.error('Error fetching status:', error));
}

function executeInstruction(userInput = null) {
    isRunning = true; // Set running state

    fetch(`${API_BASE}/step_instruction`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: userInput })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);

            if (data.message.includes("Input required") ||
                data.message.includes("Output") ||
                data.message.includes("Invalid") ||
                data.message.includes("Program halted")) {
                appendToConsole(data.message);
            }

            fetchMemory(); // Update memory and highlight

            if (data.halt) {
                console.log("Execution halted.");
                isRunning = false;
                return;
            }

            if (data.waitForInput) {
                showModal();
                isRunning = false;
            } else if (isRunning) {
                setTimeout(() => executeInstruction(), 100); // Continue automatically
            }
        })
        .catch(error => console.error('Error executing instruction:', error));
}

function appendToConsole(message) {
    let consoleElement = document.getElementById('execution-message');
    let newMessage = document.createElement('div');
    newMessage.textContent = message;
    consoleElement.appendChild(newMessage);
    consoleElement.scrollTop = consoleElement.scrollHeight; // Auto-scroll to latest message
}

function showModal(mode = 'run') {
    let modal = document.getElementById('input-modal');
    let userInputField = document.getElementById('user-input');

    userInputField.setAttribute('data-mode', mode);
    modal.classList.remove('hidden'); // Show modal
    modal.style.display = 'flex'; // Ensure it's visible
    userInputField.focus();
}

function hideModal() {
    let modal = document.getElementById('input-modal');
    modal.classList.add('hidden'); // Hide modal
    modal.style.display = 'none';
}

function submitInput() {
    let userInputField = document.getElementById('user-input');
    let userInput = userInputField.value.trim(); // Get and trim input value
    let mode = userInputField.getAttribute('data-mode') || 'run';

    if (userInput === "") {
        alert("Please enter a value."); // Prevent empty submission
        return;
    }

    hideModal(); // Hide the modal
    userInputField.value = ""; // Clear input field after submission
    userInputField.removeAttribute('data-mode'); // Reset mode

    // Call appropriate function based on mode
    if (mode === 'step') {
        stepInstruction(userInput);
    } else {
        executeInstruction(userInput);
    }
}

function resetSystem() {
    fetch(`${API_BASE}/reset`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById('execution-message').innerText = data.message;
            fetchMemory();  // Refresh memory after reset
            fetchStatus();  // Refresh accumulator and instruction pointer
        })
        .catch(error => console.error('Error resetting system:', error));
}

function loadFile() {
    // Create a temporary file input element
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.txt';

    // When a file is selected, handle the upload
    fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];

        if (!file) {
            alert("Please select a file.");
            return;
        }

        let formData = new FormData();
        formData.append("file", file);

        fetch(`${API_BASE}/load_file`, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    // Always refresh memory display in case of error (memory might have been reset)
                    fetchMemory();
                    // Show the error message
                    alert(data.message);
                    // Also log the error to the execution console
                    appendToConsole(data.message);
                } else {
                    alert(data.message);
                    fetchMemory(); // Refresh memory after loading file
                }
            })
            .catch(error => {
                console.error('Error loading file:', error);
                alert('Error loading file. Please try again.');
            });
    });

    // Trigger the file selection dialog
    fileInput.click();
}

// Add this new function for the Step button
function stepInstruction(userInput = null) {
    fetch(`${API_BASE}/step_instruction`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: userInput })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);

            // Always append execution messages to console for better visibility
            appendToConsole(data.message);

            fetchMemory(); // Update memory and highlight

            if (data.waitForInput) {
                showModal('step');
                // When submitting input from modal after step, use stepInstruction instead
                document.getElementById('user-input').setAttribute('data-mode', 'step');
            }
        })
        .catch(error => {
            console.error('Error executing instruction:', error);
            appendToConsole(`Error: ${error.message}`);
        });
}


function changeColor() {
    var r = document.querySelector(':root');
    let inputs = [];
    for (let i = 0; i < 4; i++) {
        let userInput = prompt(`Enter 4 hexadecimal colors:`);
        if (userInput == "" || userInput == null) {
            break;
        }
        if (userInput[0] != '#') {
            userInput = "#" + userInput
        }
        if (userInput.length > 7) {
            userInput = userInput.slice(0, 7)
        }
        inputs.push(userInput);
    }
    if (inputs.length == 4) {
        r.style.setProperty('--backdrop', inputs[0])
        //localStorage.setItem("--backdrop", str(inputs[0]))
        r.style.setProperty('--background', inputs[1])
        //localStorage.setItem("--background", str(inputs[1]))
        r.style.setProperty('--primary', inputs[2])
        //localStorage.setItem("--primary", str(inputs[2]))
        r.style.setProperty('--secondary', inputs[3])
        //localStorage.setItem("--secondary", str(inputs[3]))
    }
}

// quick attempt at saving the config, didn't work but might be useful dead code regardless

/*
function getCookies() {
    document.getElementById("refresh").addEventListener("click", (event) => {
        window.location.reload();
      });
    if(localStorage.getItem("--backdrop") != null)
        document.documentElement.style.setProperty("--backdrop", localStorage.getItem("--backdrop"));
    if(localStorage.getItem("--background") != null)
        document.documentElement.style.setProperty("--background", localStorage.getItem("--background"));
    if(localStorage.getItem("--primary") != null)
        document.documentElement.style.setProperty("--primary", localStorage.getItem("--primary"));
    if(localStorage.getItem("--secondary") != null)
        document.documentElement.style.setProperty("--secondary", localStorage.getItem("--secondary"));
}
*/

function saveFile() {
    // Create a temporary anchor element for saving
    const link = document.createElement('a');

    // Create the content to save
    let content = '';
    fetch(`${API_BASE}/get_memory`)
        .then(response => response.json())
        .then(data => {
            // Create content string from memory
            content = data.memory.join('\n');

            // Create a Blob with the content
            const blob = new Blob([content], { type: 'text/plain' });

            // Create a URL for the Blob
            const url = window.URL.createObjectURL(blob);

            // Setup the download link
            link.href = url;
            link.download = 'program.txt'; // Default filename

            // Trigger the download
            link.click();

            // Cleanup
            window.URL.revokeObjectURL(url);
        })
        .catch(err => {
            console.error("Save error:", err);
            alert("Something went wrong while saving the file.");
        });
}

// Fetch memory and status on page load
window.onload = fetchMemory;

// window.onload = getCookies;