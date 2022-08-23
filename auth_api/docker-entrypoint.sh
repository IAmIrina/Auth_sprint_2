#!/bin/bash

# Wait when DB Ready for connection
echo "Wait db ready to connect"
python wait_for_postgres.py

# Apply database migrations
echo "Apply database migrations"
flask db upgrade

# Run tests
echo "Tests"
pytest -s -vv --disable-warnings

# Start server
echo "Starting server"
python app.py run
