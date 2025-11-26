# ui.py
"""
User interface (CLI) functions.
"""

from typing import Dict
from calculator import calculate_all_costs, format_currency
import sys

def display_welcome():
    print("Welcome to ICSC – ISE Cloud Services Calculator\n")

def display_services_menu(services: Dict[str, dict]):
    print("Add/Modify subscription for:")
    keys = list(services.keys())
    for i, name in enumerate(keys, start=1):
        units = services[name]['units']
        print(f"{i}) {name} ({units})")
    print("s) List subscriptions and totals")
    print("$) Display cost breakdown")
    print("q) Quit")

def prompt_for_amount(service_name: str, current_amount: float, units: str) -> float:
    while True:
        print(f"You chose {service_name} ({units})")
        try:
            new_amt = input(f"Current {units} amount: {current_amount} Enter new {units} amount: ").strip()
            if new_amt == "":
                return current_amount
            amt = float(new_amt)
            if amt < 0:
                print("Amount cannot be negative. Try again.")
                continue
            return amt
        except ValueError:
            print("Invalid number. Try again.")

def display_subscriptions(subscriptions: Dict[str, float]):
    if not subscriptions:
        print("No subscriptions yet.")
        return
    print("You have subscriptions for:")
    for svc, amt in subscriptions.items():
        print(f"{svc}: {amt}")

def display_breakdown(breakdown: Dict[str, dict]):
    print("\nYour current cost breakdown is:")
    for svc, info in breakdown.items():
        if svc == "TOTAL":
            continue
        amt = info['amount']
        per = info['per_unit']
        cost = info['cost']
        units = info['units']
        print(f"{svc}: {amt} {units} @ ${per:.2f} = {format_currency(cost)}")
    print(f"TOTAL: {format_currency(breakdown.get('TOTAL', 0.0))}\n")

def main_menu(services: Dict[str, dict]):
    display_welcome()
    keys = list(services.keys())
    subscriptions = {k: 0.0 for k in keys}  # start all at 0
    while True:
        display_services_menu(services)
        choice = input("> ").strip()
        if choice.lower() == 'q':
            print("Goodbye.")
            sys.exit(0)
        elif choice.lower() == 's':
            display_subscriptions({k: v for k, v in subscriptions.items() if v > 0})
        elif choice == '$':
            breakdown = calculate_all_costs(services, {k: v for k, v in subscriptions.items() if v > 0})
            display_breakdown(breakdown)
        else:
            # numeric selection
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(keys):
                    svc_name = keys[idx]
                    current = subscriptions.get(svc_name, 0.0)
                    units = services[svc_name]['units']
                    new_amt = prompt_for_amount(svc_name, current, units)
                    subscriptions[svc_name] = new_amt
                else:
                    print("Invalid selection number.")
            except ValueError:
                print("Invalid selection. Choose a number, 's', '$' or 'q'.")
