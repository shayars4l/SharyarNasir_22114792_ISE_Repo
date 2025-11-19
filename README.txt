ISE Cloud Services Calculator (ICSC)
===================================

Author: Sharyar Nasir
Student ID: 22114792
Repo name: SharyarNasir_22114792_ISE_Repo

Files:
- main.py             : Entry point (CLI)
- loader.py           : services.csv parsing
- calculator.py       : cost calculation logic
- ui.py               : CLI menu and I/O
- services.csv        : Sample service definitions (required)
- tests/              : Unit tests (black-box & white-box)
- documentation/      : PDF doc content (to be generated)
- video.mp4           : 2-minute demo (you must record)
- .git/               : your git directory (include it in the .zip)

Requirements:
- Python 3.8+ (available in Curtin Linux labs)
- No external packages required

How to run:
1. Ensure you are in the repo root (where services.csv exists).
2. Run the program:
   $ python3 main.py

3. To run tests:
   From repo root:
   $ python3 -m unittest discover -v

Notes for the marker:
- The program reads services.csv in the current working directory.
- The UI allows adding/modifying subscription amounts, listing subscriptions, and showing a cost breakdown.
- Pricing uses tiered per-unit pricing (non-progressive — entire amount charged at per-unit of applicable tier).

Packaging:
- Create a .zip of the repository folder, making sure the hidden .git directory is included.
