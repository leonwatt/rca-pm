import statistics
import utils
from event_log_utils import any_event_matching, interesting_events, event_matching, events_matching, case_until_match

def calculate_epsion_values(prepared_event_log, prima_facie_hypotheses):

    cases = utils.group_by_as_list(prepared_event_log, "case")

    def p_e_c_x(hypothesis, x_val, c_val = True):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]
        x = (cause[0], x_val)

        interesting_parts_of_cases = [interesting_events(c, effect) for c in cases]

        def num_c_or_x(case):
            return len([ev for ev in case if event_matching(ev, cause) or event_matching(ev, x)])

        num_c_and_x = sum([num_c_or_x(c) for c in interesting_parts_of_cases if any_event_matching(c, cause) == c_val and any_event_matching(c, x)])
        num_c_and_x_and_effect = sum([num_c_or_x(c) for (index, c) in enumerate(interesting_parts_of_cases) if any_event_matching(c, cause) == c_val and any_event_matching(c, x) and any_event_matching(cases[index], effect)])

        return utils.divide_or_zero(num_c_and_x_and_effect, num_c_and_x)


    def calculate_epsilon_for_hypothesis(hypothesis):
        cause = hypothesis["cause"]
        x_vals = list(set([h["cause"][1] for h in prima_facie_hypotheses]))
        epsilons = [p_e_c_x(hypothesis, x) - p_e_c_x(hypothesis, x, False) for x in x_vals if x != cause[1]]
        # print(epsilons)
        if len(epsilons) == 0: return 0
        return statistics.mean(epsilons)


    return [calculate_epsilon_for_hypothesis(h) for h in prima_facie_hypotheses]

def calculate_epsion_values_new(prepared_event_log, prima_facie_hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")

    def p_e_c_x(hypothesis, x_val):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]
        x = (cause[0], x_val)

        clipped_cases = [case_until_match(c, effect, excluding=True) for c in cases]

        c_and_x = sum([len(events_matching(c, cause, effect)) * len(events_matching(c, x, effect)) for c in cases])
        c_and_x_before_e = sum([len(events_matching(c, cause, effect)) * len(events_matching(c, x, effect)) for c in clipped_cases])

        not_c_and_x = 0
        not_c_and_x_before_e = 0

        c_events = [ev for ev in prepared_event_log if event_matching(ev, cause)]
        c_events_clipped = [ev for c in clipped_cases for ev in c if event_matching(ev, cause)]
        x_events = [ev for ev in prepared_event_log if event_matching(ev, x)]
        x_events_clipped = [ev for c in clipped_cases for ev in c if event_matching(ev, x)]

        for c_ev in c_events:
            not_c_and_x += len([x_ev for x_ev in x_events if x_ev["case"] != c_ev["case"]])# + len(x_events)
            not_c_and_x_before_e += len([x_ev for x_ev in x_events_clipped if x_ev["case"] != c_ev["case"]])# + len([x_ev for x_ev in x_events_clipped if not any([])])

        if c_and_x == 0 or not_c_and_x == 0: return 0
        return c_and_x_before_e/c_and_x - not_c_and_x_before_e/not_c_and_x



    def calculate_epsilon_for_hypothesis(hypothesis):
        cause = hypothesis["cause"]
        x_vals = list(set([h["cause"][1] for h in prima_facie_hypotheses if h["cause"][1] != cause]))
        return statistics.mean([p_e_c_x(hypothesis, x_val) for x_val in x_vals])

    return [calculate_epsilon_for_hypothesis(h) for h in prima_facie_hypotheses]