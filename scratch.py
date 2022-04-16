# import utils

# eventlog = utils.read_csv("event-logs/original-paper.csv")
# cases = utils.group_by_as_list(eventlog, "case")
# print(len(cases))
# # print(cases[0])
# print(len([c for c in cases if any([ev for ev in c if ev["activity"] == "Case Delayed"])]))
# print(len([ev for ev in eventlog if ev["activity"] == "Case Delayed"]))

obj = {"a": "b"}
print([x for x in obj])