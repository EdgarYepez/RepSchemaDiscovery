import sys
import requests
import subprocess
import re
import time
import json

class BatchSummary:
	
	def __init__(self, batch_id, user_id, status, data_type, db_uri, collection_name, date, _id, created_at, updated_at, _v):
		self.batch_id = batch_id
		self.user_id = user_id
		self.status = status
		self.data_type = data_type
		self.db_uri = db_uri
		self.collection_name = collection_name
		self.date = date
		self._id = _id
		self.created_at = created_at
		self.updated_at = updated_at
		self._v = _v

	def from_dict(data_dict):
		return BatchSummary(
			batch_id=data_dict.get('batchId'),
			user_id=data_dict.get('userId'),
			status=data_dict.get('status'),
			data_type=data_dict.get('type'),
			db_uri=data_dict.get('dbUri'),
			collection_name=data_dict.get('collectionName'),
			date=data_dict.get('date'),
			_id=data_dict.get('_id'),
			created_at=data_dict.get('createdAt'),
			updated_at=data_dict.get('updatedAt'),
			_v=data_dict.get('__v')
		)

	def to_dict(self):
		return {
			'batchId': self.batch_id,
			'userId': self.user_id,
			'status': self.status,
			'type': self.data_type,
			'dbUri': self.db_uri,
			'collectionName': self.collection_name,
			'date': self.date,
			'_id': self._id,
			'createdAt': self.created_at,
			'updatedAt': self.updated_at,
			'__v': self._v
		}
	
class Batch:
	
	def __init__(self, _id, collection_name, db_uri, user_id, start_date, status, raw_schema_format, created_at, updated_at, _v,
				 collection_count, extraction_date, ordered_aggregation_date, ordered_map_reduce_date, reduce_type,
				 unique_unordered_count, unordered_aggregation_date, unordered_map_reduce_date, unique_ordered_count,
				 union_date, end_date, status_type):
		self._id = _id
		self.collection_name = collection_name
		self.db_uri = db_uri
		self.user_id = user_id
		self.start_date = start_date
		self.status = status
		self.raw_schema_format = raw_schema_format
		self.created_at = created_at
		self.updated_at = updated_at
		self._v = _v
		self.collection_count = collection_count
		self.extraction_date = extraction_date
		self.ordered_aggregation_date = ordered_aggregation_date
		self.ordered_map_reduce_date = ordered_map_reduce_date
		self.reduce_type = reduce_type
		self.unique_unordered_count = unique_unordered_count
		self.unordered_aggregation_date = unordered_aggregation_date
		self.unordered_map_reduce_date = unordered_map_reduce_date
		self.unique_ordered_count = unique_ordered_count
		self.union_date = union_date
		self.end_date = end_date
		self.status_type = status_type

	def from_dict(data_dict):
		return Batch(
			_id=data_dict.get('_id'),
			collection_name=data_dict.get('collectionName'),
			db_uri=data_dict.get('dbUri'),
			user_id=data_dict.get('userId'),
			start_date=data_dict.get('startDate'),
			status=data_dict.get('status'),
			raw_schema_format=data_dict.get('rawSchemaFormat'),
			created_at=data_dict.get('createdAt'),
			updated_at=data_dict.get('updatedAt'),
			_v=data_dict.get('__v'),
			collection_count=data_dict.get('collectionCount'),
			extraction_date=data_dict.get('extractionDate'),
			ordered_aggregation_date=data_dict.get('orderedAggregationDate'),
			ordered_map_reduce_date=data_dict.get('orderedMapReduceDate'),
			reduce_type=data_dict.get('reduceType'),
			unique_unordered_count=data_dict.get('uniqueUnorderedCount'),
			unordered_aggregation_date=data_dict.get('unorderedAggregationDate'),
			unordered_map_reduce_date=data_dict.get('unorderedMapReduceDate'),
			unique_ordered_count=data_dict.get('uniqueOrderedCount'),
			union_date=data_dict.get('unionDate'),
			end_date=data_dict.get('endDate'),
			status_type=data_dict.get('statusType')
		)

	def to_dict(self):
		return {
			'_id': self._id,
			'collectionName': self.collection_name,
			'dbUri': self.db_uri,
			'userId': self.user_id,
			'startDate': self.start_date,
			'status': self.status,
			'rawSchemaFormat': self.raw_schema_format,
			'createdAt': self.created_at,
			'updatedAt': self.updated_at,
			'__v': self._v,
			'collectionCount': self.collection_count,
			'extractionDate': self.extraction_date,
			'orderedAggregationDate': self.ordered_aggregation_date,
			'orderedMapReduceDate': self.ordered_map_reduce_date,
			'reduceType': self.reduce_type,
			'uniqueUnorderedCount': self.unique_unordered_count,
			'unorderedAggregationDate': self.unordered_aggregation_date,
			'unorderedMapReduceDate': self.unordered_map_reduce_date,
			'uniqueOrderedCount': self.unique_ordered_count,
			'unionDate': self.union_date,
			'endDate': self.end_date,
			'statusType': self.status_type
		}
	
class SchemaInfo:
	
	def __init__(self, _id, batch_id, json_schema, created_at, updated_at, _v):
		self._id = _id
		self.batch_id = batch_id
		self.json_schema = json_schema
		self.created_at = created_at
		self.updated_at = updated_at
		self._v = _v
		
	def from_dict(data_dict):
		return SchemaInfo(
			_id=data_dict.get('_id'),
			batch_id=data_dict.get('batchId'),
			json_schema=data_dict.get('jsonSchema'),
			created_at=data_dict.get('createdAt'),
			updated_at=data_dict.get('updatedAt'),
			_v=data_dict.get('__v')
		)
	
	def get_schema_as_string(self):
		return json.dumps(self.json_schema)

	def to_dict(self):
		return {
			'_id': self._id,
			'batchId': self.batch_id,
			'jsonSchema': self.json_schema,
			'createdAt': self.created_at,
			'updatedAt': self.updated_at,
			'__v': self._v
		}

class ApiClient:
	
	def __init__(self, api_base_url):
		self.__api_base_url = api_base_url
		
	def register(self, username, email, password):
		api_url = self.__api_base_url + "/register"
		payload_dict = {
			"email": email,
			"password": password,
			"username": username
		}
		response = requests.post(api_url, json=payload_dict)
		return response.status_code == 200

	def login(self, email, password):
		api_url = self.__api_base_url + "/login"
		payload_dict = {
			"email": email,
			"password": password
		}
		response = requests.post(api_url, json=payload_dict)
		if response.status_code == 200:
			content = response.json()
			return Session(self.__api_base_url, content["token"])
		else:
			return None
		
class Session:
	
	def __init__(self, api_base_url, token, timeout = 10):
		self.__api_base_url = api_base_url
		self.__token = token
		self.__timeout = timeout
		
	def __get_headers(self):
		return {
			'Authorization': f'Bearer {self.__token}',
			'Content-Type': 'application/json'
		}
	
	def set_timeout(self, timeout):
		self.__timeout = timeout
	
	def count_alerts(self):
		api_url = self.__api_base_url + "/alerts/count"
		
		try:
			response = requests.get(api_url, headers=self.__get_headers(), timeout=self.__timeout)
		except requests.exceptions.Timeout:
			return None
			
		if response.status_code == 200:
			content = response.json()
			return content
		else:
			return None
		
	def list_batches(self):
		api_url = self.__api_base_url + "/batches"
		
		try:
			response = requests.get(api_url, headers=self.__get_headers(), timeout=self.__timeout)
		except requests.exceptions.Timeout:
			return None
			
		if response.status_code == 200:
			content = response.json()
			return [Batch.from_dict(data_dict) for data_dict in content]
		else:
			return None
		
	def start_new_batch(self, server_address, server_port, database_name, collection_name, raw_schema_format):
		api_url = self.__api_base_url + "/batch/rawschema/steps/all"
		payload_dict = {
			"address": server_address,
			"authentication": {
				"authMechanism": "SCRAM-SHA-1"
			},
			"collectionName": collection_name,
			"databaseName": database_name,
			"port": str(server_port),
			"rawSchemaFormat": raw_schema_format
		}
		
		try:
			response = requests.post(api_url, json=payload_dict, headers=self.__get_headers(), timeout=self.__timeout)
		except requests.exceptions.Timeout:
			return None
			
		if response.status_code == 200:
			content = response.json()
			return BatchSummary.from_dict(content)
		else:
			return None
	
	def get_batch(self, batch_id):
		api_url = self.__api_base_url + f"/batch/{batch_id}"
		
		try:
			response = requests.get(api_url, headers=self.__get_headers(), timeout=self.__timeout)
		except requests.exceptions.Timeout:
			return None
			
		if response.status_code == 200:
			content = response.json()
			return Batch.from_dict(content)
		else:
			return None
		
	def get_generated_schema(self, batch_id):
		api_url = self.__api_base_url + f"/batch/jsonschema/generate/{batch_id}"
		
		try:
			response = requests.get(api_url, headers=self.__get_headers(), timeout=self.__timeout)
		except requests.exceptions.Timeout:
			return None
			
		if response.status_code == 200:
			content = response.json()
			return SchemaInfo.from_dict(content[0])
		else:
			return None

def start_server(timeout_seconds=300):
	# Run the npm run dev command
	process = subprocess.Popen(['npm', 'run', 'dev'], stdout=subprocess.PIPE, universal_newlines=True)
	ret = None

	# Define a regular expression pattern to match the successful compilation message
	compile_pattern = re.compile(r'Compiled successfully', re.IGNORECASE)

	start_time = time.time()
	
	signal_total = 2
	signal_count = 0
	
	while True:
		# Read a line from the subprocess output
		output_line = process.stdout.readline()

		# Check if the line matches the pattern
		if compile_pattern.search(output_line):
			signal_count += 1
			if signal_count == signal_total:
				print("Compilation successful!")
				ret = process
				break

		# Check if the timeout has been reached
		if time.time() - start_time > timeout_seconds:
			print(f"Timeout reached ({timeout_seconds} seconds). Exiting.")
			break

	return ret

if __name__ == '__main__':
	if len(sys.argv) != 7:
		print("usage: python main_experiment.py <mongo_server> <mongo_port> <database> <collection> <output_file> <start_app>")
		sys.exit(1)

	mongo_server = sys.argv[1]
	mongo_port = sys.argv[2]
	database = sys.argv[3]
	collection = sys.argv[4]
	output_file = sys.argv[5]
	start_app = sys.argv[6] == "true"

	app_process = None
	if start_app:
		print("Starting app...")
		app_process = start_server(timeout_seconds=300)
		if app_process == None:
			print("App could not start!")
			sys.exit(1)

	username = "repeng"
	email = "repeng@cool.srvr"
	password = "thePass1#"
	api_url = "http://localhost:4200/api"

	client = ApiClient(api_url)

	print(f"Registering user {email} if unregistered...")
	client.register(username, email, password)

	print(f"Login into account {email}...")
	session = client.login(email, password)

	if session == None:
		print("Error: Could not log in.")
		sys.exit(1)
		
	session.set_timeout(30)

	while True:
		print("Start a new schema discovery job...")
		summary = None
		while summary == None:
			summary = session.start_new_batch(mongo_server, mongo_port, database, collection, False)
			if summary == None:
				print("Time out while starting a new job.")
	
		print("Job ID: " + summary.batch_id)
	
		print("Querying upon job completion...")
		job_completed = False
		count = 1
		while count < 3 and job_completed == False:
			batch = session.get_batch(summary.batch_id)
			count += 1
			job_completed = batch.status == "DONE"
			if not job_completed:
				print(f"Job: {batch.status}")
		
		if job_completed:
			break

	print(f"Retrieving and storing discovered schema into {output_file}...")
	schema = session.get_generated_schema(summary.batch_id)
	with open(output_file, "w") as text_file:
		text_file.write(schema.get_schema_as_string())

	if app_process != None:
		print("Closing app.")
		app_process.terminate()
		
	print("End!")