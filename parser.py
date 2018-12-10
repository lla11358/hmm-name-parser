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

import math
import re
from pomegranate import HiddenMarkovModel, DiscreteDistribution, State
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
    if config.graph_type == config.graph_types[0]:
        # Graph for FirstName LastName1 LastName2 sequences
        model.add_transition(model.start, fn, 1)
        model.add_transition(fn, fn, 0.256251576)
        model.add_transition(fn, pfn, 0.028472397)
        model.add_transition(fn, ln1, 0.704144114)
        model.add_transition(fn, pln1, 0.011131913)
        model.add_transition(pfn, pfn, 0.150)
        model.add_transition(pfn, fn, 0.850)
        model.add_transition(ln1, ln1, 0.007015434)
        model.add_transition(ln1, pln1, 0.007017087)
        model.add_transition(ln1, ln2, 0.960638112)
        model.add_transition(ln1, pln2, 0.014719859)
        model.add_transition(ln1, model.end, 0.010609508)
        model.add_transition(pln1, pln1, 0.150)
        model.add_transition(pln1, ln1, 0.850)
        model.add_transition(ln2, ln2, 0.004290151)
        model.add_transition(ln2, pln2, 0.006801967)
        model.add_transition(ln2, model.end, 0.988907882)
        model.add_transition(pln2, pln2, 0.150)
        model.add_transition(pln2, ln2, 0.850)
    else:
        # Graph for LastName1 LastName2 FirstName sequences
        model.add_transition(model.start, ln1, 0.984436899)
        model.add_transition(model.start, pln1, 0.015563101)
        model.add_transition(ln1, ln1, 0.007015434)
        model.add_transition(ln1, pln1, 0.007017087)
        model.add_transition(ln1, ln2, 0.960638112)
        model.add_transition(ln1, pln2, 0.014719859)
        model.add_transition(ln1, fn, 0.010609508)
        model.add_transition(pln1, pln1, 0.150)
        model.add_transition(pln1, ln1, 0.850)
        model.add_transition(ln2, ln2, 0.004290151)
        model.add_transition(ln2, pln2, 0.006801967)
        model.add_transition(ln2, fn, 0.988907882)
        model.add_transition(pln2, pln2, 0.150)
        model.add_transition(pln2, ln2, 0.850)
        model.add_transition(fn, fn, 0.256251576)
        model.add_transition(fn, pfn, 0.028472397)
        model.add_transition(fn, model.end, 0.715276027)
        model.add_transition(pfn, pfn, 0.150)
        model.add_transition(pfn, fn, 0.850)

    # "Bake" the model, finalizing its structure
    model.bake(verbose=True)

    # Testing the model
    parse_errors = 0
    value_errors = 0
    tagged_names = utils.load_dict_from_file(config.test_set_file)
    for key, value in tagged_names.items():
        print('Observation: ' + value['observation'])
        norm_observation = utils.normalize(
            value['observation'], config.text_case
        )
        words = re.findall(config.word_pattern, norm_observation)
        token_sequence = []
        for word in words:
            token_sequence.append(utils.to_token(word, config.token_length))

        test_dict = {
            'FirstName': '',
            'LastName1': '',
            'LastName2': '',
        }
        try:
            j = 0
            for i, state in model.maximum_a_posteriori(token_sequence)[1]:
                if state.name[-4:] == 'Name':
                    test_dict['FirstName'] += words[j] + ' '
                if state.name[-5:] == 'Name1':
                    test_dict['LastName1'] += words[j] + ' '
                if state.name[-5:] == 'Name2':
                    test_dict['LastName2'] += words[j] + ' '
                j += 1

            # compare results with tagged names
            test_dict['FirstName'] = test_dict['FirstName'].rstrip()
            test_dict['LastName1'] = test_dict['LastName1'].rstrip()
            test_dict['LastName2'] = test_dict['LastName2'].rstrip()
            print('Parsed: ' + str(test_dict))

            # Probability of this sequence
            print('P(sequence) = ' + str(math.e**model.forward(
                    token_sequence)[len(token_sequence), model.end_index]))

            result = ''
            for state in ['FirstName', 'LastName1', 'LastName2']:
                if test_dict[state] == value[state]:
                    result += ''
                else:
                    result += state + ' differs. '
            if result == '':
                result = 'Correct.'
            else:
                parse_errors += 1
            print('Result: ' + result)
        except ValueError as ve:
            print(ve)
            value_errors += 1

        print('--')

    # Final statistics
    print('Summary\n=======')
    print('Number of observations: ' + str(len(tagged_names)))
    print('Parse errors:' + str(parse_errors))
    print('Value errors: ' + str(value_errors))
    
    """
    # Run the model against a text file
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
            # Probability of the given sequence
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
    """


if __name__ == '__main__':
    main()
