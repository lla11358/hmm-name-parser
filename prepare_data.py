"""
Obtains discrete probability distributions from source data.

1. split names and particles
2. subtoken extraction
3. distributions of probabilities

"""


import config
import pandas

fn = pandas.DataFrame()
ln = pandas.DataFrame()


def main():
    """
    Process input data files.
    """

    # Load csv files into dataframes.
    for file in config.fn_file:
        fn.read_csv(
            config.staging_dir + file
        )
    for file in config.ln_file:
        ln.read_csv(
            config.staging_dir + file
        )

    


if __name__ == '__main__':
    main()
