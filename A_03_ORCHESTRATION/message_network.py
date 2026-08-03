import json
import uuid
from datetime import datetime
from pathlib import Path

class MessageNetwork:

    def __init__(self):
        self.root = Path(__file__).resolve().parent
        self.network_dir = self.root / "MESSAGE_BUS"
        self.network_dir.mkdir(exist_ok=True)

    def create_message(self, sender, receiver, msg_type, payload, priority="normal"):

        message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "from": sender,
            "to": receiver,
            "type": msg_type,
            "priority": priority,
            "payload": payload,
            "status": "queued"
        }

        return message

    def send(self, message: dict):

        file = self.network_dir / f"{message['id']}.json"

        file.write_text(
            json.dumps(message, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return {
            "status": "sent",
            "message_id": message["id"]
        }

    def read_queue(self, department=None):

        messages = list(self.network_dir.glob("*.json"))

        result = []

        for m in messages:
            try:
                data = json.loads(m.read_text(encoding="utf-8"))

                if department is None or data.get("to") == department:
                    result.append(data)

            except Exception:
                continue

        return sorted(result, key=lambda x: x.get("priority", "normal"))

    def ack(self, message_id):

        file = self.network_dir / f"{message_id}.json"

        if file.exists():
            msg = json.loads(file.read_text(encoding="utf-8"))
            msg["status"] = "done"
            file.write_text(json.dumps(msg, ensure_ascii=False, indent=2), encoding="utf-8")

            return {"status": "acked"}

        return {"status": "not_found"}


if __name__ == "__main__":
    net = MessageNetwork()

    msg = net.create_message(
        "DISPATCHER",
        "RUNNER",
        "task",
        {"task": "test"}
    )

    print(net.send(msg))
