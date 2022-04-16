from input_data_preparation import prepare_input
from hypotheses_generation import generate_hypotheses
import prima_facie
import epsilon_calculation
from event_log_utils import print_hypotheses, print_hypotheses_with_epsilon

def run(event_log_path, system_states, causes_key, effects_key, causes_values = None, effects_values = None):
    # Step 1: Input data preparation
    prepared_event_log = prepare_input(system_states, event_log_path)
    
    # Step 2: Generating hypotheses
    hypotheses = generate_hypotheses(prepared_event_log, causes_key=causes_key, causes_values=causes_values, effects_key=effects_key, effects_values=effects_values)
    print_hypotheses(hypotheses)

    # Step 3: Testing for prima facie causes
    prima_facie_hypotheses = prima_facie.prima_facie_new2(prepared_event_log, hypotheses)
    print_hypotheses(prima_facie_hypotheses)
    print(f"{len(hypotheses)} ~> {len(prima_facie_hypotheses)} hypotheses")

    # Step 4: Calculation of epsilon values
    epsilon_values = epsilon_calculation.calculate_epsion_values_new2(prepared_event_log, prima_facie_hypotheses)
    print_hypotheses_with_epsilon(prima_facie_hypotheses, epsilon_values)