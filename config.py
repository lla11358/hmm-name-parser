"""Configuration file for hmm_name_parser.py."""

# Pattern used to extract tokens
token_pattern = '([a-z-]+|ben|da|das|de|del|den|der|des|di|do|dos|du|el|i|la|las|le|lo|los|mac|mc|san|st|van|von|y)+'
# List of particles for first name and last_name
particles = [
    'ben',
    'da',
    'das',
    'de',
    'del',
    'den',
    'der',
    'des',
    'di',
    'do',
    'dos',
    'du',
    'el',
    'i',
    'la',
    'las',
    'le',
    'lo',
    'los',
    'mac',
    'mc',
    'san',
    'st',
    'van',
    'von',
    'y'
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
