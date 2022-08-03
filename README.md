
# note

A general purpose database schema inplemented as a CRUD application
built with Python/fastAPI/Sqlite

Template from https://www.gormanalysis.com/blog/building-a-simple-crud-application-with-fastapi/

Examples to create a note

$ curl -X 'POST' 'http://127.0.0.1:8000/note' -H 'accept: appplication/json' -H 'Content-Type: application/json' -d '{"rid": "0", "lid": "0", "type": "MYTYPE",  "data": "mydata"}'

$ curl -X 'GET' 'http://127.0.0.1:8000/note' -H 'accept: appplication/json' -H 'Content-Type: application/json'

$ curl -X 'GET' 'http://127.0.0.1:8000/note/?type=ATYPRE' -H 'accept: appplication/json' -H 'Content-Type: application/json'
