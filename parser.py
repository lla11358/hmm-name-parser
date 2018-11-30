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
    - last characters of first name or last name (1 and 2)
    - particles = config.particles

"""

from pomegranate import HiddenMarkovModel, DiscreteDistribution, State
import re
import config
import utils


def discrete_distribution(
        prob_dist, tokens1, tokens2, tokens3, tokens4, tokens5):
    """
    Add tokens from other states to a given probability distribution.

    Added tokens have probability = 0.

    Parameters:
        prob_dist (dict): probability distribution of a given state.
        tokens1..tokens5 (list): tokens of another states,
        without associated probabilities.

    Returns:
        prob_dist (dict): input probability distribution + added tokens.

    """
    # Join (union) tokens1 to tokens5, without repetition
    tokens = set(tokens1) | set(tokens2) | set(tokens3) |\
        set(tokens4) | set(tokens5)
    tokens = set(tokens)
    # Add tokens to prob_dist with probability = 0
    for token in tokens:
        if token not in prob_dist:
            prob_dist[token] = float(0)
    return prob_dist


def main():
    """Create a Hidden Markov Model."""
    # Name of the model
    model = HiddenMarkovModel(name="Names")

    # Load probability distributions for each token set
    fn_dist = utils.load_dict_from_file(
        config.input_dir + config.token_files['first_name']
    )
    pfn_dist = utils.load_dict_from_file(
        config.input_dir + config.token_files['part_first_name']
    )
    ln1_dist = utils.load_dict_from_file(
        config.input_dir + config.token_files['last_name1']
    )
    pln1_dist = utils.load_dict_from_file(
        config.input_dir + config.token_files['part_last_name1']
    )
    ln2_dist = utils.load_dict_from_file(
        config.input_dir + config.token_files['last_name2']
    )
    pln2_dist = utils.load_dict_from_file(
        config.input_dir + config.token_files['part_last_name2']
    )

    # Calculate discrete distributions
    fn_dist = discrete_distribution(
        fn_dist, pfn_dist, ln1_dist, pln1_dist, ln2_dist, pln2_dist
    )
    pfn_dist = discrete_distribution(
        pfn_dist, fn_dist, ln1_dist, pln1_dist, ln2_dist, pln2_dist
        )
    ln1_dist = discrete_distribution(
        ln1_dist, fn_dist, pfn_dist, pln1_dist, ln2_dist, pln2_dist
        )
    pln1_dist = discrete_distribution(
        pln1_dist, fn_dist, pfn_dist, ln1_dist, ln2_dist, pln2_dist
        )
    ln2_dist = discrete_distribution(
        ln2_dist, fn_dist, pfn_dist, ln1_dist, pln1_dist, pln2_dist
        )
    pln2_dist = discrete_distribution(
        pln2_dist, fn_dist, pfn_dist, ln1_dist, pln1_dist, ln2_dist
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
        model.add_transition(pfn, pfn, 0.150)
        model.add_transition(pfn, fn, 0.850)
        model.add_transition(ln1, ln1, 0.010)
        model.add_transition(ln1, pln1, 0.010)
        model.add_transition(ln1, ln2, 0.945)
        model.add_transition(ln1, pln2, 0.001)
        model.add_transition(ln1, model.end, 0.034)
        model.add_transition(pln1, pln1, 0.150)
        model.add_transition(pln1, ln1, 0.850)
        model.add_transition(ln2, ln2, 0.004)
        model.add_transition(ln2, pln2, 0.004)
        model.add_transition(ln2, model.end, 0.992)
        model.add_transition(pln2, pln2, 0.150)
        model.add_transition(pln2, ln2, 0.850)
    else:
        # Graph for LastName1 LastName2 FirstName sequences
        model.add_transition(model.start, ln1, 0.990)
        model.add_transition(model.start, pln1, 0.010)
        model.add_transition(ln1, ln1, 0.010)
        model.add_transition(ln1, pln1, 0.010)
        model.add_transition(ln1, ln2, 0.945)
        model.add_transition(ln1, pln2, 0.001)
        model.add_transition(ln1, fn, 0.034)
        model.add_transition(pln1, pln1, 0.150)
        model.add_transition(pln1, ln1, 0.850)
        model.add_transition(ln2, ln2, 0.004)
        model.add_transition(ln2, pln2, 0.004)
        model.add_transition(ln2, fn, 0.992)
        model.add_transition(pln2, pln2, 0.150)
        model.add_transition(pln2, ln2, 0.850)
        model.add_transition(fn, fn, 0.334)
        model.add_transition(fn, pfn, 0.010)
        model.add_transition(fn, model.end, 0.656)
        model.add_transition(pfn, pfn, 0.150)
        model.add_transition(pfn, fn, 0.850)

    # "Bake" the model, finalizing its structure
    model.bake(verbose=True)

    # Testing the model
    for line in open(config.test_set_file):
        observation = line.strip('\n')
        norm_observation = utils.normalize(observation, config.text_case)
        words = re.findall(config.word_pattern, norm_observation)
        sequence = []
        for word in words:
            sequence.append(utils.to_token(word, config.token_length))
        # Probability of this sequence
        print(observation)
        # print(sequence)
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
