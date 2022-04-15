import utils
import event_log_utils
from event_log_utils import event_matching, any_event_matching

def prima_facie_filter_hypotheses(prepared_event_log, hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")
    
    def p_e(hypothesis):
        "Calculates the probability of the effect: P(e)"
        effect = hypothesis["effect"]

        def number_of_interesting_events(case):
            return len(event_log_utils.interesting_events(c, effect))


        interesting_events_with_effect = sum([number_of_interesting_events(c) for c in cases if any_event_matching(c, effect)])
        interesting_events = sum([number_of_interesting_events(c) for c in cases])
        
        return utils.divide_or_zero(interesting_events_with_effect, interesting_events)


    def p_e_c(hypothesis):
        "Calculates the probability of the effect if preceeded by the cause: P(e|c)"
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]

        def number_of_interesting_cause_events(case):
            return len([ev for ev in event_log_utils.interesting_events(case, effect) if event_matching(ev, cause)])

        interesting_cause_events = sum([number_of_interesting_cause_events(c) for c in cases])
        interesting_cause_events_with_effect = sum([number_of_interesting_cause_events(c) for c in cases if any_event_matching(c, effect)])

        return utils.divide_or_zero(interesting_cause_events_with_effect, interesting_cause_events)


    return [h for h in hypotheses if p_e_c(h) > p_e(h)]