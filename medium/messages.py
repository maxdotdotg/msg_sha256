import json
from hashlib import sha256

def fetch_message(msg_sha):
    with open(db_file, 'rb') as db:
        data = json.load(db_file)
    try: 
        response = { "digest": data[msg_sha] }
        status = 200
    except KeyError:
        response = { "error" : "unable to find message",
                "message_sha256" : msg_sha }
        status = 404
    return { "response": response, 
            "status": status} 

def write_message(msg):
    with open(db_file, 'wb+') as db:
        data = json.load(db_file)

    # check if msg already exists
    # if not, write it
    msg_sha = sha256(msg.strip().hexdigest()
    if "error" in fetch_message(msg_sha).values():
        data[msg_sha] = msg
        response = { "digest": msg_sha,
            status = 201}
        return response
    else:
        response = { "digest": msg_sha,
            status = 200}
        return response

def delete_message(msg_sha):
    with open(db_file, 'wb') as db:
        data = json.load(db_file)

    if "digest" in fetch_message(msg_sha).values():
        del data[msg_sha]
        json.dump(data,db_file)
        response = { "response" : "",
            status = 200 }
    else:
        response = { "response" : "",
            status = 404 }

    return response

