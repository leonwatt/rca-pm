import utils
from utils import event_matching

def prima_facie_filter_hypotheses(prepared_event_log, hypotheses):
    cases = utils.group_by_as_list(prepared_event_log, "case")

    def _p_e(hypothesis):
        effect = hypothesis["effect"]
        return len([c for c in cases if any([event_matching(e, effect) for e in c])]) / len(cases)
    
    def p_e(hypothesis):
        effect = hypothesis["effect"]
        return len([e for e in prepared_event_log if event_matching(e, effect)]) / len(prepared_event_log)

    def _p_e_c(hypothesis):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]

        def number_of_cause_occurances_in_case(case):
            return len([ev for ev in case if event_matching(ev, cause)])
        
        def number_of_cause_until_effect(case):
            res = 0
            for ev in case:
                if event_matching(ev, effect): return res
                if event_matching(ev, cause): res += 1
            return 0

        num_c = sum([number_of_cause_occurances_in_case(case) for case in cases])
        num_c_and_e = sum([number_of_cause_until_effect(c) for c in cases])

        # print(num_cases_with_e_and_c)
        # print(num_cases_with_c)
        # print()

        if num_c == 0: return 0
        return num_c_and_e / num_c

    def p_e_c(hypothesis):
        cause = hypothesis["cause"]
        effect = hypothesis["effect"]

        def is_case_containing_cause(case):
            return any([event_matching(ev, cause) for ev in case])
        
        def is_cause_followed_by_effect_in_case(case):
            cause_present = False
            for ev in case:
                if cause_present and event_matching(ev, effect): return True
                if event_matching(ev, cause): cause_present = True
            return False

        num_cases_with_c = len([c for c in cases if is_case_containing_cause(c)])
        num_cases_with_e_and_c = len([c for c in cases if is_cause_followed_by_effect_in_case(c)])

        # print(num_cases_with_e_and_c)
        # print(num_cases_with_c)
        # print()

        if num_cases_with_c == 0: return 0
        return num_cases_with_e_and_c / num_cases_with_c


    # for h in hypotheses:
    #     print(p_e_c(h))
    #     print(p_e(h))
    #     print()

    return [h for h in hypotheses if p_e_c(h) > p_e(h)]