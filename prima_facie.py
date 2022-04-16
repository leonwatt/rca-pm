import utils
import event_log_utils

def peform_filtering(prepared_event_log, hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")

    def is_prima_facie_hypothesis(hypothesis):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]

        num_events = len(prepared_event_log)
        
        num_c = 0
        num_c_before_e = 0
        num_events_before_e = 0

        for case in cases:
            num_c += len(event_log_utils.events_matching(case, cause))
            num_c_before_e += len(event_log_utils.events_matching(case, cause, effect))
            num_events_before_e += len(event_log_utils.case_until_match(case, effect, excluding=True))

        if num_c == 0: return False
        return num_c_before_e/num_c > num_events_before_e/num_events

    return [h for h in hypotheses if is_prima_facie_hypothesis(h)]