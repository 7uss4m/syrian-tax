#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock Server for Syria Tax API Testing
=====================================

This script creates a local mock server that simulates the Syrian Tax API endpoints.
Use this for testing the Odoo module without connecting to the real tax system.

Run with: python mock_server.py
"""

from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import random
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Mock data storage
mock_tokens = {}
mock_bills = {}

@app.route('/Taxapi/api/account/login', methods=['POST'])
def mock_login():
    """Mock login endpoint"""
    data = request.get_json()

    if not data:
        return jsonify({"succeed": False, "message": "Invalid JSON"}), 400

    username = data.get('userName')
    password = data.get('passWord')
    tax_number = data.get('taxNumber')

    # Simple validation
    if not all([username, password, tax_number]):
        return jsonify({"succeed": False, "message": "Missing required fields"}), 400

    if len(tax_number) != 12 or not tax_number.isdigit():
        return jsonify({"succeed": False, "message": "Invalid tax number format"}), 400

    # Mock successful login
    token = f"mock_token_{uuid.uuid4()}"
    mock_tokens[token] = {
        'username': username,
        'tax_number': tax_number,
        'facilityName': f"Mock Facility for {tax_number}",
        'created_at': datetime.now()
    }

    return jsonify({
        "data": {
            "token": token,
            "facilityName": f"Mock Facility for {tax_number}"
        },
        "succeed": True,
        "message": "تم تسجيل الدخول بنجاح"
    })

@app.route('/Taxapi/api/Bill/CheckBill', methods=['POST'])
def mock_check_bill():
    """Mock check bill endpoint"""
    data = request.get_json()

    if not data:
        return jsonify({"succeed": False, "message": "Invalid JSON"}), 400

    code = data.get('code')
    code_type = data.get('codeType')

    if not code or code_type not in [1, 2]:
        return jsonify({"succeed": False, "message": "Invalid code or codeType"}), 400

    # Check if bill exists in mock storage
    if code in mock_bills:
        bill = mock_bills[code]
        return jsonify({
            "data": {
                "billValue": bill['billValue'],
                "billDate": bill['billDate'],
                "facilityName": bill['facilityName']
            },
            "succeed": True,
            "message": "TaskCompletedSuccfessfully"
        })
    else:
        return jsonify({"succeed": False, "message": "BillNotFound"})

@app.route('/Taxapi/api/Bill/AddFullBill', methods=['POST'])
def mock_add_bill():
    """Mock add bill endpoint"""
    # Check authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"succeed": False, "message": "Unauthorized"}), 401

    token = auth_header.split(' ')[1]
    if token not in mock_tokens:
        return jsonify({"succeed": False, "message": "Invalid token"}), 401

    data = request.get_json()

    if not data:
        return jsonify({"succeed": False, "message": "Invalid JSON"}), 400

    # Validate required fields
    required_fields = ['billValue', 'billNumber', 'code', 'currency', 'exProgram', 'date']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"succeed": False, "message": f"Missing fields: {', '.join(missing_fields)}"}), 400

    bill_code = data['code']

    # Check if bill already exists
    if bill_code in mock_bills:
        return jsonify({"succeed": False, "message": "BillAlreadyExists"}), 400

    # Generate mock random number
    random_number = str(random.randint(100000000, 999999999))

    # Store bill
    mock_bills[bill_code] = {
        'billValue': data['billValue'],
        'billNumber': data['billNumber'],
        'code': bill_code,
        'currency': data['currency'],
        'exProgram': data['exProgram'],
        'date': data['date'],
        'facilityName': mock_tokens[token]['facilityName'],
        'billDate': datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        'randomNumber': random_number,
        'created_at': datetime.now()
    }

    return jsonify({
        "data": {
            "code": bill_code,
            "billDate": mock_bills[bill_code]['billDate'],
            "randomNumber": random_number
        },
        "succeed": True,
        "message": "تم إضافة الفاتورة بنجاح"
    })

@app.route('/Taxapi/api/account/AccountingSoftwarelogin', methods=['POST'])
def mock_accounting_login():
    """Mock accounting software login endpoint"""
    # Same as regular login for testing
    return mock_login()

@app.route('/mock/status', methods=['GET'])
def mock_status():
    """Get mock server status"""
    return jsonify({
        "status": "running",
        "bills_count": len(mock_bills),
        "tokens_count": len(mock_tokens),
        "server_time": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Syria Tax API Mock Server...")
    print("Login URL: http://localhost:5000/Taxapi/api/account/login")
    print("Check Bill URL: http://localhost:5000/Taxapi/api/Bill/CheckBill")
    print("Add Bill URL: http://localhost:5000/Taxapi/api/Bill/AddFullBill")
    print("Status URL: http://localhost:5000/mock/status")
    print("Use test credentials:")
    print("   - Username: testpos3")
    print("   - Password: A@123456789")
    print("   - Tax Number: 000000000000")
    print("Press Ctrl+C to stop")

    app.run(debug=True, host='0.0.0.0', port=5000)