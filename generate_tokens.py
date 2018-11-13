"""
Generates lists of tokens for first name and last name.

Source data extracted from Municipal Register records.
"""

# Create a list of distinct tokens for first name
first_names = [line.split([' ', '-']) for line in open('./data/distinct_first_names.txt')]

