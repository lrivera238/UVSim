const API_BASE = '/api';

let activeTabId = null; // Stores the ID of the currently active tab
let tabs = []; // Array to store tab information
let consoleMessages = {}; // Object to store console messages for each tab

// Initial load
window.onload = function () {
    // Check for existing tabs
    fetchTabs();
};

// ===== Tab Management Functions =====

function fetchTabs() {
    fetch(`${API_BASE}/list_instances`)
        .then(response => response.json())
        .then(data => {
            tabs = data.instances;
            renderTabs();

            // If there are tabs, activate the first one
            if (tabs.length > 0) {
                activateTab(tabs[0].tab_id);
            } else {
                // Show no tabs message
                document.getElementById('no-tabs-message').style.display = 'block';
                document.getElementById('main-content').style.display = 'none';
            }
        })
        .catch(error => console.error('Error fetching tabs:', error));
}

function renderTabs() {
    const tabsContainer = document.getElementById('program-tabs');

    // Clear existing tabs, keeping only the "New Tab" button
    const newTabButton = document.getElementById('new-tab-button');
    tabsContainer.innerHTML = '';
    tabsContainer.appendChild(newTabButton);

    // Add all tabs
    tabs.forEach(tab => {
        const tabElement = document.createElement('button');
        tabElement.classList.add('tab');
        if (tab.tab_id === activeTabId) {
            tabElement.classList.add('active');
        }

        // Tab label
        const tabLabel = document.createElement('span');
        tabLabel.textContent = tab.name;
        tabElement.appendChild(tabLabel);

        // Close button
        const closeButton = document.createElement('span');
        closeButton.classList.add('tab-close');
        closeButton.innerHTML = '&times;';
        closeButton.onclick = (e) => {
            e.stopPropagation(); // Prevent tab activation when closing
            deleteTab(tab.tab_id);
        };
        tabElement.appendChild(closeButton);

        // Tab click handler
        tabElement.onclick = () => activateTab(tab.tab_id);

        // Insert tab before the New Tab button
        tabsContainer.insertBefore(tabElement, newTabButton);
    });
}

function createNewTab() {
    fetch(`${API_BASE}/create_instance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: `Program ${tabs.length + 1}` })
    })
        .then(response => response.json())
        .then(data => {
            // Add new tab to the list and activate it
            tabs.push({
                tab_id: data.tab_id,
                name: data.name
            });
            renderTabs();
            activateTab(data.tab_id);
        })
        .catch(error => console.error('Error creating new tab:', error));
}

function activateTab(tabId) {
    activeTabId = tabId;

    // Update UI to show this tab is active
    renderTabs();

    // Show main content
    document.getElementById('no-tabs-message').style.display = 'none';
    document.getElementById('main-content').style.display = 'grid';

    // Show console messages for this tab
    const consoleElement = document.getElementById('execution-message');
    consoleElement.innerHTML = '';

    // Check if we have stored messages for this tab
    if (consoleMessages[tabId]) {
        // Add all stored messages back to the console
        consoleMessages[tabId].forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.textContent = message;
            consoleElement.appendChild(messageElement);
        });

        // Ensure console is scrolled to the bottom
        setTimeout(() => {
            consoleElement.scrollTop = consoleElement.scrollHeight;
        }, 0);
    }

    // Fetch the data for this tab
    fetchMemory();
}

function deleteTab(tabId) {
    if (confirm('Are you sure you want to close this program? All unsaved changes will be lost.')) {
        fetch(`${API_BASE}/delete_instance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tab_id: tabId })
        })
            .then(response => response.json())
            .then(data => {
                // Remove the tab from our list
                tabs = tabs.filter(tab => tab.tab_id !== tabId);

                // If we deleted the active tab, activate another one if available
                if (tabId === activeTabId) {
                    if (tabs.length > 0) {
                        activateTab(tabs[0].tab_id);
                    } else {
                        // No tabs left
                        activeTabId = null;
                        document.getElementById('no-tabs-message').style.display = 'block';
                        document.getElementById('main-content').style.display = 'none';
                    }
                }

                renderTabs();
            })
            .catch(error => console.error('Error deleting tab:', error));
    }
}

function renameTab() {
    if (!activeTabId) return;

    // Find the current tab name
    const currentTab = tabs.find(tab => tab.tab_id === activeTabId);
    if (!currentTab) return;

    // Show rename modal with current name
    const modal = document.getElementById('rename-modal');
    const input = document.getElementById('tab-name-input');
    input.value = currentTab.name;

    modal.classList.remove('hidden');
    modal.style.display = 'flex';
    input.focus();
}

function submitRename() {
    const newName = document.getElementById('tab-name-input').value.trim();
    if (newName) {
        fetch(`${API_BASE}/rename_instance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tab_id: activeTabId,
                name: newName
            })
        })
            .then(response => response.json())
            .then(data => {
                // Update local data
                const tabIndex = tabs.findIndex(tab => tab.tab_id === activeTabId);
                if (tabIndex !== -1) {
                    tabs[tabIndex].name = newName;
                    renderTabs();
                }
                // Close the modal
                cancelRename();
            })
            .catch(error => console.error('Error renaming tab:', error));
    }
}

function cancelRename() {
    const modal = document.getElementById('rename-modal');
    modal.classList.add('hidden');
    modal.style.display = 'none';
}

// ===== UVSim Functions =====

function updateMemory(address, value) {
    if (!activeTabId) return;

    fetch(`${API_BASE}/update_memory?tab_id=${activeTabId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tab_id: activeTabId,
            address: address,
            value: value.trim()
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            fetchMemory(); // Refresh memory UI after update
        })
        .catch(error => console.error('Error updating memory:', error));
}

function fetchMemory() {
    if (!activeTabId) return;

    fetch(`${API_BASE}/get_memory?tab_id=${activeTabId}&nocache=${new Date().getTime()}`)
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
    if (!activeTabId) return Promise.resolve({});

    return fetch(`${API_BASE}/get_status?tab_id=${activeTabId}&nocache=${new Date().getTime()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('accumulator').innerText = data.accumulator;
            document.getElementById('instruction-pointer').innerText = data.instruction_pointer;
            return data; // Return the status so fetchMemory() can use it
        })
        .catch(error => {
            console.error('Error fetching status:', error);
            return {};
        });
}

function executeInstruction(userInput = null) {
    if (!activeTabId) return;

    isRunning = true; // Set running state

    fetch(`${API_BASE}/step_instruction`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tab_id: activeTabId,
            input: userInput
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);

            // Only write Output messages and program halted to the console
            if (data.message.includes("Output")) {
                appendToConsole(data.message);
            }
            // Only show invalid instructions and program halted, NOT input required
            else if (data.message.includes("Invalid") ||
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

    // Store the message in our tab-specific console messages
    if (!consoleMessages[activeTabId]) {
        consoleMessages[activeTabId] = [];
    }
    consoleMessages[activeTabId].push(message);

    // Ensure auto-scrolling works consistently by using setTimeout
    setTimeout(() => {
        consoleElement.scrollTop = consoleElement.scrollHeight;
    }, 0);
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

    // Validate input is a number within the allowed range
    const numValue = Number(userInput);
    if (isNaN(numValue)) {
        alert("Please enter a valid number.");
        return;
    }

    if (numValue > 999999 || numValue < -999999) {
        alert("Input must be between -999999 and 999999.");
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
    if (!activeTabId) return;

    fetch(`${API_BASE}/reset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tab_id: activeTabId })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);

            // Clear the console and stored messages for this tab
            document.getElementById('execution-message').innerHTML = '';
            consoleMessages[activeTabId] = [];

            // Add reset message to console
            appendToConsole(data.message);
            fetchMemory();  // Refresh memory after reset
            fetchStatus();  // Refresh accumulator and instruction pointer
        })
        .catch(error => console.error('Error resetting system:', error));
}

function loadFile() {
    if (!activeTabId) {
        alert("Please create a new program tab first before loading a file.");
        return;
    }

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

        // Create form data with file and tab ID
        const formData = new FormData();
        formData.append("file", file);
        formData.append("tab_id", activeTabId);

        // Show loading indicator in console
        appendToConsole(`Loading file: ${file.name}...`);

        fetch(`${API_BASE}/load_file`, {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    // Always refresh memory display in case of error (memory might have been reset)
                    fetchMemory();
                    // Also log the error to the execution console
                    appendToConsole(`Error: ${data.message}`);
                } else {
                    appendToConsole(`Success: ${data.message}`);
                    fetchMemory(); // Refresh memory after loading file
                }
            })
            .catch(error => {
                console.error('Error loading file:', error);
                appendToConsole(`Error loading file: ${error.message}`);
                alert('Error loading file. Please check the console for details.');
            });
    });

    // Trigger the file selection dialog
    fileInput.click();
}

function stepInstruction(userInput = null) {
    if (!activeTabId) return;

    fetch(`${API_BASE}/step_instruction`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tab_id: activeTabId,
            input: userInput
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);

            // Always append execution messages to console for better visibility
            appendToConsole(data.message);

            // Additional scrolling for step function to ensure it scrolls properly
            setTimeout(() => {
                let consoleElement = document.getElementById('execution-message');
                consoleElement.scrollTop = consoleElement.scrollHeight;
            }, 10);

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

function saveFile() {
    if (!activeTabId) return;

    // Create a temporary anchor element for saving
    const link = document.createElement('a');

    // Create the content to save
    let content = '';
    fetch(`${API_BASE}/get_memory?tab_id=${activeTabId}`)
        .then(response => response.json())
        .then(data => {
            // Create content string from memory
            content = data.memory.join('\n');

            // Create a Blob with the content
            const blob = new Blob([content], { type: 'text/plain' });

            // Create a URL for the Blob
            const url = window.URL.createObjectURL(blob);

            // Get the tab name for the filename
            const tabName = tabs.find(tab => tab.tab_id === activeTabId)?.name || 'program';

            // Setup the download link
            link.href = url;
            link.download = `${tabName}.txt`; // Use tab name for the filename

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
        r.style.setProperty('--background', inputs[1])
        r.style.setProperty('--primary', inputs[2])
        r.style.setProperty('--secondary', inputs[3])
    }
}