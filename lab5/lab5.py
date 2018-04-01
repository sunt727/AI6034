# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by 6.034 Staff

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')


################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################


#### Part 1A: Classifying points ###############################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    return id_tree.get_node_classification() if id_tree.is_leaf() else \
        id_tree_classify_point(point, id_tree.apply_classifier(point))


#### Part 1B: Splitting data with a classifier #################################

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    dict = {}
    for point in data:
        if dict.get(classifier.classify(point), None) is None:
            dict[classifier.classify(point)] = [point]
        else:
            points = dict.get(classifier.classify(point), None)
            points.append(point)
            dict[classifier.classify(point)] = points
    return dict


#### Part 1C: Calculating disorder #############################################

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    counts, disorder = [], 0
    dict = split_on_classifier(data, target_classifier)
    for value in list(dict.values()):
        counts.append(len(value))
    for count in counts:
        disorder += (-(count/sum(counts))) * log2((count/sum(counts)))
    return disorder

def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    d_branches = split_on_classifier(data, test_classifier)
    weights, disorders, stump_disorder = [], [], 0
    for branch in list(d_branches.values()):
        weights.append(len(branch))
        disorders.append(branch_disorder(branch, target_classifier))
    for i in range(len(weights)):
        stump_disorder += (weights[i]/sum(weights)) * disorders[i]
    return stump_disorder


## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:
#
# for classifier in tree_classifiers:
#     print(classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type")))


#### Part 1D: Constructing an ID tree ##########################################

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    stump_disorders = []
    for test_classifier in possible_classifiers:
        stump_disorders.append(average_test_disorder(data, test_classifier, target_classifier))
    best_classifier = possible_classifiers[stump_disorders.index(min(stump_disorders))]
    if len(split_on_classifier(data, best_classifier)) <= 1:
        raise NoGoodClassifiersError("message")
    else:
        return best_classifier


# To find the best classifier from 2014 Q2, Part A, uncomment:
#print(find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type")))

def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    if id_tree_node is None:
        id_tree_node = IdentificationTreeNode(target_classifier)
    if branch_disorder(data, target_classifier) > 0:
        try:
            best_classifier = find_best_classifier(data, possible_classifiers, target_classifier)
            d_branches = split_on_classifier(data, best_classifier)
            id_tree_node.set_classifier_and_expand(best_classifier, d_branches.keys())
            for point in d_branches.keys():
                construct_greedy_id_tree(d_branches[point], possible_classifiers, target_classifier, id_tree_node.get_branches()[point])
        except NoGoodClassifiersError:
            pass
    else:
        id_tree_node.set_node_classification(target_classifier.classify(data[0]))
    return id_tree_node


# # To construct an ID tree for 2014 Q2, Part A:
# print(construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type")))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
# tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
# print(id_tree_classify_point(tree_test_point, tree_tree))

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
# print(construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification")))
# print(construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class")))


#### Part 1E: Multiple choice ##################################################

ANSWER_1 = 'bark_texture'
ANSWER_2 = 'leaf_shape'
ANSWER_3 = 'orange_foliage'

ANSWER_4 = [2, 3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = 'No'
ANSWER_9 = 'No'


#### OPTIONAL: Construct an ID tree with medical data ##########################

## Set this to True if you'd like to do this part of the lab
DO_OPTIONAL_SECTION = False

if DO_OPTIONAL_SECTION:
    from parse import *
    medical_id_tree = construct_greedy_id_tree(heart_training_data, heart_classifiers, heart_target_classifier_discrete)


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### Part 2A: Drawing Boundaries ###############################################

BOUNDARY_ANS_1 = 3
BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4

BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### Part 2B: Distance metrics #################################################

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    prod = 0
    for i in range(len(u)):
        prod += u[i] * v[i]
    return prod

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return dot_product(v, v) ** 0.5

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    v = []
    for i, j in zip(point1, point2):
        v.append(i-j)
    return dot_product(v, v) ** 0.5

def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    v = []
    for i, j in zip(point1, point2):
        v.append(abs(i - j))
    return sum(v)

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    v = []
    for i, j in zip(point1, point2):
        if i != j:
            v.append(1)
    return sum(v)

def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    return 1 - dot_product(point1.coords, point2.coords)/(norm(point1.coords) * norm(point2.coords))


#### Part 2C: Classifying points ###############################################

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    dict_k, list_d = {}, []
    for i in range(len(data)):
        dict_k[i] = distance_metric(point, data[i]), data[i].coords
    for i in sorted(list(dict_k.keys()), key=lambda x: dict_k[x])[:k]:
        list_d.append(data[i])
    return list_d

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    k_points, names = get_k_closest_points(point, data, k, distance_metric), []
    for point in k_points:
        names.append(point.classification)
    return max(names, key=lambda x: names.count(x))


# # To run your classify function on the k-nearest neighbors problem from 2014 Q2
# # part B2, uncomment the line below and try different values of k:
# print(knn_classify_point(knn_tree_test_point, knn_tree_data, 1, euclidean_distance))


#### Part 2C: Choosing k #######################################################

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    results = []
    for i in range(len(data)):
        test = data[i]
        trainings = data[:i] + data[i+1:]
        results.append(1) if knn_classify_point(test, trainings, k, distance_metric) == test.classification \
            else results.append(0)
    return sum(results)/len(results)

def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    results = {}
    for dm in [euclidean_distance, manhattan_distance, hamming_distance, cosine_distance]:
        for k in range(1, len(data)):
            results[k, dm] = cross_validate(data, k, dm)
    return max(list(results.keys()), key=lambda x: results[x])


# # To find the best k and distance metric for 2014 Q2, part B, uncomment:
# print(cross_validate(knn_tree_data, 3, cosine_distance))
# print(find_best_k_and_metric(knn_tree_data))


#### Part 2E: More multiple choice #############################################

kNN_ANSWER_1 = "Overfitting"
kNN_ANSWER_2 = "Underfitting"
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3


#### SURVEY ####################################################################

NAME = 'Tuo Sun'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = 12
WHAT_I_FOUND_INTERESTING = 'learning the difference of distance measuring'
WHAT_I_FOUND_BORING = 'data structure of IdentificationTreeNode is too complex'
SUGGESTIONS = None
