import csv

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

def read_from_file(path):
    with open(path) as f:
        return f.read()

def write_to_file(path, content):
    with open(path, "w") as f:
        f.write(str(content))


def read_csv(path, delimiter = ","):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def write_csv(path, content):
    with open(path, "w") as f:
        writer = csv.writer(f)
        header = content[0].keys()
        writer.writerow(header)
        writer.writerows([[row[h] for h in list(header)] for row in content])

def group_by(arr_of_dicts, grouping_attr):
    res = {}

    for el in arr_of_dicts:
        grouping_value = el[grouping_attr]
        res.setdefault(grouping_value, [])
        res[grouping_value] += [el]

    return res

def group_by_as_list(arr_of_dicts, grouping_attr):
    return list(group_by(arr_of_dicts, grouping_attr).values())


def event_matching(event, cause_or_effect):
    return event["state"][cause_or_effect[0]] == cause_or_effect[1]


def get_all_values_for_state_attribute(event_log, attribute):
    system_states = [e["state"] for e in event_log]
    return list(set([s[attribute] for s in system_states]))

def divide_or_zero(numerator, denominator):
    if denominator == 0: return 0
    return numerator / denominator