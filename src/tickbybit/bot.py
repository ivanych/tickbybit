import json


def notify(diff) -> None:
    print(json.dumps(diff, indent=2))


def to_json(diff: dict) -> str:
    dump = json.dumps(diff, indent=2)
    return f"```json\n{dump}\n```"
