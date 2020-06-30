# -*- coding: utf-8 -*-

# Baqir Khan
# Software Engineer (Backend)
from datetime import datetime
import asyncio

# Convert time from string format to python's datetime object for easy comparisons
def isodate_to_datetime_obj(isodate):
    if type(isodate) == bytes:
        return datetime.strptime(isodate.decode('utf-8'), "%Y-%m-%dT%H:%M:%S.%fZ")
    elif type(isodate) == str:
        return datetime.strptime(isodate, "%Y-%m-%dT%H:%M:%S.%fZ")


class LogReader:

    # Variables used in API Output JSON
    START_DATE = "start_date"
    END_DATE = "end_date"
    LOGS = "logs"
    TIME = "time"
    MESSAGE = "message"
    LOGS_COUNT = "logs_count"

    def __init__(self, start_date, end_date, mapping, number_of_lines, filename):
        self.start_date = start_date
        self.end_date = end_date
        self.mapping = mapping
        self.number_of_lines = number_of_lines
        self.filename = filename
        self.results = {self.START_DATE: start_date, self.END_DATE: end_date, self.LOGS_COUNT: 0, self.LOGS: []}

    # Given offset('value' field in 'mapping' dictionary), return file pointer to that location
    def __get_file_pointer_at_offset(self, offset):
        fp = open(self.filename, 'rb')
        fp.seek(offset, 1)
        return fp

    # Parses date from line by splitting on space (' ') and taking the first element
    def __get_date_at_file_pointer(self, file_pointer):
        return file_pointer.readline().split(' ')[0]

    # Binary search in O(log(n)) and returns the line number right before start_date
    def __binary_search(self, target_date):
        lo, hi = 1, self.number_of_lines
        while lo <= hi:
            mid = (lo + hi) >> 1
            fp_at_mid = self.__get_file_pointer_at_offset(self.mapping[mid])
            date_at_mid_isoformat = self.__get_date_at_file_pointer(fp_at_mid)
            date_at_mid_datetime = isodate_to_datetime_obj(date_at_mid_isoformat)
            if date_at_mid_datetime == target_date:
                return mid
            elif date_at_mid_datetime < target_date:
                lo = mid + 1
            else:
                hi = mid - 1
        return lo

    # Loops from line given by binary search until end date is reached
    async def __populate_error_logs(self, offset):
        fp = self.__get_file_pointer_at_offset(offset)
        end_date_isoformat = isodate_to_datetime_obj(self.end_date)
        start_date_isoformat = isodate_to_datetime_obj(self.start_date)
        count = 0
        for i, line in enumerate(fp):
            line = line.decode('utf-8')
            line_splitted = line.split()
            line_date = isodate_to_datetime_obj(line_splitted[0])

            # Current log date not in range as required by client, break
            if line_date > end_date_isoformat or line_date < start_date_isoformat:
                break

            count += 1
            self.results[self.LOGS].append({self.TIME: line_splitted[0], self.MESSAGE: " ".join(line_splitted[1:])})
        self.results[self.LOGS_COUNT] = count

    # The only public function which can be accessed outside the class, entry point.
    def build(self):
        line_start = self.__binary_search(isodate_to_datetime_obj(self.start_date))

        # USING Async/Await
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__populate_error_logs(self.mapping[line_start]))

        # Without using Async await
        # self.__populate_error_logs(self.mapping[line_start])
        return self.results








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
