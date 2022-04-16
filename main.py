import time
import input_data_preparation
import hypotheses_generator
import prima_facie
import epsilon_calculation
import event_log_utils

def run(event_log_path, system_states, causes_key, effects_key, causes_values = None, effects_values = None, case_attribute = "case", timestamp_attribute = "timestamp"):
    # Step 1: Input data preparation
    prepared_event_log = input_data_preparation.prepare(system_states, event_log_path, case_attribute, timestamp_attribute)
    
    # Step 2: Generating hypotheses
    hypotheses = hypotheses_generator.generate(prepared_event_log, causes_key=causes_key, causes_values=causes_values, effects_key=effects_key, effects_values=effects_values)
    event_log_utils.print_hypotheses(hypotheses)

    # Step 3: Testing for prima facie causes
    prima_facie_hypotheses = prima_facie.peform_filtering(prepared_event_log, hypotheses)
    event_log_utils.print_hypotheses(prima_facie_hypotheses)
    print(f"{len(hypotheses)} ~> {len(prima_facie_hypotheses)} hypotheses")

    # Step 4: Calculation of epsilon values
    epsilon_values = epsilon_calculation.calculate_values(prepared_event_log, prima_facie_hypotheses)
    event_log_utils.print_hypotheses_with_epsilon(prima_facie_hypotheses, epsilon_values)