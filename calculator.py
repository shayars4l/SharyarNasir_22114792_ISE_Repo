# calculator.py
"""
Cost calculation logic for ICSC
Exports:
- calculate_service_cost(service_def, amount) -> float
- calculate_all_costs(services, subscriptions) -> dict
- format_currency(amount) -> str
"""

from typing import Dict, List

def calculate_service_cost(service_def: Dict, amount: float) -> float:
    """
    Determine cost for a single service.
    IMPORTANT: Pricing is not progressive — the *single* per-unit cost
    is chosen by the tier that starts at the highest value <= amount,
    then cost = amount * per_unit_cost.
    Example: tiers [0,50,1000], costs [0.62,0.58,0.55].
    amount=100 => cost-per-unit = 0.58 -> total = 100*0.58
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    tiers: List[float] = service_def["tiers"]
    costs: List[float] = service_def["costs"]
    # Find rightmost tier start <= amount
    chosen_index = 0
    for idx, tier_start in enumerate(tiers):
        if amount >= tier_start:
            chosen_index = idx
        else:
            break
    per_unit = costs[chosen_index]
    return amount * per_unit

def calculate_all_costs(services: Dict[str, Dict], subscriptions: Dict[str, float]) -> Dict[str, dict]:
    """
    Returns breakdown:
    {
      "Compute": {"amount":100,"units":"hour","per_unit":0.58,"cost":58.0},
      ...
      "TOTAL": 123.45
    }
    services: as from loader.load_services
    subscriptions: { "Compute": 100, ... }
    """
    breakdown = {}
    total = 0.0
    for svc, amt in subscriptions.items():
        if svc not in services:
            raise KeyError(f"Service {svc} not defined")
        service_def = services[svc]
        cost = calculate_service_cost(service_def, amt)
        # determine per_unit displayed
        # get chosen tier index again
        tiers = service_def["tiers"]
        costs = service_def["costs"]
        chosen_idx = 0
        for idx, start in enumerate(tiers):
            if amt >= start:
                chosen_idx = idx
            else:
                break
        per_unit = costs[chosen_idx]
        breakdown[svc] = {
            "amount": amt,
            "units": service_def["units"],
            "per_unit": per_unit,
            "cost": round(cost, 2)
        }
        total += cost
    breakdown["TOTAL"] = round(total, 2)
    return breakdown

def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"
