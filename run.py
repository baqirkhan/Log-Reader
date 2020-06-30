# -*- coding: utf-8 -*-

# Baqir Khan
# Software Engineer (Backend)

from flask import abort, jsonify, request, Flask
from fetch import LogReader

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
filename = 'example.txt'
API_KEY = "qp0jnJKA78"


# Mapping where key corresponds to line number of log file and value corresponds to its offset from beginning
def generate_mapping():
    mapping = {1: 0}
    number_of_lines = 0
    with open(filename, 'rb') as fp:
        for i, line in enumerate(fp):
            mapping[i + 2] = fp.tell()
            number_of_lines += 1
    return mapping, number_of_lines


# Checks if all the required fields are provided or not
def check_required_fields(required_fields, request):
    current_fields = set(list(request.keys()))
    for field in required_fields:
        if field not in current_fields:
            return False
    return True


# Authenticates, checks if body is valid or not
def authenticate_request(request):
    request_body = request.json
    if not request_body:
        abort(400, "Missing request body")
    required_fields = ["start_date", "end_date", "api_key"]
    if not check_required_fields(required_fields, request_body):
        abort(400, f"Missing 1 or more required fields: {','.join(required_fields)}")
    api_key = request_body.get('api_key')
    if api_key != API_KEY:
        abort(400, "Authentication failed")
    return request_body


# Start point of program
@app.route("/fetch_logs", methods=['POST'])
def fetch_logs():
    request_body = authenticate_request(request)

    start_date = request_body.get('start_date')
    end_date = request_body.get('end_date')

    print("Request received")
    results = LogReader(start_date, end_date, mapping, number_of_lines, filename).build()
    print("Request Processed")

    return jsonify(results)


# Calling mapping func only once to serve all request
mapping, number_of_lines = generate_mapping()

# Starting Flask API
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)