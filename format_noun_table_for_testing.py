import csv

# Reads the nouns_semtype.data from tscan/data.
# This file has a restricted license and is not included in the
# distribution.
input_file = "../tscan/data/nouns_semtype.data"
output_file = "./test_sets/nouns_semtype.csv"


with open(input_file) as in_file:
    reader = csv.reader(in_file, delimiter='\t')

    def parse(row):
        is_compound = bool(int(row[2]))

        if not is_compound:
            data = {
                'word': row[0],
                'is_compound': is_compound
            }
        else:
            data = {
                'word': row[0],
                'is_compound': is_compound,
                'n_parts': int(row[5]),
                'head': row[3],
                'satellite': row[4]
            }

        return data

    data_sequence = [parse(row) for row in reader]
    all_data = {data['word']: data for data in data_sequence}


def parts(word):
    if word not in all_data:
        return None

    data = all_data[word]

    if not data['is_compound']:
        return data['word']

    sat, head = data['satellite'], data['head']

    if data['n_parts'] == 2:
        return f'{sat}_{head}'
    else:
        sat_parts = parts(sat)
        if sat_parts:
            return f'{sat_parts}_{head}'
        else:
            return None


words_parts = {word: parts(word) for word in all_data}

with open(output_file, 'w') as out_file:
    writer = csv.DictWriter(out_file, fieldnames=['compound', 'expected'])
    writer.writeheader()

    for word, parts in words_parts.items():
        if parts is not None:
            writer.writerow({'compound': word, 'expected': parts})
