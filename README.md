# Description

A small HTTP service that implements a RESTful API that stores a message and returns the SHA256 hash of that message to the user.
- POST to `/messages`: stores the message and returns the SHA256 hash of that message
- GET to `/messages/$HASH`: retrieves the message using the hash
- DELETE to `/messages/$HASH`: delete the message if it exists
- GET to `/metrics`: qty of records, time of last write(?)



