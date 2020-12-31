# Description
A small HTTP service written using the Python 3 standard library.

This service implements a RESTful API that stores a message and returns the SHA256 hash of that message to the user.
- POST to `/messages`: stores the message and returns the SHA256 hash of that message
- GET to `/messages/$HASH`: retrieves the message using the hash
- DELETE to `/messages/$HASH`: delete the message if it exists
- GET to `/metrics`: qty of records, size of db, most requested paths


## Usage
to run the server via the CLI, execute `main`
``` bash
./main
```

Alternatively, use docker:
``` bash
# build
docker build -t msg_sha256 .

# run
docker run --name msg_sha256 -p 8000:8000 -d msg_sha256
```

Sample calls:
``` bash
# create a message
curl -XPOST localhost:8000/messages/ -d '{"message": "hello"}'
{"digest": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"}%

# read that message
curl -XGET 127.0.0.1:8000/messages/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
{"message": "hello"}%

# delete a message
curl -XDELETE 127.0.0.1:8000/messages/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
curl -XGET 127.0.0.1:8000/messages/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
{"error": "unable to find message", "message_sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"}%

# get some metrics
curl -XGET 127.0.0.1:8000/metrics
{"top_requests": {"/messages/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824": 3, "/messages/": 2, "/metrics": 2}, "records_qty": 0, "db_size_bytes": 2}%
```
