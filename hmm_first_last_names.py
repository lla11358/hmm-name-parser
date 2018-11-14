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

from pomegranate import HiddenMarkovModel, DiscreteDistribution, State
import re
import math

# Pattern defining the token separators
separators = '[^-, ]+'
# Raw data files
first_name_file = './data/raw_first_name.txt'
last_name_1_file = './data/raw_last_name_1.txt'
last_name_2_file = './data/raw_last_name_2.txt'
test_set_file = './data/test_set.txt'


def extract_tokens(file_name, pattern):
    """
    Extract all tokens found in a raw data file.

    Parameters:
        file_name (str): path of the file containing raw data
        pattern (str): regular expression used to identify separators
    Returns:
        tokens (list)

    """
    tokens = []
    for line in open(file_name):
        line = line.strip('\n').strip()
        # List of tokens from each line
        line_tokens = re.findall(pattern, line)
        for line_token in line_tokens:
            tokens.append(line_token)
    return tokens


def probability_distribution(tokens):
    """
    Calculate the probabilities for each token in a given list.

    Parameters:
        tokens (list): list containing tokens

    Returns:
        prob_dist (dict): dictionary of token-probability pairs

    """
    token_count = 0
    prob_dist = {}
    # Frequencies of each token
    for token in tokens:
        token_count += 1
        if token not in prob_dist:
            prob_dist[token] = 1
        else:
            prob_dist[token] += 1
    # Calculate probabilities
    for key, value in prob_dist.iteritems():
        prob_dist[key] = float(value) / float(token_count)
    return prob_dist


def discrete_distribution(prob_dist, tokens_1, tokens_2):
    """
    Add tokens from other states to a given probability distribution.

    Added tokens have probability = 0.

    Parameters:
        prob_dist (dict): probability distribution of a given state
        tokens_1 (list): tokens of another state
        tokens_2 (list): tokens of another state
    Returns:
        prob_dist (dict): input probability distribution + added tokens

    """
    # Join (union) tokens_1 and tokens_2, without repetition
    tokens = set(tokens_1) | set(tokens_2)
    tokens = set(tokens)
    # Add tokens to prob_dist with probability = 0
    for token in tokens:
        if token not in prob_dist:
            prob_dist[token] = float(0)
    return prob_dist


def main():
    """Create a Hidden Markov Model."""
    # Name of the model
    model = HiddenMarkovModel(name="First-Last-Names")

    # Extract tokens from the training sets
    first_name_tokens = extract_tokens(first_name_file, separators)
    last_name_1_tokens = extract_tokens(last_name_1_file, separators)
    last_name_2_tokens = extract_tokens(last_name_2_file, separators)

    # Calculate probability distributions for each token set
    first_name_dist = probability_distribution(first_name_tokens)
    last_name_1_dist = probability_distribution(last_name_1_tokens)
    last_name_2_dist = probability_distribution(last_name_2_tokens)

    # Calculate discrete distributions
    first_name_dist = discrete_distribution(
        first_name_dist, last_name_1_tokens, last_name_2_tokens
        )
    last_name_1_dist = discrete_distribution(
        last_name_1_dist, first_name_tokens, last_name_2_tokens
        )
    last_name_2_dist = discrete_distribution(
        last_name_2_dist, first_name_tokens, last_name_1_tokens
        )

    # Debugging
    """
    print(len(first_name_dist))
    print(len(last_name_1_dist))
    print(len(last_name_2_dist))
    """

    # States of the model
    first_name = State(DiscreteDistribution(
        first_name_dist), name='FirstName'
        )
    last_name_1 = State(DiscreteDistribution(
        last_name_1_dist), name='LastName1'
        )
    last_name_2 = State(DiscreteDistribution(
        last_name_2_dist), name='LastName2'
        )

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

    # Testing the model
    for line in open(test_set_file):
        observation = line.strip('\n')
        sequence = observation.split()

        # Probability of this sequence
        print('Observation: ' + observation)
        try:
            print('P(sequence) = ' + str(math.e**model.forward(
                    sequence)[len(sequence), model.end_index]))
            # Probable series of states given the above sequence
            print(' '.join(
                state.name for i, state in model.maximum_a_posteriori(
                    sequence)[1]))
        except ValueError as ve:
            print(ve)
        finally:
            print('--')


if __name__ == '__main__':
    main()
