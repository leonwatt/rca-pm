from matplotlib.cbook import index_of
import utils
import random

cases = {
    "c1": "ABCDS",
    "c2": "BAS",
    "c3": "BDEAS",
    "c4": "BBBE",
    "c5": "ACDDE"
}
res = []
timestamp = 0
max_started_case_index = 0

while(True):
    # Choose randomly a non-emtpy case, in the correct order (do not choose the third case if the second case has not started yet)
    items = [it for (index, it) in enumerate(cases.items()) if len(it[1]) > 0 and index <= max_started_case_index]
    if len(items) == 0: break
    case = random.choice(items)
    case_id = case[0]
    if (list(cases.keys()).index(case_id) == max_started_case_index): max_started_case_index += 1

    # Append the first event of the randomly chosen case to the event log
    res.append({
        "timestamp": timestamp,
        "case": case_id,
        "state": case[1][0]
    })
    cases[case_id] = cases[case_id][1:]
    # if (random.random() < .5): 
    timestamp += 1

utils.write_csv("event-logs/log.csv", res)