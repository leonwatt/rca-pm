import utils
import event_log_utils
from event_log_utils import event_matching, any_event_matching

def prima_facie_filter_hypotheses(prepared_event_log, hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")
    
    def p_e(hypothesis):
        "Calculates the probability of the effect: P(e)"
        effect = hypothesis["effect"]

        def number_of_interesting_events(case):
            return len(event_log_utils.interesting_events(case, effect))


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


def prima_face_new(prepared_event_log, hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")

    def is_prima_facie_hypothesis(hypothesis):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]
        c_and_e = len(utils.flatten([[ev for ev in event_log_utils.interesting_events(c, effect) if event_matching(ev, cause)] for c in cases]))
        c_true = len([ev for ev in prepared_event_log if event_matching(ev, cause)])
        e_true = len([ev for ev in prepared_event_log if event_matching(ev, effect)])
        total_events = len(prepared_event_log)
        return utils.divide_or_zero(c_and_e, c_true) > utils.divide_or_zero(e_true, total_events)

    return [h for h in hypotheses if is_prima_facie_hypothesis(h)]

def prima_facie_new2(prepared_event_log, hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")

    def is_prima_facie_hypothesis(hypothesis):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]
        
        num_c = 0
        num_c_before_e = 0
        num_events_before_e = 0
        for case in cases:
            num_c += len(event_log_utils.events_matching(case, cause))
            num_c_before_e += len(event_log_utils.events_matching(case, cause, effect))
            num_events_before_e += len(event_log_utils.case_until_match(case, effect, excluding=True))

        num_events = len(prepared_event_log)

        # print()
        # print(num_c_before_e)
        # print(num_c)
        # print(num_events_before_e/num_events)
        # print()

        if num_c == 0: return False
        return num_c_before_e/num_c > num_events_before_e/num_events

    return [h for h in hypotheses if is_prima_facie_hypothesis(h)]