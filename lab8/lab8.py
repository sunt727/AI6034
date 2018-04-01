# MIT 6.034 Lab 8: Bayesian Inference
# Written by 6.034 staff

from nets import *


#### Part 1: Warm-up; Ancestors, Descendents, and Non-descendents ##############

def get_ancestors(net, var):
	"Return a set containing the ancestors of var"
	parents = net.get_parents(var)
	for parent in parents:
		parents = set(list(parents) + list(get_ancestors(net, parent)))
	return parents

def get_descendants(net, var):
	"Returns a set containing the descendants of var"
	children = net.get_children(var)
	for child in children:
		children = set(list(children) + list(get_descendants(net, child)))
	return children

def get_nondescendants(net, var):
	"Returns a set containing the non-descendants of var"
	return {x for x in net.get_variables() if x not in get_descendants(net, var) and x != var}


#### Part 2: Computing Probability #############################################

def simplify_givens(net, var, givens):
	"""
	If givens include every parent of var and no descendants, returns a
	simplified list of givens, keeping only parents.  Does not modify original
	givens.  Otherwise, if not all parents are given, or if a descendant is
	given, returns original givens.
	"""
	return {g: givens[g] for g in net.get_parents(var)} \
		if net.get_parents(var).issubset(givens.keys()) and \
		   set(givens.keys()).issubset(get_nondescendants(net, var)) else givens

def probability_lookup(net, hypothesis, givens=None):
	"Looks up a probability in the Bayes net, or raises LookupError"
	try:
		return net.get_probability(hypothesis, givens)
	except ValueError:
		try:
			return net.get_probability(hypothesis, simplify_givens(net, list(hypothesis.keys())[0], givens))
		except ValueError:
			raise LookupError

def probability_joint(net, hypothesis):
	"Uses the chain rule to compute a joint probability"
	return product([net.get_probability({h: hypothesis[h]},
                    {parent: hypothesis[parent] for parent in net.get_parents(h)})
	                for h in hypothesis.keys()])

def probability_marginal(net, hypothesis):
	"Computes a marginal probability as a sum of joint probabilities"
	marginals = [m for m in net.get_variables() if m not in hypothesis.keys()]
	return sum([probability_joint(net, dict(hypothesis, **vars)) for vars in net.combinations(marginals)])

def probability_conditional(net, hypothesis, givens=None):
	"Computes a conditional probability as a ratio of marginal probabilities"
	if givens is None:
		return probability_joint(net, hypothesis) if sorted(hypothesis.keys()) == sorted(net.get_variables()) \
			else probability_marginal(net, hypothesis)
	elif not all(hypothesis[h] == givens.get(h, hypothesis[h]) for h in hypothesis.keys()) is True:
		return 0
	else:
		return probability_marginal(net, dict(hypothesis, **givens)) / probability_marginal(net, givens)

def probability(net, hypothesis, givens=None):
	"Calls previous functions to compute any probability"
	return probability_conditional(net, hypothesis, givens)


#### Part 3: Counting Parameters ###############################################

def number_of_parameters(net):
	"""
	Computes the minimum number of parameters required for the Bayes net.
	"""
	params = []
	for var in net.get_variables():
		table = [len(net.get_domain(var))-1]
		for parent in net.get_parents(var):
			table.append(len(net.get_domain(parent)))
		params.append(product(table))
	return sum(params)


#### Part 4: Independence ######################################################

def is_independent(net, var1, var2, givens=None):
	"""
	Return True if var1, var2 are conditionally independent given givens,
	otherwise False. Uses numerical independence.
	"""
	if givens is None:
		return all(approx_equal(probability(net, hypothesis1, hypothesis2),
		                        probability(net, hypothesis1)) for hypothesis1 in net.combinations(var1) for
		           hypothesis2 in net.combinations(var2)) is True
	else:
		return all(approx_equal(probability(net, hypothesis1, dict(hypothesis2, **givens)),
		                        probability(net, hypothesis1, givens)) for hypothesis1 in net.combinations(var1) for
		           hypothesis2 in net.combinations(var2)) is True

def is_structurally_independent(net, var1, var2, givens=None):
	"""
	Return True if var1, var2 are conditionally independent given givens,
	based on the structure of the Bayes net, otherwise False.
	Uses structural independence only (not numerical independence).
	"""
	if var1 == var2:
		return False
	considervar = {var1, var2}
	if givens is not None:
		considervar = considervar.union(givens)
	for var in considervar:
		considervar = considervar.union(get_ancestors(net, var))
	newnet = net.subnet(considervar)  # 1. Draw the ancestral graph
	vars = newnet.get_variables()
	for var in vars:
		parents = net.get_parents(var)
		for x in parents:
			for y in parents:
				if x != y:
					newnet = newnet.link(x, y)  # 2. “Moralize” the ancestral graph by “marrying” the parents.
	# 3. "Disorient" the graph by replacing the directed edges (arrows) with undirected edges (lines).
	newnet.make_bidirectional()
	if givens is not None:
		for var in givens.keys():  # 4. Delete the givens and their edges.
			newnet.remove_variable(var)
	return newnet.find_path(var1, var2) is None

#### SURVEY ####################################################################

NAME = 'Tuo Sun'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = 4.5
WHAT_I_FOUND_INTERESTING = 'the flow chart!'
WHAT_I_FOUND_BORING = 'None'
SUGGESTIONS = None
