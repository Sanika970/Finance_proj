"""Basic NPV and IRR on a list of periodic cash flows (index 0 = today)."""


def npv(rate, cashflows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, low=-0.99, high=1.0, tol=1e-7, max_iter=200):
    """Internal rate of return by bisection. Returns None if no sign change."""
    f_low, f_high = npv(low, cashflows), npv(high, cashflows)
    if f_low * f_high > 0:
        return None
    for _ in range(max_iter):
        mid = (low + high) / 2
        f_mid = npv(mid, cashflows)
        if abs(f_mid) < tol:
            return mid
        if f_low * f_mid < 0:
            high, f_high = mid, f_mid
        else:
            low, f_low = mid, f_mid
    return (low + high) / 2
