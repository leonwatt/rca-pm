import statistics
import utils
from utils import event_matching
from utils import get_all_values_for_state_attribute

def calculate_epsion_values(prepared_event_log, prima_facie_hypotheses):

    cases = utils.group_by_as_list(prepared_event_log, "case")

    def p_e_c_x(hypothesis, x_val):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]
        x_obj = (cause[0], x_val)

        def number_of_c_and_x_preceding_e(case):
            num = 0
            x_matching = False
            c_matching = False
            for ev in case:
                if event_matching(ev, effect):
                    if x_matching and c_matching: return num
                    return 0
                if event_matching(ev, cause):
                    c_matching = True
                    num += 1
                if event_matching(ev, x_obj):
                    x_matching = True
                    num += 1
            return 0

        def number_of_c_and_x(case):
            num = 0
            x_matching = False
            c_matching = False
            for ev in case:
                if event_matching(ev, cause):
                    c_matching = True
                    num += 1
                if event_matching(ev, x_obj):
                    x_matching = True
                    num += 1
            if x_matching and c_matching: return num
            return 0


        return utils.divide_or_zero(sum([number_of_c_and_x_preceding_e(c) for c in cases]), sum([number_of_c_and_x(c) for c in cases]))



    def p_e_notc_x(hypothesis, x_val):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]
        x_obj = (cause[0], x_val)

        def number_of_notc_and_x_preceding_e(case):
            num = 0
            for ev in case:
                if event_matching(ev, effect): return num
                if event_matching(ev, cause): return 0
                if event_matching(ev, x_obj): num += 1
            return 0

        def number_of_notc_and_x(case):
            num = 0
            for ev in case:
                if event_matching(ev, cause): return 0
                if event_matching(ev, x_obj): num += 1
            return num

        return utils.divide_or_zero(sum([number_of_notc_and_x_preceding_e(c) for c in cases]), sum([number_of_notc_and_x(c) for c in cases]))

    def calculate_epsilon_for_hypothesis(hypothesis):
        cause = hypothesis["cause"]
        x_vals = get_all_values_for_state_attribute(prepared_event_log, cause[0])
        epsilons = [p_e_c_x(hypothesis, x) - p_e_notc_x(hypothesis, x) for x in x_vals if x != cause[1]]
        if len(epsilons) == 0: return 0
        return statistics.mean(epsilons)

    return [calculate_epsilon_for_hypothesis(h) for h in prima_facie_hypotheses]