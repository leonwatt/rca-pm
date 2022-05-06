import utils

def save_results(out_path, prima_facie_hypotheses, epsilon_values, z_values):
    utils.write_csv(out_path, [{
        "cause_key": h["cause"][0],
        "cause_value": h["cause"][1],
        "effect_key": h["effect"][0],
        "effect_value": h["effect"][1],
        "epsilon": epsilon_values[index],
        "z": z_values[index]
    } for (index, h) in enumerate(prima_facie_hypotheses)])