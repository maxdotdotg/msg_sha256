import json
from collections import Counter

path_counter = Counter()


def get_count_items():
    records = {}
    try:
        with open("data.json", "r") as db:
            data = json.load(db)
        records["records_qty"] = len(data)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        from messages import check_for_db

        check_for_db()
        records["records_qty"] = 0

    return records


def get_db_size():
    db_size = {}

    try:
        from os import stat

        db_size["db_size_bytes"] = stat("data.json").st_size
    except FileNotFoundError:
        from messages import check_for_db

        check_for_db()
        db_size["db_size_bytes"] = 0

    return db_size


def get_metrics():
    # aggregate the things and provide'em
    metrics_blob = {}

    records = get_count_items()
    size = get_db_size()
    top_requests = {record[0]: record[1] for record in path_counter.most_common(10)}

    metrics_blob["top_requests"] = top_requests
    metrics_blob.update(records)
    metrics_blob.update(size)

    return metrics_blob


def record_request(path):
    path_counter.update([path])
