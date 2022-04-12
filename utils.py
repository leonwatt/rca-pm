import csv


def read_from_file(path):
    with open(path) as f:
        return f.read()

def write_to_file(path, content):
    with open(path, "w") as f:
        f.write(str(content))


def read_csv(path, delimiter = ","):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def write_csv(path, content):
    with open(path, "w") as f:
        writer = csv.writer(f)
        header = content[0].keys()
        writer.writerow(header)
        writer.writerows([[row[h] for h in list(header)] for row in content])

def group_by(arr_of_dicts, grouping_attr):
    res = {}

    for el in arr_of_dicts:
        grouping_value = el[grouping_attr]
        res.setdefault(grouping_value, [])
        res[grouping_value] += [el]

    return res