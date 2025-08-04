let currentInput = '';
let previousInput = '';
let operator = null;
let shouldReset = false;

function updateDisplay() {
    const display = document.getElementById('mainDisplay');
    display.textContent = currentInput || '0';
}

function updateHistory(text) {
    const history = document.getElementById('historyDisplay');
    history.textContent = text;
}

function showError(message) {
    const errorEl = document.getElementById('errorMessage');
    errorEl.textContent = message;
    errorEl.style.display = 'block';
    setTimeout(() => {
        errorEl.style.display = 'none';
    }, 3000);
}

function appendNumber(num) {
    if (shouldReset) {
        currentInput = '';
        shouldReset = false;
    }
    
    if (currentInput === '0') {
        currentInput = num;
    } else {
        currentInput += num;
    }
    updateDisplay();
}

function appendDecimal() {
    if (shouldReset) {
        currentInput = '0';
        shouldReset = false;
    }
    
    if (!currentInput.includes('.')) {
        if (!currentInput) currentInput = '0';
        currentInput += '.';
        updateDisplay();
    }
}

function appendOperator(op) {
    if (currentInput) {
        if (operator && !shouldReset) {
            calculate();
        }
        
        previousInput = currentInput;
        operator = op;
        shouldReset = true;
        
        updateHistory(`${previousInput} ${op}`);
    }
}

function appendConstant(constant) {
    if (shouldReset) {
        currentInput = '';
        shouldReset = false;
    }
    
    if (constant === 'pi') {
        currentInput += 'pi';
    } else if (constant === 'e') {
        currentInput += 'e';
    }
    updateDisplay();
}

function clearAll() {
    currentInput = '';
    previousInput = '';
    operator = null;
    shouldReset = false;
    updateDisplay();
    updateHistory('');
}

function clearEntry() {
    currentInput = '';
    updateDisplay();
}

function backspace() {
    if (currentInput && !shouldReset) {
        currentInput = currentInput.slice(0, -1);
        updateDisplay();
    }
}

function toggleSign() {
    if (currentInput && currentInput !== '0') {
        if (currentInput.startsWith('-')) {
            currentInput = currentInput.slice(1);
        } else {
            currentInput = '-' + currentInput;
        }
        updateDisplay();
    }
}

async function calculate() {
    if (!operator || !previousInput || !currentInput) return;
    
    try {
        const expression = `${previousInput}${operator}${currentInput}`;
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expression })
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateHistory(`${previousInput} ${operator} ${currentInput} =`);
            currentInput = String(data.result);
            operator = null;
            previousInput = '';
            shouldReset = true;
        } else {
            showError(data.error);
        }
        
        updateDisplay();
    } catch (error) {
        showError('Calculation error: ' + error.message);
    }
}

async function applyFunction(funcName) {
    if (!currentInput) return;
    
    try {
        const response = await fetch('/api/function', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                function: funcName, 
                value: parseFloat(currentInput) 
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateHistory(`${funcName}(${currentInput}) =`);
            currentInput = String(data.result);
            shouldReset = true;
        } else {
            showError(data.error);
        }
        
        updateDisplay();
    } catch (error) {
        showError('Function error: ' + error.message);
    }
}

function switchMode(mode) {
    const basicMode = document.getElementById('basicMode');
    const advancedMode = document.getElementById('advancedMode');
    const buttons = document.querySelectorAll('.mode-btn');
    
    buttons.forEach(btn => btn.classList.remove('active'));
    
    if (mode === 'basic') {
        basicMode.style.display = 'block';
        advancedMode.style.display = 'none';
        buttons[0].classList.add('active');
    } else {
        basicMode.style.display = 'none';
        advancedMode.style.display = 'block';
        buttons[1].classList.add('active');
    }
}

// Keyboard support
document.addEventListener('keydown', (event) => {
    const key = event.key;
    
    if (key >= '0' && key <= '9') {
        appendNumber(key);
    } else if (key === '.') {
        appendDecimal();
    } else if (key === '+') {
        appendOperator('+');
    } else if (key === '-') {
        appendOperator('-');
    } else if (key === '*') {
        appendOperator('*');
    } else if (key === '/') {
        event.preventDefault();
        appendOperator('/');
    } else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculate();
    } else if (key === 'Escape') {
        clearAll();
    } else if (key === 'Backspace') {
        backspace();
    }
});

// Initialize display on page load
updateDisplay();