from datetime import datetime
import numpy as np

def ecart_type_publications(dates):
    dates_dt = sorted([datetime.fromisoformat(d) for d in dates])
    intervalles = [(dates_dt[i] - dates_dt[i-1]).days for i in range(1, len(dates_dt))]
    if len(intervalles) >= 2:
        return np.std(intervalles)
    else:
        return None

dates_ex1 = [
    "2024-12-01",
    "2025-01-01",
    "2025-02-01",
    "2025-03-01",
    "2025-04-01"
]

dates_ex2 = [
    "2023-01-01",
    "2023-12-01",
    "2024-12-01",
    "2025-03-01",
    "2025-04-01"
]

ecart_type_ex1 = ecart_type_publications(dates_ex1)
ecart_type_ex2 = ecart_type_publications(dates_ex2)

print("Écart-type exemple 1 :", 1/ecart_type_ex1)
print("Écart-type exemple 2 :", 1/ecart_type_ex2)
