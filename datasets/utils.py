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
                # print(f'Column names are {row}')
                columns = row
                line_count += 1
            else:
                new_item = {}
                for ind in range(len(columns)):
                    new_item[columns[ind].lower()] = row[ind]
                if file == "ads":
                    new_item["is_published"] = True if new_item.get("is_published") == "TRUE" else False
                print(new_item)
                data.append(new_item)

    # print(data)
    # f_json = open("ads.json", encoding="UTF-8")
    with open(f"{file}.json", 'w', encoding="UTF-8") as f:
        # f.write(data)
        json.dump(data,  f)


csv_to_json("ads")
csv_to_json("categories")

# def json_to_cat(file):
#     with open(file, encoding='utf-8') as f:
#         json_data = json.loads(f.read())
#
#         for item in json_data:
#             cat = Category.objects.get_or_create(**item)
#             # movie and genres created
# json_to_cat("categories.json")
