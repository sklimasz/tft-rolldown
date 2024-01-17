from statistics import median, stdev

def rolls_needed_for_probability(rolldown_list, target_probability):
    rolldown_list = sorted(rolldown_list)
    total_rolldowns = len(rolldown_list)

    # Calculate the empirical cumulative distribution function (ECDF)
    ecdf = [i / total_rolldowns for i in range(1, total_rolldowns + 1)]

    # Find the index where the ECDF first exceeds or equals the target probability
    index = next(i for i, p in enumerate(ecdf) if p >= target_probability)

    # The number of rolls needed is the corresponding element in the rolldown list
    rolls_needed = rolldown_list[index]

    return rolls_needed

def get_stats(list, probabilities=None):
    """Compute statistics"""
    if probabilities is None:
        probabilities = [0.5, 0.75, 0.9]
    
    rolls_needed = [rolls_needed_for_probability(list, prob) for prob in probabilities]
    med = median(list)
    dev = stdev(list)
    
    return rolls_needed, med, dev




