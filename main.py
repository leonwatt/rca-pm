from input_data_preparation import prepare_input
from hypotheses_generation import generate_hypotheses
from prima_facie import prima_facie_filter_hypotheses

if __name__ == '__main__':

    SYSTEM_STATES = {
        "resource": lambda e: e["resource"],
        "deadline": lambda e: e["deadline_exceeded"]
    }

    prepared_event_log = prepare_input(SYSTEM_STATES)
    # print(input)
    
    hypotheses = generate_hypotheses(prepared_event_log, causes_key="resource", effects_key="deadline", effects_values=[True])
    # print(hypotheses)
    print(len(hypotheses))

    prima_facie_hypotheses = prima_facie_filter_hypotheses(prepared_event_log, hypotheses)
    print(prima_facie_hypotheses)
    print(len(prima_facie_hypotheses))