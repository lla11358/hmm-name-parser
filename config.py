"""Configuration file for hmm_name_parser.py."""

# Pattern used to extract particles and tokens
token_pattern = \
    '( de la | de las | de los| del | da | de | di | do | dos | el | i |' + \
    ' la | las | los | le | san | van | y |[a-z-]+)'
# List of particles
particles = [
    ' da ',
    ' de la ',
    ' de las ',
    ' de los ',
    ' del ',
    ' de ',
    ' di ',
    ' do ',
    ' dos ',
    ' el ',
    ' i ',
    ' la ',
    ' las ',
    ' los ',
    ' le ',
    ' san ',
    ' van ',
    ' y '
]
# Length of subtokens
subtoken_length = 3
# Graph types: First Name first or Last Name first
graph_types = ['FNF', 'LNF']
graph_type = graph_types[0]
# Raw data files
data_dir = '/home/lla11358/data/git/python/hmm-name-parser/data/'
staging_dir = data_dir + 'staging/'
input_dir = data_dir + 'input/'
output_dir = data_dir + 'output/'
fn_file = ['mujeres.csv', 'hombres.csv']
ln_file = ['apellidos.csv', 'apellidos-20.csv']
test_set_file = input_dir + 'test_set_fnf.txt'
encoding = 'utf-8'
