from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/market-order', methods=['POST'])
def market_order():
    data = request.json
    symbol = data['symbol']
    side = data['side']
    quantity = data['quantity']
    test_mode = data.get('test', False)
    
    try:
        # Call your existing market_orders.py
        cmd = ['python', '../src/market_orders.py', symbol, side, quantity]
        if test_mode:
            cmd.append('--test')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Market order placed successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/limit-order', methods=['POST'])
def limit_order():
    data = request.json
    symbol = data['symbol']
    side = data['side']
    quantity = data['quantity']
    price = data['price']
    test_mode = data.get('test', False)
    
    try:
        cmd = ['python', '../src/limit_orders.py', symbol, side, quantity, price]
        if test_mode:
            cmd.append('--test')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Limit order placed successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/oco-order', methods=['POST'])
def oco_order():
    data = request.json
    symbol = data['symbol']
    side = data['side']
    quantity = data['quantity']
    price = data['price']
    stop_price = data['stopPrice']
    stop_limit_price = data['stopLimitPrice']
    test_mode = data.get('test', False)
    
    try:
        cmd = [
            'python', '../src/advanced/oco.py', 
            symbol, side, quantity, price, stop_price, stop_limit_price
        ]
        if test_mode:
            cmd.append('--test')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'OCO order placed successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)