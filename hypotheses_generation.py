
def generate_hypotheses(input, causes_key, effects_key, causes_values = None, effects_values = None):
    system_states = [e["state"] for e in input]

    def generate_values(key):
        return list(set([s[key] for s in system_states]))

    if causes_values == None: causes_values = generate_values(causes_key)
    if effects_values == None: effects_values = generate_values(effects_key)

    causes = [(causes_key, v) for v in causes_values]
    effects = [(effects_key, v) for v in effects_values]

    rules = []

    for c in causes:
        for e in effects:
            rules.append({
                "cause": c,
                "effect": e
            })

    return rules
