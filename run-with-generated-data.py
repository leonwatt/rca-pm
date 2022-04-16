import main
import os

if __name__ == '__main__':
    SYSTEM_STATES = {
        "activity-resource": lambda e: e["activity"] + "-" + e["resource"],
        "resource": lambda e: e["resource"],
        "activity": lambda e: e["activity"],
        "deadline": lambda e: e["deadline_exceeded"]
    }
    main.run(os.path.join("event-logs", "log.csv"), SYSTEM_STATES, causes_key="resource", effects_key="deadline", effects_values=["True"])