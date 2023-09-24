import json

json_data = {}

with open('data/words2.txt', 'r') as file:
    for each in file:
        key, value = each.strip(), 1
        json_data[key] = value

with open('dict_words.json', 'w') as f:
    json.dump(json_data, f, indent=2)



print(json_data)
