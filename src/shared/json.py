import json


def jsonify(data):
    return json.dumps(data, indent=4, sort_keys=True, default=str)


def json_load_file(file):
    return json.load(file)


def json_loads(data):
    return json.loads(data)


def json_dump_file(data, file):
    return json.dump(data, file, indent=4, sort_keys=True, default=str)
