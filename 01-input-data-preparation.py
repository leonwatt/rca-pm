import utils
import os
import statistics
import datetime


def prepare_input(path = os.path.join("event-logs", "log.csv")):
    event_log = utils.read_csv(path)

    def parse_timestamp(event):
        return datetime.datetime.strptime(event["timestamp"], utils.DATE_FORMAT)

    first_timestamp = parse_timestamp(event_log[0])
    for e in event_log:
        e["deadline_exceeded"] = e["deadline_exceeded"] == "True"
        e["rel_timestamp"] = (parse_timestamp(e) - first_timestamp).total_seconds() / 3600 / 24

    cases = list(utils.group_by(event_log, "case").values())

    def print_event_log_stats():
        print("=== STATS ===")
        print(str(len([c for c in cases if any([e["deadline_exceeded"] for e in c])])) + f"/{len(cases)} cases exceeded the deadline")
        print(f"Median case length (#events): {statistics.median([len(c) for c in cases])}")
        print(f"Median case length (days): {statistics.median([c[-1]['rel_timestamp'] - c[0]['rel_timestamp'] for c in cases])}")
        print()

    print_event_log_stats()

    print(event_log[10])