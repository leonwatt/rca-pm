import utils
from utils import DATE_FORMAT
import random
import os
import datetime

ACTIVITY_NAMES = ["A", "B", "C", "D"]
RESOURCE_NAMES = ["r1", "r2", "r3", "r4", "r5", "r6"]
AVERAGE_CASE_LENGTH = 4
CASE_LENGTH_VARIATION = 2
NUMBER_OF_CASES = 100
DEADLINE_EXCEED_PROBABILITY_PER_EVENT = .1 # => 34% chance to exceed deadline for case of length 4
RESOURCE_DEADLINE_INFLUENCE_VARIATION = .3
INITIAL_TIMESTAMP = datetime.datetime(2022, 1, 2, 12, 48, 36) # Start at an arbitrary point in time
AVERAGE_TIMESTAMP_INCREASE_IN_HOURS = 5
TIMESTAMP_INCREASE_VARIATION = 4.9

event_log = []
timestamp = INITIAL_TIMESTAMP

resource_influences_on_deadlines = {r: 1 + RESOURCE_DEADLINE_INFLUENCE_VARIATION * (2 * random.random() - 1) for r in RESOURCE_NAMES}

cases = []
for case_index in range(0, NUMBER_OF_CASES):
    # Determine a random case length in the range AVERAGE_CASE_LENGTH ± CASE_LENGTH_VARIATION
    case_length = round(AVERAGE_CASE_LENGTH + CASE_LENGTH_VARIATION * (2 * random.random() - 1))
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

max_case_index = 0
while(True):
    non_empty_cases = [c for (index, c) in enumerate(cases) if index <= max_case_index and len(c["events"]) > 0]

    # Terminate when all events have been added
    if len(non_empty_cases) == 0: break


    # Choose a random case and append first event of it
    case = random.choice(non_empty_cases)
    event = case["events"][0]

    # Extend range of allowed cases (if applicable)
    if cases.index(case) == max_case_index: max_case_index += 1

    # Determine if the deadline is exceeded
    deadline_exceed_probability = DEADLINE_EXCEED_PROBABILITY_PER_EVENT * resource_influences_on_deadlines[event["resource"]]
    case["deadline_exceeded"] = case["deadline_exceeded"] or random.random() < deadline_exceed_probability
    event["deadline_exceeded"] = case["deadline_exceeded"]

    event["case"] = case["id"]
    event["timestamp"] = timestamp.strftime(DATE_FORMAT)
    event_log.append(event)
    
    case["events"] = case["events"][1:]

    timestamp += datetime.timedelta(hours = AVERAGE_TIMESTAMP_INCREASE_IN_HOURS + TIMESTAMP_INCREASE_VARIATION * (2 * random.random() - 1))

path = os.path.join("event-logs", "log.csv")
utils.write_csv(path, event_log)
print(f"Written event log with {len(event_log)} events to {path}")