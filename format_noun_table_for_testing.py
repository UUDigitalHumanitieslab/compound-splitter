import csv

input_file = "./nominalijst_raw.csv"
output_file = "./nominalijst.csv"


with open(input_file) as in_file:
    reader = csv.DictReader(in_file)

    def parse(row):
        is_compound = bool(int(row['samenst']))

        if not is_compound:
            data = {
                'word': row['woord'],
                'is_compound': is_compound
            }
        else:
            data = {
                'word': row['woord'],
                'is_compound': is_compound,
                'n_parts': int(row['aantal_delen']),
                'head': row['hoofdwoord'],
                'satellite': row['satelliet_schoon']
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
        if parts:
            writer.writerow({'compound': word, 'expected': parts})
