import utils

def prepare(system_states, path_to_event_log, case_attribute_name, timestamp_attribute_name):
    event_log = utils.read_csv(path_to_event_log)

    return [{
        "case": e[case_attribute_name],
        "state": {key: fn(e) for (key, fn) in system_states.items()},
        "timestamp": e[timestamp_attribute_name]
    } for e in event_log]