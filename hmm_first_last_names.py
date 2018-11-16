"""
Hidden Markov Model to parse first names and last names from unstructured text.

Pomegranate documentation:
    https://pomegranate.readthedocs.io/
Code example:
    https://github.com/jmschrei/pomegranate/blob/master/examples/hmm_rainy_sunny.ipynb
Considered tokens:
    first_name -> person names
    last_names -> family names
    particles -> DA|DE|DE LA|DE LAS|DE LOS|DEL|DI|DL|DO|DOS|EL|
        EP|I|LA|LAS|LOS|LE|SAN|VAN
    separator -> [ ,]+
    Dot (.) as abbreviation is considered part of the name.
"""

from pomegranate import HiddenMarkovModel, DiscreteDistribution, State
import re
import math
import config


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
        # Some cleaning
        line = line.strip('\n')
        line = line.replace(' - ', '-')
        line = line.replace('"', '')
        line = line.replace('\t', ' ').strip()
        # List of tokens from each line
        line_tokens = re.split(pattern, line)
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
    # Frequency of each token
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
    first_name_tokens = extract_tokens(
        config.first_name_file, config.separators)
    last_name_1_tokens = extract_tokens(
        config.last_name_1_file, config.separators)
    last_name_2_tokens = extract_tokens(
        config.last_name_2_file, config.separators)

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

    # TODO: rebuild graphs of states and transitions
    # Transition probabilities
    # Obtained from a huge dataset of names
    if config.graph_type == config.graph_types[0]:
        # Graph for FirstName LastName1 LastName2 sequences
        model.add_transition(model.start, first_name, 1)
        model.add_transition(first_name, first_name, 0.349495808)
        model.add_transition(first_name, last_name_1, 0.650504192)
        model.add_transition(last_name_1, last_name_1, 0.02401917)
        model.add_transition(last_name_1, last_name_2, 0.942227494)
        model.add_transition(last_name_1, model.end, 0.033753336)
        model.add_transition(last_name_2, last_name_2, 0.055919604)
        model.add_transition(last_name_2, model.end, 0.944080396)
    else:
        # Graph for LastName1 LastName2 FirstName sequences
        model.add_transition(model.start, last_name_1, 1)
        model.add_transition(last_name_1, last_name_1, 0.02401917)
        model.add_transition(last_name_1, last_name_2, 0.942227494)
        model.add_transition(last_name_1, first_name, 0.033753336)
        model.add_transition(last_name_2, last_name_2, 0.055919604)
        model.add_transition(last_name_2, first_name, 0.944080396)
        model.add_transition(first_name, first_name, 0.349495808)
        model.add_transition(first_name, model.end, 0.650504192)

    # "Bake" the model, finalizing its structure
    model.bake(verbose=True)

    # Testing the model
    for line in open(config.test_set_file):
        observation = line.strip('\n')
        sequence = observation.split()
        # Probability of this sequence
        print(observation)
        try:
            """
            # Probability of the given sequence
            print('P(sequence) = ' + str(math.e**model.forward(
                    sequence)[len(sequence), model.end_index]))
            """
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
