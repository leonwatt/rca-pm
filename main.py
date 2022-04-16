from input_data_preparation import prepare_input
from hypotheses_generation import generate_hypotheses
from prima_facie import prima_facie_filter_hypotheses, prima_face_new
from epsilon_calculation import calculate_epsion_values, calculate_epsion_values_new

from event_log_utils import print_hypotheses

if __name__ == '__main__':

    # Configuration
    # SYSTEM_STATES = {
    #     "resource": lambda e: e["resource"],
    #     "deadline": lambda e: e["deadline_exceeded"]
    # }
    SYSTEM_STATES = {
        "activity": lambda e: e["activity"]
    }

    # Step 1: Input data preparation
    # prepared_event_log = prepare_input(SYSTEM_STATES)
    prepared_event_log = prepare_input(SYSTEM_STATES, "event-logs/original-paper.csv")
    
    # Step 2: Generating hypotheses
    # hypotheses = generate_hypotheses(prepared_event_log, causes_key="resource", effects_key="deadline", effects_values=[True])
    hypotheses = generate_hypotheses(prepared_event_log, causes_key="activity", effects_key="activity", effects_values=["Case Delayed"])
    print_hypotheses(hypotheses)
    # print(len(hypotheses))

    # Step 3: Testing for prima facie causes
    # prima_facie_hypotheses = prima_facie_filter_hypotheses(prepared_event_log, hypotheses)
    prima_facie_hypotheses = prima_face_new(prepared_event_log, hypotheses)
    print_hypotheses(prima_facie_hypotheses)
    print(len(prima_facie_hypotheses))

    # Step 4: Calculation of epsilon values
    epsilon_values = calculate_epsion_values_new(prepared_event_log, prima_facie_hypotheses)
    print(epsilon_values)

