import csv
import os

def convert(column:int, value):
    if column <= 2:
        return value
    elif column == 3:
        return int(value)
    elif column == 4:
        return float(value)

def InternalSort(filename:str, column:int, rev:bool):
    table = []
    with open(filename, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            table.append(row)
    lenTable = len(table)
    table.sort(key=lambda x: convert(column, x[column]), reverse=rev)
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        for row in range(lenTable):
            writer.writerow(table[row])

def split(filename:str):
    rows = -1
    with open(filename, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            rows += 1
    rowsInFile = rows // 10
    with open(filename, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        first = next(reader)
        for i in range(10):
            with open(f"file{i + 1}.txt", "w", newline="", encoding="utf-8-sig") as files:
                writer = csv.writer(files)
                lenF = rowsInFile
                for row in reader:
                    writer.writerow(row)
                    if lenF == 0:
                        break
                    lenF -= 1
    return first

def ExternalSort(filename:str, column:int, rev:bool):
    first = split(filename)
    for i in range(10):
        InternalSort(f"file{i + 1}.txt", column, rev)
    filename = filename.replace(".csv", ".txt")
    files = []
    readers = []
    current = []
    for i in range(10):
        f = open(f"file{i + 1}.txt", encoding="utf-8-sig")
        reader = csv.reader(f)
        files.append(f)
        readers.append(reader)
        current.append(next(reader, None))
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(first)
        while(True):
            valid = []
            for i in range(10):
                if current[i] is not None:
                    valid.append((current[i], i))
            if not valid:
                break
            valid.sort(key=lambda x: convert(column, x[0][column]), reverse=rev)
            writer.writerow(valid[0][0])
            current[valid[0][1]] = next(readers[valid[0][1]], None)
    for f in files:
        f.close()
    for i in range(10):
        os.remove(f"file{i + 1}.txt")