import utils
import prima_facie

event_log = utils.read_csv("event-logs/log.csv")
print(prima_facie.test_prima_facie(event_log, "A", "J"))