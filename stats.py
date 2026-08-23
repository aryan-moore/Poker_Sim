def confidence_interval(count, n, confidence = 0.95):
     
    """
    Compute a confidence interval for the proportion count/n, using the
    normal approximation to the binomial distribution.
    Returns (proportion, margin_of_error) -- report as proportion ± margin.
    """
     
    if n == 0:
        return (0, 0)
    
    p = count / n
    z = 1.96  # z-score for 95% confidence
    margin_of_error = z * ((p * (1 - p) / n) ** 0.5)
    
    lower_bound = max(0, p - margin_of_error)
    upper_bound = min(1, p + margin_of_error)
    
    return (lower_bound, upper_bound)