"""
Hidden Markov Model to parse first names and last names from unstructured text.

Pomegranate documentation:
    https://pomegranate.readthedocs.io/
Code example:
    https://github.com/jmschrei/pomegranate/blob/master/examples/hmm_rainy_sunny.ipynb
States:
    FN -> first name
    PFN -> particle of first name
    LN1 -> last name 1
    PLN1 -> particle of last name 1
    LN2 -> last name 2
    PLN2 -> particle of last name 2
Tokens:
    - last 4 characters of first name or last name (1 and 2)
    - particles = '( da | de | de la | de las | de los | del | di | dl |
                     do | dos | el | ep | i | la | las | los | le | san | van )'

"""

from pomegranate import HiddenMarkovModel, DiscreteDistribution, State
import re
import math
import config
import tokenizer


def extract_tokens(file_name):
    """
    Extract all tokens found in a raw data file.

    Parameters:
        file_name (str): path of the file containing raw data
        pattern (str): regular expression used to identify separators
    Returns:
        tokens (list)

    """
    name_tokens = []
    particle_tokens = []
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
    return name_tokens, particle_tokens


def probability_distribution(subtokens):
    """
    Calculate the probabilities for each token in a given list.

    Parameters:
        subtokens (list): list containing subtokens

    Returns:
        prob_dist (dict): dictionary of subtoken-probability pairs

    """
    subtoken_count = 0
    prob_dist = {}
    # Frequency of each token
    for subtoken in subtokens:
        subtoken_count += 1
        if subtoken not in prob_dist:
            prob_dist[subtoken] = 1
        else:
            prob_dist[subtoken] += 1
    # Calculate probabilities
    for key, value in prob_dist.items():
        prob_dist[key] = float(value) / float(subtoken_count)
    return prob_dist


def discrete_distribution(
        prob_dist, subtokens1, subtokens2, subtokens3, subtokens4, subtokens5):
    """
    Add subtokens from other states to a given probability distribution.

    Added subtokens have probability = 0.

    Parameters:
        prob_dist (dict): probability distribution of a given state
        subtokens1..subtokens5 (list): subtokens of another states

    Returns:
        prob_dist (dict): input probability distribution + added subtokens

    """
    # Join (union) subtokens1 to subtokens5, without repetition
    subtokens = set(subtokens1) | set(subtokens2) | set(subtokens3) |\
        set(subtokens4) | set(subtokens5)
    subtokens = set(subtokens)
    # Add tokens to prob_dist with probability = 0
    for subtoken in subtokens:
        if subtoken not in prob_dist:
            prob_dist[subtoken] = float(0)
    return prob_dist


def main():
    """Create a Hidden Markov Model."""
    # Name of the model
    model = HiddenMarkovModel(name="First-Last-Names")

    # Extract tokens from the training sets
    fn_tokens, pfn_tokens = extract_tokens(config.fn_file)
    ln1_tokens, pln1_tokens = extract_tokens(config.ln1_file)
    ln2_tokens, pln2_tokens = extract_tokens(config.ln2_file)

    # Calculate probability distributions for each token set
    fn_dist = probability_distribution(fn_tokens)
    pfn_dist = probability_distribution(pfn_tokens)
    ln1_dist = probability_distribution(ln1_tokens)
    pln1_dist = probability_distribution(pln1_tokens)
    ln2_dist = probability_distribution(ln2_tokens)
    pln2_dist = probability_distribution(pln2_tokens)

    # Calculate discrete distributions
    fn_dist = discrete_distribution(
        fn_dist, pfn_tokens, ln1_tokens, pln1_tokens, ln2_tokens, pln2_tokens
        )
    pfn_dist = discrete_distribution(
        pfn_dist, fn_tokens, ln1_tokens, pln1_tokens, ln2_tokens, pln2_tokens
        )
    ln1_dist = discrete_distribution(
        ln1_dist, fn_tokens, pfn_tokens, pln1_tokens, ln2_tokens, pln2_tokens
        )
    pln1_dist = discrete_distribution(
        pln1_dist, fn_tokens, pfn_tokens, ln1_tokens, ln2_tokens, pln2_tokens
        )
    ln2_dist = discrete_distribution(
        ln2_dist, fn_tokens, pfn_tokens, ln1_tokens, pln1_tokens, pln2_tokens
        )
    pln2_dist = discrete_distribution(
        pln2_dist, fn_tokens, pfn_tokens, ln1_tokens, pln1_tokens, ln2_tokens
        )

    # States of the model
    fn = State(DiscreteDistribution(
        fn_dist), name='FirstName'
        )
    pfn = State(DiscreteDistribution(
        pfn_dist), name='ParticleFirstName'
        )
    ln1 = State(DiscreteDistribution(
        ln1_dist), name='LastName1'
        )
    pln1 = State(DiscreteDistribution(
        pln1_dist), name='ParticleLastName1'
        )
    ln2 = State(DiscreteDistribution(
        ln2_dist), name='LastName2'
        )
    pln2 = State(DiscreteDistribution(
        pln2_dist), name='ParticleLastName2'
        )

    # Transition probabilities
    # Obtained from a huge dataset of names
    if config.graph_type == config.graph_types[0]:
        # Graph for FirstName LastName1 LastName2 sequences
        model.add_transition(model.start, fn, 1)
        model.add_transition(fn, fn, 0.334)
        model.add_transition(fn, pfn, 0.010)
        model.add_transition(fn, ln1, 0.648)
        model.add_transition(fn, pln1, 0.008)
        model.add_transition(pfn, fn, 1)
        model.add_transition(ln1, ln1, 0.010)
        model.add_transition(ln1, pln1, 0.010)
        model.add_transition(ln1, ln2, 0.945)
        model.add_transition(ln1, pln2, 0.001)
        model.add_transition(ln1, model.end, 0.034)
        model.add_transition(pln1, ln1, 1)
        model.add_transition(ln2, ln2, 0.004)
        model.add_transition(ln2, pln2, 0.004)
        model.add_transition(ln2, model.end, 0.992)
        model.add_transition(pln2, ln2, 1)
    else:
        # Graph for LastName1 LastName2 FirstName sequences
        model.add_transition(model.start, ln1, 0.990)
        model.add_transition(model.start, pln1, 0.010)
        model.add_transition(ln1, ln1, 0.010)
        model.add_transition(ln1, pln1, 0.010)
        model.add_transition(ln1, ln2, 0.945)
        model.add_transition(ln1, pln2, 0.001)
        model.add_transition(ln1, fn, 0.034)
        model.add_transition(pln1, ln1, 1)
        model.add_transition(ln2, ln2, 0.004)
        model.add_transition(ln2, pln2, 0.004)
        model.add_transition(ln2, fn, 0.992)
        model.add_transition(pln2, ln2, 1)
        model.add_transition(fn, fn, 0.334)
        model.add_transition(fn, pfn, 0.010)
        model.add_transition(fn, model.end, 0.656)
        model.add_transition(pfn, fn, 1)

    # "Bake" the model, finalizing its structure
    model.bake(verbose=True)

    # Testing the model
    for line in open(config.test_set_file):
        observation = line.strip('\n')
        norm_observation = tokenizer.unicode(observation)
        sequence = tokenizer.split_sequence(
            norm_observation.lower(), config.token_pattern)
        sequence = tokenizer.subtokens(
            sequence, config.subtoken_length, config.particles)
        # Probability of this sequence
        print(observation)
        print(sequence)
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
