import utils
import random

ACTIVITY_NAMES = ["A", "B", "C", "D"]
RESOURCE_NAMES = ["r1", "r2", "r3"]
AVERAGE_CASE_LENGTH = 4
MAX_CASE_LENGTH_DEVIATION = 2
NUMBER_OF_CASES = 100

event_log = []
timestamp = 0
max_started_case_index = 0

cases = []
for case_index in range(0, NUMBER_OF_CASES):
    # Determine a random case length in the range AVERAGE_CASE_LENGTH ± MAX_CASE_LENGTH_DEVIATION
    case_length = round(AVERAGE_CASE_LENGTH + 2 * MAX_CASE_LENGTH_DEVIATION * (random.random() - .5))
    case_id = f"c{case_index}"

    # Create an object for each case that contains the case name and the list of events belonging to this case.
    # In this list each event has a random activity and resource.
    cases.append({
        "id": case_id,
        "events": [{
            "activity": random.choice(ACTIVITY_NAMES),
            "resource": random.choice(RESOURCE_NAMES)
        } for _ in range(0, case_length)]
    })

while(True):
    non_empty_cases = [c for c in cases if len(c["events"]) > 0]

    # Terminate when all events have been added
    if len(non_empty_cases) == 0: break

    # Choose a random case and append first event of it
    case = random.choice(non_empty_cases)
    event = case["events"][0]
    event["case"] = case["id"]
    event["timestamp"] = timestamp
    event_log.append(event)
    case["events"] = case["events"][1:]

    if (random.random() < .5): timestamp += 1

utils.write_csv("event-logs/log.csv", event_log)