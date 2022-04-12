import utils
import random
import os

ACTIVITY_NAMES = ["A", "B", "C", "D"]
RESOURCE_NAMES = ["r1", "r2", "r3"]
AVERAGE_CASE_LENGTH = 4
MAX_CASE_LENGTH_DEVIATION = 2
NUMBER_OF_CASES = 100
TIMESTAMP_INCREASE_PROBABILITY = .5
DEADLINE_EXCEED_PROBABILITY_PER_EVENT = .1 # Approx. 34% chance to exceed deadline for case of length 4

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
        "deadline_exceeded": False, # Initially always false, may turn true with every event (and stay true then)
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

    case["deadline_exceeded"] = case["deadline_exceeded"] or random.random() < DEADLINE_EXCEED_PROBABILITY_PER_EVENT
    event["deadline_exceeded"] = case["deadline_exceeded"]

    event["case"] = case["id"]
    event["timestamp"] = timestamp
    event_log.append(event)
    
    case["events"] = case["events"][1:]

    if (random.random() < TIMESTAMP_INCREASE_PROBABILITY): timestamp += 1

path = os.path.join("event-logs", "log.csv")
utils.write_csv(path, event_log)
print(f"Written event log with {len(event_log)} events to {path}")