# Log-Reader

**Strategy:**

Since the Log file is very large, therefore, _pre-processing_ it and making an index like structure will be efficient. To do that, we can create
a dictionary where `key` contains the _line number_ and `value` contains _offset_ of that line in terms of bytes from starting.
In this way, given any line number, we can find its position in the file and read the line in **O(1)** time as dictionaries are nothing but _hashmap_.  

If we are given _1 TB_ large Log file, then its index dictionary will not be more than _100MB_ since it only contains key/value pairs for every line and both are integers.
Once the request comes, we perform **binary search** using _start_date_ as target value and find the line number from where we have 
to start reading the logs. This process will take **O(log(n**)) time where **n** is the _number of lines_ in the log file.

Now that we have starting line number from where we have to read logs, we can read line by line sequentially without bringing the entire file
in memory and append our results into the array.

<hr>

**Input/Output Description:**

The application can be interacted with POST API's and response comes back the JSON. The input/output format is as follow:

**INPUT:**

<pre>
{
    "start_date": "2020-01-01T15:41:52.301Z",
    "end_date": "2020-02-18T07:34:09.451Z",
    "api_key": "qp0jnJKA78"
 }
</pre>

1. **start_date**: Takes start date in _ISO 8601 format_ as given in the log file.
2. **end_date**: Takes end date in _ISO 8601 format_ as given in the log
3. **api_key**: API key is just their for authentication purpose, copy the same api key in all requests


OUTPUT:

<pre>
{
   "start_date": "2020-01-01T15:41:52.301Z",
   "end_date": "2020-02-18T07:34:09.451Z",
   "logs_count": 96172,
   "logs": [
     {
       "time": "2020-01-01T15:42:01.290Z",
       "message": "Response 200 sent to 79.122.157.242 for /about"
     },
     {
       "time": "2020-01-01T15:42:28.385Z",
       "message": "Querying table customers"
     },
     ...
     ..
     .
     ]
 }
</pre>

1. **start_date**: Same as input
2. **end_date**: Same as output
3. **logs_count**: Total number of logs in the given range
4. **logs**: Array of dictionaries, where each element has log message and timestamp

<hr>

**Installation steps:**

Project requires `Python 3.6 or above`. To check if you have it, please run:
    `python3.6` on terminal. After installing it, please follow the instructions:

1. Install virtualenv.

    `sudo apt-get install python3-pip` \
    `sudo pip3 install virtualenv `
    
2. Clone the project and navigate to inside `home-project` folder. Then create a new virtual environment.
    
    `virtualenv -p python3.6 env`

3. Activate the virtual environment:

    `source env/bin/activate`
    
4. Install the dependencies:

    `pip install -r requirements.txt`
    
5. Start the API's:

    `python run.py`
    
6. Use POSTMAN to make API requests, else terminal using CURL:

    `curl --location --request POST 'http://0.0.0.0:8000/fetch_logs' --header 'Content-Type: application/json' --data-raw '{
       "start_date": "2020-01-01T15:41:52.301Z",
       "end_date": "2020-02-18T07:34:09.451Z",
       "api_key": "qp0jnJKA78"
     }'`
     
The application uses asyncio, therefore, requests from multiple clients can be served asynchronously.
