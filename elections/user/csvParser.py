import csv
import io


def parse(csvFile):
    content = io.StringIO(csvFile.stream.read().decode("utf-8"))
    reader = csv.reader(content)
    data = []
    line = 0
    for row in reader:
        if len(row) != 2:
            data.clear()
            data.append("error")
            data.append(f"Incorrect number of values on line {line}.")
            return data
        if not row[1].isdigit() or int(row[1]) < 0:
            data.clear()
            data.append("error")
            data.append(f"Incorrect poll number on line {line}.")
            return data
        data.append(row)
        line += 1
    return data