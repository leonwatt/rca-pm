import utils
import os
import statistics

event_log = utils.read_csv(os.path.join("event-logs", "log.csv"))

for e in event_log:
    e["deadline_exceeded"] = e["deadline_exceeded"] == "True"
    e["timestamp"] = int(e["timestamp"])

cases = list(utils.group_by(event_log, "case").values())

print(str(len([c for c in cases if any([e["deadline_exceeded"] for e in c])])) + " cases exceeded the deadline")
print(f"Average case length (time units): {statistics.median([c[-1]['timestamp'] - c[0]['timestamp'] for c in cases])}")