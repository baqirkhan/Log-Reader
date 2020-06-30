# Log-Reader

The application can be interacted with POST API's and response comes back the JSON. The input/output format is as follow:

**INPUT:**

`{
   "start_date": "2020-01-01T15:41:52.301Z",
   "end_date": "2020-02-18T07:34:09.451Z",
   "api_key": "qp0jnJKA78"
 }`

1. **start_date**: Takes start date in *ISO 8601 forma*t as given in the log file.
2. **end_date**: Takes end date in _ISO 8601 format_ as given in the log
3. **api_key**: API key is just their for authentication purpose, copy the same api key in all requests


OUTPUT:

`{
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
     },`

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