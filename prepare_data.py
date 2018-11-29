"""
Obtains discrete probability distributions from source data.

This module is extremely coupled with data files provided by the
National Statistics Institute of Spain (INE).

1. split names and particles
2. subtoken extraction
3. distributions of probabilities

"""

import pandas
import re
import utils
import config


def main():
    """
    Process data source files.

    Generates a discrete distribution of probabilities for each state.

    """
    # Load csv files into dataframes.
    list = []
    for file in config.fn_file:
        df = pandas.read_csv(
            config.staging_dir + file,
            sep=',',
            encoding=config.encoding
        )
        list.append(df)
    first_name = pandas.concat(list, axis=0, ignore_index=True)
    first_name = first_name.dropna(axis='rows')

    list = []
    for file in config.ln_file:
        df = pandas.read_csv(
            config.staging_dir + file,
            sep=',',
            encoding=config.encoding
        )
        list.append(df)
    last_name = pandas.concat(list, axis=0, ignore_index=True)
    last_name = last_name.dropna(axis='rows')

    # Generate probability distributions for tokens and particles
    # A) first names and particles of first name
    first_name_tokens = {}
    part_first_name_tokens = {}
    first_name_total = 0
    part_first_name_total = 0
    for index, row in first_name.iterrows():
        text = utils.normalize(row['nombre'], config.text_case)
        freq = row['frec']
        words = re.findall(config.word_pattern, text)

        for word in words:
            if word in config.particles:
                if word not in part_first_name_tokens:
                    part_first_name_tokens[word] = freq
                else:
                    part_first_name_tokens[word] += freq
                part_first_name_total += freq
            else:
                token = utils.to_token(word, config.token_length)
                if token not in first_name_tokens:
                    first_name_tokens[token] = freq
                else:
                    first_name_tokens[token] += freq
                first_name_total += freq

    # Calculate probabilities
    for key, value in part_first_name_tokens.items():
        part_first_name_tokens[key] = \
            float(value) / float(part_first_name_total)
    for key, value in first_name_tokens.items():
        first_name_tokens[key] = \
            float(value) / float(first_name_total)

    # Save probability distributions to file
    utils.save_dict_to_file(
        part_first_name_tokens,
        config.input_dir + config.token_files['part_first_name']
    )
    utils.save_dict_to_file(
        first_name_tokens,
        config.input_dir + config.token_files['first_name']
    )

    # B) last names and particles of last name
    last_name1_tokens = {}
    part_last_name1_tokens = {}
    last_name2_tokens = {}
    part_last_name2_tokens = {}
    last_name1_total = 0
    part_last_name1_total = 0
    last_name2_total = 0
    part_last_name2_total = 0
    for index, row in last_name.iterrows():
        text = utils.normalize(row['apellido'], config.text_case)
        freq1 = row['frec_pri']
        freq2 = row['frec_seg']
        freqr = row['freq_rep']
        words = re.findall(config.word_pattern, text)

        for word in words:
            if word in config.particles:
                if word not in part_last_name1_tokens:
                    part_last_name1_tokens[word] = freq1 + freqr
                else:
                    part_last_name1_tokens[word] += freq1 + freqr
                part_last_name1_total += freq1 + freqr
                if word not in part_last_name2_tokens:
                    part_last_name2_tokens[word] = freq2 + freqr
                else:
                    part_last_name2_tokens[word] += freq2 + freqr
                part_last_name2_total += freq2 + freqr
            else:
                token = utils.to_token(word, config.token_length)
                if token not in last_name1_tokens:
                    last_name1_tokens[token] = freq1 + freqr
                else:
                    last_name1_tokens[token] += freq1 + freqr
                last_name1_total += freq1 + freqr
                if token not in last_name2_tokens:
                    last_name2_tokens[token] = freq2 + freqr
                else:
                    last_name2_tokens[token] += freq2 + freqr
                last_name2_total += freq2 + freqr

    # Calculate probabilities
    # Last name 1
    for key, value in part_last_name1_tokens.items():
        part_last_name1_tokens[key] = \
            float(value) / float(part_last_name1_total)
    for key, value in last_name1_tokens.items():
        last_name1_tokens[key] = \
            float(value) / float(last_name1_total)
    # Save probability distributions to file
    utils.save_dict_to_file(
        part_last_name1_tokens,
        config.input_dir + config.token_files['part_last_name1']
    )
    utils.save_dict_to_file(
        last_name1_tokens,
        config.input_dir + config.token_files['last_name1']
    )
    # Last name 2
    for key, value in part_last_name2_tokens.items():
        part_last_name2_tokens[key] = \
            float(value) / float(part_last_name2_total)
    for key, value in last_name2_tokens.items():
        last_name2_tokens[key] = \
            float(value) / float(last_name2_total)
    # Save probability distributions to file
    utils.save_dict_to_file(
        part_last_name2_tokens,
        config.input_dir + config.token_files['part_last_name2']
    )
    utils.save_dict_to_file(
        last_name2_tokens,
        config.input_dir + config.token_files['last_name2']
    )


if __name__ == '__main__':
    main()
