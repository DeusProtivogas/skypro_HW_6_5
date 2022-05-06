import csv
import json



def csv_to_json(file):
    data = []
    with open(f"{file}.csv", encoding="UTF-8") as f:
        columns = []
        line_count = 0
        csvReader = csv.reader(f, delimiter=',')
        for row in csvReader:
            if line_count == 0:
                columns = row
                line_count += 1
            else:
                new_item = {}
                for ind in range(len(columns)):
                    new_item[columns[ind].lower()] = row[ind]
                if file == "ads":
                    new_item["is_published"] = True if new_item.get("is_published") == "TRUE" else False
                data.append(new_item)

    with open(f"{file}.json", 'w', encoding="UTF-8") as f:
        json.dump(data,  f)


csv_to_json("ads")
csv_to_json("categories")

