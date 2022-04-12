import utils

def test_prima_facie(event_log, cause, effect):
    p_e = count_events_of_state(event_log, effect) / len(event_log) # P(e)
    p_e_given_c = count_effect_after_cause(event_log, cause, effect) / count_events_of_state(event_log, cause) # P(e|c)
    
    return p_e_given_c > p_e


def count_effect_after_cause(event_log, cause, effect):
    def cause_index(c):
        matches = [index for (index, obj) in enumerate(c) if obj["state"] == cause]
        if len(matches) == 0: return -1
        return matches[0]

    case_objects = list(utils.group_by(event_log, "case").values())

    cases = [{
        "events": c,
        "events_after_cause": c[cause_index(c) + 1:]
    } for c in case_objects]
    return sum([len([e for e in case["events_after_cause"] if e["state"] == effect]) for case in cases])

def count_events_of_state(event_log, state):
    return count_matching_events(event_log, lambda e: e["state"] == state)

def count_matching_events(event_log, check_fn):
    return len([e for e in event_log if check_fn(e)])