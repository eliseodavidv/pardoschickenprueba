import os
import json
import boto3
from datetime import datetime, timezone

_events = boto3.client("events")
EVENTS_BUS_NAME = os.environ["EVENTS_BUS_NAME"]

def publish_event(source: str, detail_type: str, detail: dict):
    if "timestamp" not in detail:
        detail["timestamp"] = datetime.now(timezone.utc).isoformat()

    _events.put_events(
        Entries=[
            {
                "Source": source,
                "DetailType": detail_type,
                "Detail": json.dumps(detail),
                "EventBusName": EVENTS_BUS_NAME,
            }
        ]
    )
