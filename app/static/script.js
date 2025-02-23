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
                input.addEventListener("blur", function() {
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

function showModal() {
    let modal = document.getElementById('input-modal');
    modal.classList.remove('hidden'); // Show modal
    modal.style.display = 'flex'; // Ensure it's visible
    document.getElementById('user-input').focus();
}

function hideModal() {
    let modal = document.getElementById('input-modal');
    modal.classList.add('hidden'); // Hide modal
    modal.style.display = 'none';
}


function submitInput() {
    let userInputField = document.getElementById('user-input');
    let userInput = userInputField.value.trim(); // Get and trim input value

    if (userInput === "") {
        alert("Please enter a value."); // Prevent empty submission
        return;
    }

    hideModal(); // Hide the modal
    userInputField.value = ""; // Clear input field after submission

    executeInstruction(userInput); // Pass input to the execution function
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
    let fileInput = document.getElementById('file-input');
    let file = fileInput.files[0]; // Get the selected file

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
        alert(data.message);
        fetchMemory(); // Refresh memory after loading file
    })
    .catch(error => console.error('Error loading file:', error));
}

// Fetch memory and status on page load
window.onload = fetchMemory;
