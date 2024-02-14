from statistics import median, stdev


def rolls_needed_for_probability(rolls_list: list[int], target_probability: float) -> int:
    """Calculate rolls needed to achieve target probability."""
    rolls_list = sorted(rolls_list)
    total_rolldowns = len(rolls_list)

    # Calculate the empirical cumulative distribution function (ECDF).
    ecdf = [i / total_rolldowns for i in range(1, total_rolldowns + 1)]

    # Find the index where the ECDF first exceeds or equals the target probability.
    index = next(i for i, p in enumerate(ecdf) if p >= target_probability)

    # The number of rolls needed is the corresponding element in the rolldown list.
    return rolls_list[index]

def get_stats(rolls_list: list[int], probabilities: list[float] | None = None) -> list[float]:
    """Compute statistics."""
    if probabilities is None:
        probabilities = [0.5, 0.75, 0.9]

    rolls_needed = [rolls_needed_for_probability(rolls_list, prob)
                    for prob in probabilities]
    med = median(rolls_list)
    dev = stdev(rolls_list)
    return rolls_needed, med, dev




