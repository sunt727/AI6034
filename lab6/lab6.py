# MIT 6.034 Lab 6: Neural Nets
# Written by 6.034 Staff

from nn_problems import *
from math import e

INF = float('inf')

#### Part 1: Wiring a Neural Net ###############################################

nn_half = [1]

nn_angle = [2, 1]

nn_cross = [2, 2, 1]

nn_stripe = [3, 1]

nn_hexagon = [6, 1]

nn_grid = [4, 2, 1]


#### Part 2: Coding Warmup #####################################################

# Threshold functions
def stairstep(x, threshold=0):
	"Computes stairstep(x) using the given threshold (T)"
	return 1 if x >= threshold else 0


def sigmoid(x, steepness=1, midpoint=0):
	"Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
	return pow((1 + pow(e, ((-steepness) * (x - midpoint)))), -1)


def ReLU(x):
	"Computes the threshold of an input using a rectified linear unit."
	return max(0, x)


# Accuracy function
def accuracy(desired_output, actual_output):
	"Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
	return (-0.5) * pow((desired_output - actual_output), 2)


#### Part 3: Forward Propagation ###############################################

def node_value(node, input_values, neuron_outputs):  # PROVIDED BY THE STAFF
	"""
	Given
	 * a node (as an input or as a neuron),
	 * a dictionary mapping input names to their values, and
	 * a dictionary mapping neuron names to their outputs
	returns the output value of the node.
	This function does NOT do any computation; it simply looks up
	values in the provided dictionaries.
	"""
	if isinstance(node, str):
		# A string node (either an input or a neuron)
		if node in input_values:
			return input_values[node]
		if node in neuron_outputs:
			return neuron_outputs[node]
		raise KeyError("Node '{}' not found in either the input values or neuron outputs dictionary.".format(node))

	if isinstance(node, (int, float)):
		# A constant input, such as -1
		return node

	raise TypeError("Node argument is {}; should be either a string or a number.".format(node))


def forward_prop(net, input_values, threshold_fn=stairstep):
	"""Given a neural net and dictionary of input values, performs forward
	propagation with the given threshold function to compute binary output.
	This function should not modify the input net.  Returns a tuple containing:
	(1) the final output of the neural net
	(2) a dictionary mapping neurons to their immediate outputs"""
	neuron_dict = {}
	sorted_neurons = net.topological_sort()
	for neuron in sorted_neurons:
		values = 0
		for wire in net.get_wires(endNode=neuron):
			values += node_value(wire.startNode, input_values, neuron_dict) * wire.get_weight()
		neuron_dict[neuron] = threshold_fn(values)
	return neuron_dict[sorted_neurons[-1]], neuron_dict


#### Part 4: Backward Propagation ##############################################

def gradient_ascent_step(func, inputs, step_size):
	"""Given an unknown function of three variables and a list of three values
	representing the current inputs into the function, increments each variable
	by +/- step_size or 0, with the goal of maximizing the function output.
	After trying all possible variable assignments, returns a tuple containing:
	(1) the maximum function output found, and
	(2) the list of inputs that yielded the highest function output."""
	a, b, c = inputs
	steps = (step_size, 0, -step_size)
	func_dict = {(a + opa, b + opb, c + opc): func(a + opa, b + opb, c + opc)
	             for opa in steps for opb in steps for opc in steps}
	an, bn, cn = max(func_dict.keys(), key=lambda x: func_dict[x])
	return func(an, bn, cn), [an, bn, cn]


def get_back_prop_dependencies(net, wire):
	"""Given a wire in a neural network, returns a set of inputs, neurons, and
	Wires whose outputs/values are required to update this wire's weight."""
	updates = []
	wires = [wire]
	while wires:
		new_wire = wires.pop(0)
		updates += [new_wire.startNode, new_wire.endNode, new_wire]
		wires += net.get_wires(startNode=new_wire.endNode)
	return set(updates)


def calculate_deltas(net, desired_output, neuron_outputs):
	"""Given a neural net and a dictionary of neuron outputs from forward-
	propagation, computes the update coefficient (delta_B) for each
	neuron in the net. Uses the sigmoid function to compute neuron output.
	Returns a dictionary mapping neuron names to update coefficient (the
	delta_B values). """

	def delta(neuron):
		out_B = neuron_outputs[neuron]
		if neuron == net.get_output_neuron():
			return out_B * (1 - out_B) * (desired_output - out_B)
		val = 0
		for node_C in net.get_outgoing_neighbors(neuron):
			[wire_BtoC] = net.get_wires(startNode=neuron, endNode=node_C)
			weight_BtoC = wire_BtoC.get_weight()
			val += out_B * (1 - out_B) * weight_BtoC * delta(node_C)
		return val

	return {n: delta(n) for n in neuron_outputs.keys() if n not in net.inputs}


def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
	"""Performs a single step of back-propagation.  Computes delta_B values and
	weight updates for entire neural net, then updates all weights.  Uses the
	sigmoid function to compute neuron output.  Returns the modified neural net,
	with the updated weights."""
	delta_B_dict = calculate_deltas(net, desired_output, neuron_outputs)
	wires = net.get_wires()
	delta_W_dict = {wire: r * node_value(wire.startNode, input_values, neuron_outputs) * delta_B_dict[wire.endNode]
	                   for wire in wires}
	for i in range(len(wires)):
		wire = wires[i]
		wire.set_weight(wire.get_weight() + delta_W_dict[wire])
	return net


def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
	"""Updates weights until accuracy surpasses minimum_accuracy.  Uses the
	sigmoid function to compute neuron output.  Returns a tuple containing:
	(1) the modified neural net, with trained weights
	(2) the number of iterations (that is, the number of weight updates)"""
	iterations = 0
	actual_output, neuron_outputs = forward_prop(net, input_values, threshold_fn=sigmoid)
	while accuracy(desired_output, actual_output) < minimum_accuracy:
		iterations += 1
		update_weights(net, input_values, desired_output, neuron_outputs, r)
		actual_output, neuron_outputs = forward_prop(net, input_values, threshold_fn=sigmoid)
	return net, iterations


#### Part 5: Training a Neural Net #############################################

ANSWER_1 = 18
ANSWER_2 = 36
ANSWER_3 = 9
ANSWER_4 = 189
ANSWER_5 = 53

ANSWER_6 = 1
ANSWER_7 = "checkerboard"
ANSWER_8 = ['small', 'medium', 'large']
ANSWER_9 = 'B'

ANSWER_10 = 'D'
ANSWER_11 = ['A', 'C']
ANSWER_12 = ['A', 'E']

#### SURVEY ####################################################################

NAME = 'Tuo Sun'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = 8
WHAT_I_FOUND_INTERESTING = 'the graphic presentation of neurons'
WHAT_I_FOUND_BORING = 'None'
SUGGESTIONS = None
