"""
Obtains discrete probability distributions from source data.

1. split names and particles
2. subtoken extraction
3. distributions of probabilities

"""

import pandas
import tokenizer
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

    # Generate dictionaries of tokens and its frequencies
    tokens = {}
    for index, row in first_name.iterrows():
        name = tokenizer.unicode(row['nombre'])
        freq = row['frec']
        token_list = tokenizer.split_sequence(name, config.token_pattern)

    for line in open(file_name):
        line = line.strip('\n')
        line = tokenizer.unicode(line)
        # List of tokens from each line
        line_tokens = tokenizer.split_sequence(line, config.token_pattern)
        line_tokens = tokenizer.subtokens(
            line_tokens, config.subtoken_length, config.particles)
        for token in line_tokens:
            if token in config.particles:
                particle_tokens.append(token)
            else:
                name_tokens.append(token)
    return tokens



if __name__ == '__main__':
    main()
