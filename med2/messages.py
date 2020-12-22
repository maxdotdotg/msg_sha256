import logging
import json
from hashlib import sha256

def check_for_db():
    try:
        with open("data.json", "r") as db:
            data = json.load(db)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("no db file found, creating empty db")
        logging.info("initialize empty db")
        with open("data.json", "w") as db:
            data = {}
            db.write(json.dumps(data))

def fetch_message(msg_sha):
    with open("data.json", "r") as db:
            data = json.load(db)
    try:
        logging.info(f"looking for {msg_sha}")
        response = {"message": data[msg_sha]}
        status = 200
    except KeyError:
        response = {"error": "unable to find message", "message_sha256": msg_sha}
        status = 404

    return {"response": response, "status": status}


def write_message(msg):
    msg_sha = sha256(msg.encode("utf-8").strip()).hexdigest()

    infile = json.load(open("data.json", "r"))
    outfile = open("data.json", "w+")

    infile[msg_sha] = msg
    json.dump(infile, outfile)
    response = {"digest": msg_sha}
    status = 201

    return { "response": response, "status": status }


def delete_message(msg_sha):
    with open("data.json", "wb") as db:
        data = json.load(db)

    if "digest" in fetch_message(msg_sha).values():
        del data[msg_sha]
        json.dump(data, db)
        response = {"response": ""}
        status = 200
    else:
        response = {"response": ""}
        status = 404

    return response
