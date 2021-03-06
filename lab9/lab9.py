# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by 6.034 staff

from math import log as ln
from utils import *


#### Part 1: Helper functions ##################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    d = {}
    for pt in training_points:
        d[pt] = make_fraction(1,len(training_points))
    return d

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    d = {}
    for classifier in classifier_to_misclassified.keys():
        epsilon = sum([point_to_weight[pt] for pt in classifier_to_misclassified[classifier]])
        d[classifier] = epsilon
    return d

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    if use_smallest_error:
        best = min(sorted(classifier_to_error_rate.keys()), key = lambda x: classifier_to_error_rate[x])
    else:
        best = max(sorted(classifier_to_error_rate.keys()), \
                   key = lambda x: abs(classifier_to_error_rate[x] - make_fraction(1,2)))
    if classifier_to_error_rate[best] == 0.5:
        raise NoGoodClassifiersError
    else:
        return best

def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 0:
        return INF
    elif error_rate == 1:
        return -INF
    else:
        return 1/2 * ln((1-error_rate)/error_rate)


def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
	"""Given an overall classifier H, a list of all training points, and a
	dictionary mapping classifiers to the training points they misclassify,
	returns a set containing the training points that H misclassifies.
	H is represented as a list of (classifier, voting_power) tuples."""
	l = []
	for pt in training_points:
		num = 0
		for h in H:
			if pt in classifier_to_misclassified[h[0]]:
				num -= h[1]
			else:
				num += h[1]
		if num <= 0:
			l.append(pt)
	return set(l)


def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
	"""Given an overall classifier H, a list of all training points, a
	dictionary mapping classifiers to the training points they misclassify, and
	a mistake tolerance (the maximum number of allowed misclassifications),
	returns False if H misclassifies more points than the tolerance allows,
	otherwise True.  H is represented as a list of (classifier, voting_power)
	tuples."""
	miss = get_overall_misclassifications(H, training_points, classifier_to_misclassified)
	return True if len(miss) <= mistake_tolerance else False

def update_weights(point_to_weight, misclassified_points, error_rate):
	"""Given a dictionary mapping training points to their old weights, a list
	of training points misclassified by the current weak classifier, and the
	error rate of the current weak classifier, returns a dictionary mapping
	training points to their new weights.  This function is allowed (but not
	required) to modify the input dictionary point_to_weight."""
	d = {}
	for pt in point_to_weight.keys():
		if pt in misclassified_points:
			new = make_fraction(1, 2 * error_rate) * point_to_weight[pt]
		else:
			new = make_fraction(1, 2 * (1-error_rate)) * point_to_weight[pt]
		d[pt] = new
	return d


#### Part 2: Adaboost ##########################################################

def adaboost(training_points, classifier_to_misclassified,
			 use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
	"""Performs the Adaboost algorithm for up to max_rounds rounds.
	Returns the resulting overall classifier H, represented as a list of
	(classifier, voting_power) tuples."""
	point_to_weight = initialize_weights(training_points)
	H = []
	rounds = 0
	while True:
		rounds += 1
		classifier_to_error_rate = calculate_error_rates(point_to_weight, classifier_to_misclassified)
		try:
			best_classifier = pick_best_classifier(classifier_to_error_rate, use_smallest_error)
		except NoGoodClassifiersError:
			break
		H.append((best_classifier, calculate_voting_power(classifier_to_error_rate[best_classifier])))
		if rounds >= max_rounds:
			break
		if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
			break
		point_to_weight = update_weights(point_to_weight, classifier_to_misclassified[best_classifier],
										 classifier_to_error_rate[best_classifier])

	return H


#### SURVEY ####################################################################

NAME = 'Tuo Sun'
COLLABORATORS = 'Sen Dai'
HOW_MANY_HOURS_THIS_LAB_TOOK = 4
WHAT_I_FOUND_INTERESTING = 'None'
WHAT_I_FOUND_BORING = 'None'
SUGGESTIONS = None
