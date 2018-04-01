# MIT 6.034 Lab 7: Support Vector Machines
# Written by 6.034 staff

from svm_data import *
from functools import reduce


#### Part 1: Vector Math #######################################################

def dot_product(u, v):
	"""Computes the dot product of two vectors u and v, each represented
	as a tuple or list of coordinates. Assume the two vectors are the
	same length."""
	return sum(u[i] * v[i] for i in range(len(u)))

def norm(v):
	"""Computes the norm (length) of a vector v, represented
	as a tuple or list of coords."""
	return pow(sum(i*i for i in v), 0.5)


#### Part 2: Using the SVM Boundary Equations ##################################

def positiveness(svm, point):
	"""Computes the expression (w dot x + b) for the given Point x."""
	return dot_product(svm.w, point.coords) + svm.b

def classify(svm, point):
	"""Uses the given SVM to classify a Point. Assume that the point's true
	classification is unknown.
	Returns +1 or -1, or 0 if point is on boundary."""
	y = positiveness(svm, point)
	return 0 if y == 0 else +1 if y > 0 else -1

def margin_width(svm):
	"""Calculate margin width based on the current boundary."""
	return 2/norm(svm.w)

def check_gutter_constraint(svm):
	"""Returns the set of training points that violate one or both conditions:
		* gutter constraint (positiveness == classification, for support vectors)
		* training points must not be between the gutters
	Assumes that the SVM has support vectors assigned."""
	return set([sv for sv in svm.support_vectors if positiveness(svm, sv) != sv.classification]
	           + [tp for tp in svm.training_points if +1 > positiveness(svm, tp) > -1])


#### Part 3: Supportiveness ####################################################

def check_alpha_signs(svm):
	"""Returns the set of training points that violate either condition:
		* all non-support-vector training points have alpha = 0
		* all support vectors have alpha > 0
	Assumes that the SVM has support vectors assigned, and that all training
	points have alpha values assigned."""
	return set([tp for tp in svm.training_points if (tp in svm.support_vectors and tp.alpha <= 0)
	            or (tp not in svm.support_vectors and tp.alpha != 0)])

def vecsum(vecs):
	if len(vecs) > 2:
		return vector_add(vecs[0], vecsum(vecs[1:]))
	elif len(vecs) == 2:
		return vector_add(vecs[0], vecs[1])
	elif len(vecs) == 1:
		return vecs[0]

def check_alpha_equations(svm):
	"""Returns True if both Lagrange-multiplier equations are satisfied,
	otherwise False. Assumes that the SVM has support vectors assigned, and
	that all training points have alpha values assigned."""

	return sum(pt.alpha * pt.classification for pt in svm.training_points) == 0 \
	       and vecsum([scalar_mult(pt.alpha * pt.classification, pt) for pt in svm.training_points]) == svm.w


#### Part 4: Evaluating Accuracy ###############################################

def misclassified_training_points(svm):
	"""Returns the set of training points that are classified incorrectly
	using the current decision boundary."""
	return set([pt for pt in svm.training_points if classify(svm, pt) != pt.classification])


#### Part 5: Training an SVM ###################################################

def update_svm_from_alphas(svm):
	"""Given an SVM with training data and alpha values, use alpha values to
	update the SVM's support vectors, w, and b. Return the updated SVM."""
	svm.support_vectors = [pt for pt in svm.training_points if pt.alpha > 0]
	new_w = vecsum([scalar_mult(pt.alpha * pt.classification, pt) for pt in svm.training_points])
	min_pts = [pt.classification - dot_product(new_w, pt.coords) for pt in svm.support_vectors if pt.classification < 0]
	max_pts = [pt.classification - dot_product(new_w, pt.coords) for pt in svm.support_vectors if pt.classification > 0]
	new_b = (min(min_pts) + max(max_pts))/2
	svm.set_boundary(new_w, new_b)
	return svm

#### Part 6: Multiple Choice ###################################################

ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ['A', 'D']
ANSWER_6 = ['A', 'B', 'D']
ANSWER_7 = ['A', 'B', 'D']
ANSWER_8 = []
ANSWER_9 = ['A', 'B', 'D']
ANSWER_10 = ['A', 'B', 'D']

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1, 3, 6, 8]
ANSWER_18 = [1, 2, 4, 5, 6, 7, 8]
ANSWER_19 = [1, 2, 4, 5, 6, 7, 8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = 'Tuo Sun'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = 3
WHAT_I_FOUND_INTERESTING = 'Observing the graphic process of training'
WHAT_I_FOUND_BORING = 'None'
SUGGESTIONS = None
