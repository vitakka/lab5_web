#!/bin/bash

echo "=== Starting Gunicorn Production Server ==="
gunicorn --bind 127.0.0.1:5000 wsgi:app &
APP_PID=$!

sleep 10

echo "Gunicorn PID: $APP_PID"

if kill -0 $APP_PID 2>/dev/null; then
    echo "✅ Gunicorn is running successfully on http://127.0.0.1:5000"
    echo "⏳ Letting it run for 5 seconds..."
    sleep 5
    echo "🛑 Stopping Gunicorn..."
    kill -TERM $APP_PID
    wait $APP_PID 2>/dev/null
    echo "✅ Gunicorn process stopped gracefully"
else
    echo "❌ ERROR: Gunicorn failed to start"
    exit 1
fi

echo "=== Script completed successfully ==="
exit 0