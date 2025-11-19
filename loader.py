# loader.py
"""
Functions for loading and validating services.csv
Exports:
- load_services(filename) -> dict
- parse_service_block(lines, start_idx) -> (service_name, service_dict, next_index)
"""

import csv
from typing import Dict, List, Tuple

def load_services(filename: str = 'services.csv') -> Dict[str, dict]:
    """
    Read services.csv and return a dict:
    {
      "Compute": {
         "units": "hour",
         "tiers": [0,50,1000,8000],
         "costs": [0.62,0.58,0.55,0.52]
      }, ...
    }
    Raises:
      FileNotFoundError if file missing
      ValueError on malformed file
    """
    services = {}
    with open(filename, newline='') as csvfile:
        reader = list(csv.reader(csvfile))
        # Remove empty rows
        rows = [row for row in reader if row and any(cell.strip() for cell in row)]
        i = 0
        while i < len(rows):
            # Expect: <ServiceName>,<units>
            header = rows[i]
            if len(header) < 2:
                raise ValueError(f"Malformed header row at line {i+1}: {header}")
            service_name = header[0].strip()
            units = header[1].strip()
            if not service_name:
                raise ValueError(f"Empty service name at line {i+1}")
            # Next line: tier starts
            if i+1 >= len(rows):
                raise ValueError(f"Missing tier line for service {service_name}")
            tier_line = rows[i+1]
            try:
                tiers = [float(x) for x in tier_line]
            except Exception as e:
                raise ValueError(f"Malformed tiers for {service_name}: {e}")
            if i+2 >= len(rows):
                raise ValueError(f"Missing cost line for service {service_name}")
            cost_line = rows[i+2]
            try:
                costs = [float(x) for x in cost_line]
            except Exception as e:
                raise ValueError(f"Malformed costs for {service_name}: {e}")
            if len(costs) != len(tiers):
                raise ValueError(f"Tiers and costs length mismatch for {service_name}")
            services[service_name] = {
                "units": units,
                "tiers": tiers,
                "costs": costs
            }
            i += 3
    return services

