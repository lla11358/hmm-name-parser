"""
Hidden Markov Model to parse first names and last names from unstructured text.

Pomegranate documentation:
    https://pomegranate.readthedocs.io/
Code example:
    https://github.com/jmschrei/pomegranate/blob/master/examples/hmm_rainy_sunny.ipynb
Considered tokens:
    first_name -> person names + particles
    last_names -> family names + particles
    particles -> DE, DEL, LO, LOS, LA, DO, DU, Y
    separator -> [ -,]+
    Dot (.) as abbreviation is considered part of the name.
"""

from pomegranate import *
import re
import math


def discrete_distributions():
    first_name_file = './data/raw_first_name.txt'
    last_name_1_file = './data/raw_last_name_1.txt'
    last_name_2_file = './data/raw_last_name_2.txt'
    first_name_dist = {}
    last_name_1_dist = {}
    last_name_2_dist = {}
    pattern = '[^-, ]+'

    # Calculate probabilities for first name
    token_count = 0
    for line in open(first_name_file):
        line = line.strip('\n').strip()
        # List of tokens from each line
        tokens = re.findall(pattern, line)
        # Add tokens to dictionary
        for token in tokens:
            token_count += 1
            if token not in first_name_dist:
                first_name_dist[token] = 1
            else:
                first_name_dist[token] += 1
    # Add tokens from other data files
    for line in open(last_name_1_file):
        line = line.strip('\n').strip()
        tokens = re.findall(pattern, line)
        for token in tokens:
            if token not in first_name_dist:
                first_name_dist[token] = 0
    for line in open(last_name_2_file):
        line = line.strip('\n').strip()
        tokens = re.findall(pattern, line)
        for token in tokens:
            if token not in first_name_dist:
                first_name_dist[token] = 0
    # Calculate probabilities
    for key, value in first_name_dist.iteritems():
        first_name_dist[key] = float(value) / float(token_count)

    # Calculate probabilities for last name 1
    token_count = 0
    for line in open(last_name_1_file):
        line = line.strip('\n').strip()
        # List of tokens from each line
        tokens = re.findall(pattern, line)
        # Add tokens to dictionary
        for token in tokens:
            token_count += 1
            if token not in last_name_1_dist:
                last_name_1_dist[token] = 1
            else:
                last_name_1_dist[token] += 1
    # Add tokens from other data files
    for line in open(first_name_file):
        line = line.strip('\n').strip()
        tokens = re.findall(pattern, line)
        for token in tokens:
            if token not in last_name_1_dist:
                last_name_1_dist[token] = 0
    for line in open(last_name_2_file):
        line = line.strip('\n').strip()
        tokens = re.findall(pattern, line)
        for token in tokens:
            if token not in last_name_1_dist:
                last_name_1_dist[token] = 0
    # Calculate probabilities
    for key, value in last_name_1_dist.iteritems():
        last_name_1_dist[key] = float(value) / float(token_count)

    # Calculate probabilities for last name 2
    token_count = 0
    for line in open(last_name_2_file):
        line = line.strip('\n').strip()
        # List of tokens from each line
        tokens = re.findall(pattern, line)
        # Add tokens to dictionary
        for token in tokens:
            token_count += 1
            if token not in last_name_2_dist:
                last_name_2_dist[token] = 1
            else:
                last_name_2_dist[token] += 1
    # Add tokens from other data files
    for line in open(first_name_file):
        line = line.strip('\n').strip()
        tokens = re.findall(pattern, line)
        for token in tokens:
            if token not in last_name_2_dist:
                last_name_2_dist[token] = 0
    for line in open(last_name_1_file):
        line = line.strip('\n').strip()
        tokens = re.findall(pattern, line)
        for token in tokens:
            if token not in last_name_2_dist:
                last_name_2_dist[token] = 0
    # Calculate probabilities
    for key, value in last_name_2_dist.iteritems():
        last_name_2_dist[key] = float(value) / float(token_count)

    # Order dictionaries by key
    return first_name_dist, last_name_1_dist, last_name_2_dist


# Create dictionaries of pairs token-probability from raw data
# These dictionaries define the distribution of probability for each token
first_name_dist, last_name_1_dist, last_name_2_dist = discrete_distributions()

# Name of the model
model = HiddenMarkovModel(name="First-Last-Names")

# States of the model
first_name = State(DiscreteDistribution(first_name_dist), name='First Name')
last_name_1 = State(DiscreteDistribution(last_name_1_dist), name='Last Name 1')
last_name_2 = State(DiscreteDistribution(last_name_2_dist), name='Last Name 2')

# Transition probabilities
# Obtained from a huge dataset of names
model.add_transition(model.start, first_name, 1)
model.add_transition(first_name, first_name, 0.349495808)
model.add_transition(first_name, last_name_1, 0.650504192)
model.add_transition(last_name_1, last_name_1, 0.02401917)
model.add_transition(last_name_1, last_name_2, 0.942227494)
model.add_transition(last_name_1, model.end, 0.033753336)
model.add_transition(last_name_2, last_name_2, 0.055919604)
model.add_transition(last_name_2, model.end, 0.944080396)

# "Bake" the model, finalizing its structure
model.bake(verbose=True)

# Test
observation = 'ALBERTO ALEJO DE LA CORTE WILSON'
sequence = observation.split()

# Probability of this sequence
print('Observation: ' + observation)
print('P(sequence) = ' + str(
    math.e**model.forward(sequence)[len(sequence), model.end_index]))

# Probability of token 2 = last_name_1
print(
    math.e**model.forward_backward(sequence)
    [1][2, model.states.index(last_name_1)]
)
# Probability of token 2 = last_name_2
print(
    math.e**model.forward_backward(sequence)
    [1][2, model.states.index(last_name_2)]
)
# Probability of token 0 = first_name
print(
    math.e**model.forward_backward(sequence)
    [1][0, model.states.index(first_name)]
)
# Probability of the sequence given it is first_name at token 1
print(math.e**model.backward(sequence)[1, model.states.index(first_name)])
# Probable series of states given the above sequence
print(' '.join(state.name for i, state in model.maximum_a_posteriori(
    sequence)[1]))
