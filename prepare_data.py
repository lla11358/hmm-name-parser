"""
Obtains discrete probability distributions from source data.

1. split names and particles
2. subtoken extraction
3. distributions of probabilities

"""

import pandas
import normalizer
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
    first_name_df = pandas.concat(list, axis=0, ignore_index=True)

    list = []
    for file in config.ln_file:
        df = pandas.read_csv(
            config.staging_dir + file,
            sep=',',
            encoding=config.encoding
        )
        list.append(df)
    last_name_df = pandas.concat(list, axis=0, ignore_index=True)

    # Extract tokens
    

if __name__ == '__main__':
    main()
