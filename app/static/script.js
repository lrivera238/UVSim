function updateMemory(address, value) {
    fetch('/api/update_memory', {
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
    fetch('/api/get_memory')
    .then(response => response.json())
    .then(data => {
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
        });
    })
    .catch(error => console.error('Error fetching memory:', error));
}

function fetchStatus() {
    fetch('/api/get_status')
    .then(response => response.json())
    .then(data => {
        document.getElementById('accumulator').innerText = data.accumulator;
        document.getElementById('instruction-pointer').innerText = data.instruction_pointer;
    })
    .catch(error => console.error('Error fetching status:', error));
}

function executeInstruction(userInput = null) {
    fetch('/api/step_instruction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: userInput }) // Send user input if needed
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('execution-message').innerText = data.message;

        // Update system status after each instruction
        fetchStatus();

        if (data.waitForInput) {
            document.getElementById('input-container').style.display = 'block';
            document.getElementById('user-input').focus();
        } else {
            document.getElementById('input-container').style.display = 'none';

            if (!data.halt) {
                executeInstruction(); // Continue execution automatically
            }
        }
    })
    .catch(error => console.error('Error executing instruction:', error));
}

function submitInput() {
    let userInput = document.getElementById('user-input').value;
    executeInstruction(userInput);  // Pass input to the execution function
}

function resetSystem() {
    fetch('/api/reset', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('execution-message').innerText = data.message;
        fetchMemory();  // Refresh memory after reset
        fetchStatus();  // Refresh accumulator and instruction pointer
    })
    .catch(error => console.error('Error resetting system:', error));
}


// Fetch memory and status on page load
window.onload = fetchMemory;
