import main
import os

if __name__ == '__main__':
    SYSTEM_STATES = {
        "activity": lambda e: e["activity"]
    }
    main.run(os.path.join("event-logs", "original-paper.csv"), SYSTEM_STATES, causes_key="activity", effects_key="activity", effects_values=["Case Delayed"])