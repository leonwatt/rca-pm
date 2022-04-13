from input_data_preparation import prepare_input
from hypotheses_generation import generate_hypotheses

if __name__ == '__main__':

    SYSTEM_STATES = {
        "resource": lambda e: e["resource"],
        "deadline": lambda e: e["deadline_exceeded"]
    }

    input = prepare_input(SYSTEM_STATES)
    # print(input)
    
    hypotheses = generate_hypotheses(input, causes_key="resource", causes_values=["r1"], effects_key="deadline", effects_values=[True])
    print(hypotheses)