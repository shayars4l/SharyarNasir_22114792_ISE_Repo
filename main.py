# main.py

from loader import load_services
from ui import main_menu

def run():
    try:
        services = load_services('services.csv')
    except Exception as e:
        print(f"Failed to load services.csv: {e}")
        return
    main_menu(services)

if __name__ == "__main__":
    run()
