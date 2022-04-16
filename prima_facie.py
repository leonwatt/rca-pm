import utils
import event_log_utils

def peform_filtering(prepared_event_log, hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")

    def is_prima_facie_hypothesis(hypothesis):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]

        
        num_c = sum([len(event_log_utils.events_matching(case, cause)) for case in cases])
        num_c_before_e = sum([len(event_log_utils.events_matching(case, cause, before_effect=effect)) for case in cases])

        num_events_before_e = sum([len(event_log_utils.case_until_match(case, effect, excluding=True)) for case in cases])
        num_events = len(prepared_event_log)


        if num_c == 0: return False
        return num_c_before_e / num_c > num_events_before_e / num_events


    return [h for h in hypotheses if is_prima_facie_hypothesis(h)]