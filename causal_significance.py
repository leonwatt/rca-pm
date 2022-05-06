import statistics

def calculate_z_values(epsilon_values):
    mu = statistics.mean(epsilon_values)
    sigma = statistics.stdev(epsilon_values)
    return [(e - mu) / sigma for e in epsilon_values]