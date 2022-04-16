import statistics
import utils
from event_log_utils import events_matching, events_not_matching

def calculate_values(prepared_event_log, prima_facie_hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")

    def epsilon(hypothesis, x_val):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]
        x = (cause[0], x_val)

        c_and_x_before_e = sum([len(events_matching(c, cause, effect)) * len(events_matching(c, x, effect)) for c in cases])
        c_and_x = sum([len(events_matching(c, cause)) * len(events_matching(c, x)) for c in cases])

        not_c_and_x_before_e = sum([len(events_not_matching(c, cause, effect)) * len(events_matching(c, x, effect)) for c in cases])
        not_c_and_x = sum([len(events_not_matching(c, cause)) * len(events_matching(c, x)) for c in cases])

        if c_and_x == 0 or not_c_and_x == 0: return 0
        return c_and_x_before_e/c_and_x - not_c_and_x_before_e/not_c_and_x


    def calculate_epsilon_for_hypothesis(hypothesis):
        cause = hypothesis["cause"]
        x_vals = list(set([h["cause"][1] for h in prima_facie_hypotheses if h["cause"] != cause]))
        if len(x_vals) == 0: return 0
        return statistics.mean([epsilon(hypothesis, x_val) for x_val in x_vals])

    return [calculate_epsilon_for_hypothesis(h) for h in prima_facie_hypotheses]