import json


def notify(diff) -> None:
    print(json.dumps(diff, indent=2))
