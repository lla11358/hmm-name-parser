"""Configuration file for hmm_name_parser.py."""

# Text case for generate tokens: 'upper' | 'lower' | None
text_case = 'lower'
# Pattern used to extract words
word_pattern = '([a-z-]+)+'
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
# Length of tokens
token_length = 4
# Graph types: First Name first or Last Name first
graph_types = ['FNF', 'LNF']
graph_type = graph_types[0]
# Raw data files
staging_dir = 'data/staging/'
input_dir = 'data/input/'
output_dir = 'data/output/'
fn_file = ['mujeres.csv', 'hombres.csv']
ln_file = ['apellidos.csv', 'apellidos-20.csv']
test_set_file = input_dir + 'tagged_names_fnf.dict'
encoding = 'utf-8'
# Token files
token_files = {
    'first_name': 'first_name_tokens.dict',
    'part_first_name': 'part_first_name_tokens.dict',
    'last_name1': 'last_name1_tokens.dict',
    'part_last_name1': 'part_last_name1_tokens.dict',
    'last_name2': 'last_name2_tokens.dict',
    'part_last_name2': 'part_last_name2_tokens.dict'
}
