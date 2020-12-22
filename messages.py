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
    check_for_db()
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
    check_for_db()
    msg_sha = sha256(msg.encode("utf-8").strip()).hexdigest()

    infile = json.load(open("data.json", "r"))
    outfile = open("data.json", "w+")

    infile[msg_sha] = msg
    json.dump(infile, outfile)
    response = {"digest": msg_sha}

    # return 201 on successful create
    # https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.5
    status = 201

    return {"response": response, "status": status}


def delete_message(msg_sha):
    infile = json.load(open("data.json", "r"))
    outfile = open("data.json", "w+")

    try:
        del infile[msg_sha]
        json.dump(infile, outfile)
        response = ""

        # return 204 on successful delete
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.7
        status = 204
    except KeyError:
        # even if key wasn't found, treat delete as success since the record
        # is not in the db
        response = ""
        status = 204

    return {"response": response, "status": status}
