#!/bin/bash

echo "===================================="
echo "Syria Tax API Mock Server"
echo "===================================="
echo ""
echo "Starting mock server on http://localhost:5000"
echo ""
echo "Test endpoints:"
echo "- Login: POST http://localhost:5000/Taxapi/api/account/login"
echo "- Check Bill: POST http://localhost:5000/Taxapi/api/Bill/CheckBill"
echo "- Add Bill: POST http://localhost:5000/Taxapi/api/Bill/AddFullBill"
echo "- Status: GET http://localhost:5000/mock/status"
echo ""
echo "Test credentials:"
echo "- Username: testpos3"
echo "- Password: A@123456789"
echo "- Tax Number: 000000000000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================="
echo ""

python3 mock_server.py