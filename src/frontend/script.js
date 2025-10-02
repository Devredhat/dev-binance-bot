class TradingBotUI {
    constructor() {
        this.isConnected = false;
        this.currentTab = 'market';
        this.initializeEventListeners();
        this.addLog('UI Initialized', 'info');
    }

    initializeEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Form submissions
        document.getElementById('marketForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.placeMarketOrder();
        });

        document.getElementById('limitForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.placeLimitOrder();
        });

        document.getElementById('ocoForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.placeOCOOrder();
        });

        // Test buttons
        document.getElementById('marketTest').addEventListener('click', () => {
            this.placeMarketOrder(true);
        });

        document.getElementById('limitTest').addEventListener('click', () => {
            this.placeLimitOrder(true);
        });

        document.getElementById('ocoTest').addEventListener('click', () => {
            this.placeOCOOrder(true);
        });

        // Connect button
        document.getElementById('connectBtn').addEventListener('click', () => {
            this.connectToBinance();
        });
    }

    switchTab(tabName) {
        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        this.currentTab = tabName;
        this.addLog(`Switched to ${tabName.toUpperCase()} orders`, 'info');
    }

    connectToBinance() {
        this.addLog('Connecting to Binance Testnet...', 'info');
        
        // Simulate API connection
        setTimeout(() => {
            this.isConnected = true;
            document.getElementById('status').textContent = 'Connected';
            document.getElementById('status').className = 'status-connected';
            document.getElementById('connectBtn').textContent = 'Connected ✓';
            document.getElementById('connectBtn').style.background = '#28a745';
            
            this.addLog('Successfully connected to Binance Testnet!', 'success');
            this.addLog('API Key verified and session initialized', 'success');
        }, 1500);
    }

    async placeMarketOrder(isTest = false) {
        const symbol = document.getElementById('marketSymbol').value;
        const side = document.getElementById('marketSide').value;
        const quantity = document.getElementById('marketQuantity').value;

        if (!this.validateInputs(symbol, side, quantity)) return;

        this.addLog(`Placing ${isTest ? 'TEST ' : ''}Market Order: ${side} ${quantity} ${symbol}`, 'info');

        try {
            const response = await this.callBackendAPI('/market-order', {
                symbol, side, quantity, test: isTest
            });

            this.displayResult(response, isTest);
        } catch (error) {
            this.displayError(error.message);
        }
    }

    async placeLimitOrder(isTest = false) {
        const symbol = document.getElementById('limitSymbol').value;
        const side = document.getElementById('limitSide').value;
        const quantity = document.getElementById('limitQuantity').value;
        const price = document.getElementById('limitPrice').value;

        if (!this.validateInputs(symbol, side, quantity, price)) return;

        this.addLog(`Placing ${isTest ? 'TEST ' : ''}Limit Order: ${side} ${quantity} ${symbol} @ $${price}`, 'info');

        try {
            const response = await this.callBackendAPI('/limit-order', {
                symbol, side, quantity, price, test: isTest
            });

            this.displayResult(response, isTest);
        } catch (error) {
            this.displayError(error.message);
        }
    }

    async placeOCOOrder(isTest = false) {
        const symbol = document.getElementById('ocoSymbol').value;
        const side = document.getElementById('ocoSide').value;
        const quantity = document.getElementById('ocoQuantity').value;
        const price = document.getElementById('ocoPrice').value;
        const stopPrice = document.getElementById('ocoStopPrice').value;
        const stopLimitPrice = document.getElementById('ocoStopLimitPrice').value;

        if (!this.validateInputs(symbol, side, quantity, price, stopPrice, stopLimitPrice)) return;

        this.addLog(`Placing ${isTest ? 'TEST ' : ''}OCO Order: ${side} ${quantity} ${symbol}`, 'info');

        try {
            const response = await this.callBackendAPI('/oco-order', {
                symbol, side, quantity, price, stopPrice, stopLimitPrice, test: isTest
            });

            this.displayResult(response, isTest);
        } catch (error) {
            this.displayError(error.message);
        }
    }

    validateInputs(symbol, side, quantity, ...prices) {
        if (!symbol.endsWith('USDT')) {
            this.displayError('Symbol must end with USDT (e.g., BTCUSDT)');
            return false;
        }

        if (parseFloat(quantity) < 0.001) {
            this.displayError('Quantity must be at least 0.001');
            return false;
        }

        for (const price of prices) {
            if (price && parseFloat(price) <= 0) {
                this.displayError('All prices must be positive numbers');
                return false;
            }
        }

        return true;
    }

    async callBackendAPI(endpoint, data) {
        // For demo purposes - in real implementation, this would call your Python backend
        // Using setTimeout to simulate API call delay
        
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (Math.random() < 0.9) { // 90% success rate for demo
                    const simulatedResponse = this.createSimulatedResponse(data);
                    resolve(simulatedResponse);
                } else {
                    reject(new Error('API Error: Insufficient balance or network issue'));
                }
            }, 2000);
        });
    }

    createSimulatedResponse(data) {
        const baseResponse = {
            orderId: Math.floor(Math.random() * 1000000),
            status: data.test ? 'FILLED' : 'NEW',
            symbol: data.symbol,
            side: data.side,
            quantity: data.quantity,
            timestamp: new Date().toISOString()
        };

        if (data.price) {
            baseResponse.price = data.price;
            baseResponse.type = 'LIMIT';
        } else if (data.stopPrice) {
            baseResponse.price = data.price;
            baseResponse.stopPrice = data.stopPrice;
            baseResponse.stopLimitPrice = data.stopLimitPrice;
            baseResponse.type = 'OCO';
            baseResponse.orderListId = Math.floor(Math.random() * 1000000);
        } else {
            baseResponse.type = 'MARKET';
            baseResponse.executedPrice = (Math.random() * 10000 + 30000).toFixed(2);
        }

        return baseResponse;
    }

    displayResult(result, isTest = false) {
        const resultsContainer = document.getElementById('results');
        const noOrders = resultsContainer.querySelector('.no-orders');
        
        if (noOrders) {
            noOrders.remove();
        }

        const resultDiv = document.createElement('div');
        resultDiv.className = `order-result ${isTest ? 'test' : 'success'}`;
        
        let resultHTML = `
            <strong>${isTest ? '🧪 TEST ' : '✅ '}Order Placed Successfully!</strong><br>
            Type: ${result.type} | Side: ${result.side} | Symbol: ${result.symbol}<br>
            Quantity: ${result.quantity} | Status: ${result.status}<br>
            Order ID: ${result.orderId}
        `;

        if (result.executedPrice) {
            resultHTML += `<br>Executed Price: $${parseFloat(result.executedPrice).toLocaleString()}`;
        } else if (result.price) {
            resultHTML += `<br>Price: $${parseFloat(result.price).toLocaleString()}`;
        }

        if (result.orderListId) {
            resultHTML += `<br>Order List ID: ${result.orderListId}`;
        }

        resultHTML += `<br><small>${new Date(result.timestamp).toLocaleString()}</small>`;

        resultDiv.innerHTML = resultHTML;
        resultsContainer.prepend(resultDiv);

        this.addLog(`Order ${result.orderId} placed successfully`, 'success');
    }

    displayError(message) {
        const resultsContainer = document.getElementById('results');
        const noOrders = resultsContainer.querySelector('.no-orders');
        
        if (noOrders) {
            noOrders.remove();
        }

        const errorDiv = document.createElement('div');
        errorDiv.className = 'order-result error';
        errorDiv.innerHTML = `
            <strong>❌ Order Failed</strong><br>
            ${message}<br>
            <small>${new Date().toLocaleString()}</small>
        `;

        resultsContainer.prepend(errorDiv);
        this.addLog(`Order failed: ${message}`, 'error');
    }

    addLog(message, type = 'info') {
        const logContainer = document.getElementById('logContainer');
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        
        const timestamp = new Date().toLocaleTimeString();
        logEntry.textContent = `[${timestamp}] ${message}`;
        
        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
    }
}

// Initialize the UI when page loads
document.addEventListener('DOMContentLoaded', () => {
    new TradingBotUI();
});