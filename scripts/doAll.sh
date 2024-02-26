#!/bin/bash

# Function to get all running processes and then kill all
# of them but the current running process.
kill_all_except_current() {
    current_pid=$$
    all_processes=$(ps -eo pid)
    while read -r pid; do
        if [[ $pid -ne $current_pid ]]; then
            kill $pid >/dev/null 2>&1
            sleep 2
        fi
    done <<< "$all_processes"
}

echo "Json Schema Discovery - Experiment replication"
echo "Based on the paper 'An Approach for Schema Extraction of JSON and Extended JSON Document Collections' by Frozza A. et al."
echo "Welcome"
echo "Edgar Yepez - University of Passau"
echo "------"
echo "Killing all running processes for a clean start..."
kill_all_except_current
#ps aux | grep -E 'node|ng|sh' | grep -v grep | awk '{print $2}' | xargs kill -9

echo "Checking for MongoDB status..."
# Check if mongod process is running.
if pgrep -x "mongod" > /dev/null
then
    echo "MongoDB is running."
else
	# Start mongo daemon in background.
	echo "Starting MongoDB..."
	/usr/bin/mongod --config /etc/mongodb.conf &
	# Wait for a short duration to allow daemon to start.
	sleep 7
fi

# mongo database parameters.
HOST="localhost"
PORT="27017"
DATABASE="repeng"
COLLECTION="schema_discovery"
JSON_FILE="data_source/firenze_checkins.json"
OUTPUT_FILE="experiment/firenze_checkins_generated_schema.json"
REFERENCE_FILE="experiment/firenze_checkins_reference_schema.json"
DIFF_OUTPUT_FILE="experiment/firenze_checkins_diff.json"
SUMMARY_OUTPUT_FILE="experiment/firenze_checkins_summary.txt"

echo "Checking for experiment data set..."

# Check if the mongo database and collection exist, and create them if not.
if ! mongo --host $HOST --port $PORT --quiet --eval "db.getSiblingDB('$DATABASE').getCollectionNames().indexOf('$COLLECTION') != -1" | grep "true" > /dev/null; then
    echo "Collection $COLLECTION does not exist in database $DATABASE. Creating..."
    mongo --host $HOST --port $PORT --quiet --eval "db.getSiblingDB('$DATABASE').createCollection('$COLLECTION')"
else
	echo "Collection $COLLECTION is already present in database $DATABASE."
fi

# Check if there are documents in the collection, and add them if not.
document_count=$(mongo --host $HOST --port $PORT --quiet --eval "db.getSiblingDB('$DATABASE').$COLLECTION.count()")
if [ "$document_count" -eq 0 ]; then
    echo "No documents found in collection $COLLECTION. Inserting documents from $JSON_FILE..."
    mongoimport --host $HOST --port $PORT --db $DATABASE --collection $COLLECTION --file $JSON_FILE
else
    echo "Collection $COLLECTION in database $DATABASE contains $document_count documents."
fi

echo "Starting web application..."
npm run dev > /dev/null &

echo "Sleeping for 120 seconds to let the web application start."
sleep 120

echo "------"
echo "Beginning of experiment."
python3 main_experiment.py $HOST $PORT $DATABASE $COLLECTION $OUTPUT_FILE false

echo "Computing diff..."
python3 json_deepdiff.py $REFERENCE_FILE $OUTPUT_FILE $DIFF_OUTPUT_FILE $SUMMARY_OUTPUT_FILE

echo "------"
echo "Accessing the report directory and building the report document main.pdf..."
cd report
make clean > /dev/null
make >/dev/null 2>&1
cd ..

echo "------"
echo "End of experiment."