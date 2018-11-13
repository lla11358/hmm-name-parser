"""
Hidden Markov Model to parse first names and last names from unstructured text.

Pomegranate documentation:
    https://pomegranate.readthedocs.io/
Code example:
    https://github.com/jmschrei/pomegranate/blob/master/examples/hmm_rainy_sunny.ipynb
Considered tokens:
    first_name -> person names + particles
    last_names -> family names + particles
    particles -> DE, DEL, LO, LOS, LA, DO, DU, -
    separator -> blank
"""

from pomegranate import *
import math

# Name of the model
model = HiddenMarkovModel(name="First-Last-Names")

# States of the model
first_name = State(DiscreteDistribution(
    {'first_name': 0.00, 'last_name': 0.00}), name='First Name')
last_name_1 = State(DiscreteDistribution(
    {'first_name': 0.00, 'last_name': 0.00}), name='Last Name 1')
last_name_2 = State(DiscreteDistribution(
    {'first_name': 0.00, 'last_name': 0.00}), name='Last Name 2')

# Transition probabilities
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
observation = 'Alberto Lezcano Lastra'
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
