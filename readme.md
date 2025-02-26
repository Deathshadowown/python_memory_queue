## FIRST TIME INSTALL

- pip install virtualenv
- virtualenv venv
- source ./venv/bin/activate
  (make sure you have entered into the venv)
- pip install -r requirements.txt
- python3 server.py
- deactivate

- Gain access to bqd_shared_utils repo (Pieka)
- Git clone bqd_shared_utils into root folder
- Get access to .env file and firebase credentials json file (admin)
- copy both files into the root folder

## ADDED NEW MODULES, ADD THEM TO REQUIREMENTS FILE

- - pip freeze > requirements.txt

## HOW TO RUN APPLICATION

- python server.py

# status codes

- 400 Bad Request: The server cannot understand the request due to a client error, such as malformed request syntax, invalid request message framing, or deceptive request routing.

- 405 Method Not Allowed: The method specified in the request (GET, POST, PUT, DELETE) is not allowed for the given resource. The server responds with this status code when the requested method is not applicable to the target resource.

- 404 Not Found: The server cannot find the requested resource. This status code is returned when the requested URL doesn't correspond to any known resource on the server.

- 403 Forbidden response: indicates that the server understands the request but refuses to authorize it.

- 401 Unauthorized: The client must authenticate itself to get the requested response. It means the client's credentials (if provided) are not valid or are missing, and authentication is required.

- 409 Data conflict: When there is a conflict in the data being submitted, such as trying to create a resource that already exists or updating a resource with outdated information.

- 200 OK: The request has succeeded. The server responds with this status code when the request has been successfully processed, and the response body may contain the requested data.

- 201 Created: The request has been fulfilled, resulting in the creation of a new resource. This status code is often used for successful POST requests that create new items.

pip install gunicorn
export PYTHONPATH=/mnt/c/project/new_ithemba_project_2025/venv/lib/python3.10/site-packages

gunicorn -w 4 -k "uvicorn.workers.UvicornWorker" main:app --bind 0.0.0.0:8000

lsof -i :8000
kill -9 PID

uvicorn main:app --reload
