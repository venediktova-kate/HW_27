import csv
import json


def convert(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if 'is_published' in row:
                if row['is_published'] == "TRUE":
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            result.append({"model": model, "fields": row})

    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    convert('ads.csv', 'ads.json', 'ad')
    convert('categories.csv', 'categories.json', 'category')
