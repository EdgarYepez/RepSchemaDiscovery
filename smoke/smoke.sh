#!/bin/bash

# Run ng serve in the background.
ng serve &

# Capture the process ID of the ng serve command.
ng_serve_pid=$!

# Wait for a short duration to allow ng serve to start.
sleep 120

# Check if the ng serve process is still running.
if ps -p $ng_serve_pid > /dev/null; then
    echo "ng serve is running with process ID $ng_serve_pid."
    exit 0  # Success
else
    echo "Failed to start ng serve."
    exit 1  # Failure
fi
