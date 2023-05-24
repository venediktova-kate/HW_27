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

            if 'location_id' in row:
                row['locations'] = [row['location_id']]
                del row['location_id']

            result.append({"model": model, "fields": row})

    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    convert('ad.csv', 'ad.json', 'ads.ad')
    convert('category.csv', 'category.json', 'ads.category')
    convert('location.csv', 'location.json', 'users.location')
    convert('user.csv', 'user.json', 'users.user')
