
def event_matching(event, cause_or_effect):
    return event["state"][cause_or_effect[0]] == cause_or_effect[1]

def any_event_matching(case, cause_or_effect):
    return any([event["state"][cause_or_effect[0]] == cause_or_effect[1] for event in case]) 

def get_all_values_for_state_attribute(event_log, attribute):
    system_states = [e["state"] for e in event_log]
    return list(set([s[attribute] for s in system_states]))

def events_before_effect_or_complete(case, effect):
    res = []
    for ev in case:
        res.append(ev)
        if event_matching(ev, effect): break
    return res

def interesting_events(case, effect):
    res = []
    for ev in case:
        if event_matching(ev, effect): break
        res.append(ev)
    return res

def interesting_parts_of_cases(cases, effect):
    return [events_before_effect_or_complete(c, effect) for c in cases]

def print_hypothesis(hypothesis):
    print(f"{hypothesis['cause'][0]}: {hypothesis['cause'][1]} => {hypothesis['effect'][0]}: {hypothesis['effect'][1]}")

def print_hypotheses(hypotheses):
    print(f"{len(hypotheses)} hypotheses:")
    for h in hypotheses:
        print_hypothesis(h)