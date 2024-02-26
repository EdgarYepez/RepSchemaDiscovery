import sys
from deepdiff import DeepDiff
import json

def load_json_from_file(json_file_path):
	with open(json_file_path) as json_file:
		return json.load(json_file) 

def save_text_file(contents, file_path):
	with open(file_path, 'w') as file:
		file.write(contents)

def save_dictionary_as_json(json_string, json_file_path):
	json_data = json.loads(json_string)
	pretty_json = json.dumps(json_data, indent=4, sort_keys=True)
	save_text_file(pretty_json, json_file_path)

if len(sys.argv) != 5:
	print("usage: python jsondeepdiff.py <json_file_reference> <json_file_target> <json_diff_output_file_path> <summary_file_path>")
	sys.exit(1)

json_file_reference = sys.argv[1]
json_file_target = sys.argv[2]
json_output_file_path = sys.argv[3]
summary_file_path = sys.argv[4]

json_target = load_json_from_file(json_file_target)
json_reference = load_json_from_file(json_file_reference)

print(f"Target file: {json_file_target}")
print(f"Reference file: {json_file_reference}")

diff = DeepDiff(json_reference, json_target, ignore_order=True)

summary = ""
additions = 0 if not "dictionary_item_added" in diff else f"{len(diff['dictionary_item_added'])}: {diff['dictionary_item_added']}"
summary += f"Additions: { additions }\n"
removals = 0 if not "dictionary_item_removed" in diff else f"{len(diff['dictionary_item_removed'])}: {diff['dictionary_item_removed']}"
summary += f"Removals: { removals }\n"
changes = 0 if not "values_changed" in diff else f"{len(diff['values_changed'])}: {diff['values_changed']}"
summary += f"Changes: { changes }"

print(summary)

save_dictionary_as_json(diff.to_json(), json_output_file_path)
save_text_file(summary, summary_file_path)

print(f"Output diff saved in {json_output_file_path}")
print(f"Output summary saved in {summary_file_path}")