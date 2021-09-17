import pandas
import numpy as np
import json

max_part = 5
df = pandas.read_csv('car_database.csv')

intro = {"item_num": len(df),
         "attrs": {"discrete": [],
                   "continuous": []
                   }}
for attr in df.columns:
    if 'Unnamed' in attr:
        continue
    if df[attr].dtypes in [np.object, np.unicode, np.str]:
        intro['attrs']['discrete'].append(attr)
    else:
        intro['attrs']['continuous'].append(attr)
attr_details = {'discrete': {}, 'continuous': {}}
for attr in intro['attrs']['discrete']:
    type_counter = {}
    for item in df[attr]:
        if item not in type_counter.keys():
            type_counter[item] = 1
        else:
            type_counter[item] += 1
    if len(type_counter.keys()) < max_part:
        attr_details['discrete'][attr] = type_counter
    else:
        type_counter = {k: v for k, v in sorted(
            type_counter.items(), key=lambda item: item[1], reverse=True)}
        part_counter = {k: type_counter[k]
                        for k in list(type_counter.keys())[:max_part]}
        rest_counter = 0
        for val in list(type_counter.values())[max_part:]:
            rest_counter += val
        part_counter['rest'] = rest_counter
        attr_details['discrete'][attr] = part_counter

for attr in intro['attrs']['continuous']:
    value = np.asarray(df[attr])
    min_val, max_val = np.min(value), np.max(value)
    range_val = max_val-min_val
    sparse = max_part
    counter = []
    for i in range(sparse):
        counter.append(int(((value >= min_val+range_val*i/sparse) &
                            (value <= min_val+range_val*(i+1)/sparse)).sum()))
    attr_details['continuous'][attr] = {'min': int(
        min_val), 'max': int(max_val), 'counter': counter}
intro['attr_details'] = attr_details
json.dump(intro, open('car_db.json', 'w'))
