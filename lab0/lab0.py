# MIT 6.034 Lab 0: Getting Started
# Written by jb16, jmn, dxh, and past 6.034 staff

from point_api import Point
import sys

#### Multiple Choice ###########################################################

# These are multiple choice questions. You answer by replacing
# the symbol 'None' with a letter (or True or False), corresponding 
# to your answer.

# True or False: Our code supports both Python 2 and Python 3
# Fill in your answer in the next line of code (True or False):
ANSWER_1 = False

# What version(s) of Python do we *recommend* for this course?
#   A. Python v2.3
#   B. Python V2.5 through v2.7
#   C. Python v3.2 or v3.3
#   D. Python v3.4 or higher
# Fill in your answer in the next line of code ("A", "B", "C", or "D"):
ANSWER_2 = "D"


################################################################################
# Note: Each function we require you to fill in has brief documentation        # 
# describing what the function should input and output. For more detailed      # 
# instructions, check out the lab 0 wiki page!                                 #
################################################################################


#### Warmup ####################################################################

import math

def is_even(x):
    "If x is even, returns True; otherwise returns False"
    return True if x%2 == 0 else False 
    raise NotImplementedError

def decrement(x):
    """Given a number x, returns x - 1 unless that would be less than
    zero, in which case returns 0."""
    return x-1 if x-1>0 else 0
    raise NotImplementedError

def cube(x):
    "Given a number x, returns its cube (x^3)"
    return math.pow(x,3)
    raise NotImplementedError
    



#### Iteration #################################################################

def is_prime(x):
    "Given a number x, returns True if it is prime; otherwise returns False"
    y = False
    
    if x > 2:
        
        for i in (2, int(x**0.5)+1):
            i = 2
            if x%i == 0:
                y = False
            else:
                y = True
                i += 1
        
    elif x == 1 or x == 2: y = True
    
    return True if y else False

    raise NotImplementedError

def primes_up_to(x):
    "Given a number x, returns an in-order list of all primes up to and including x"
    l = []
           
    for num in range(2, math.floor(x+1)):
        if all(num%i!=0 for i in range(2,num)):
            l.append(num)            
                
    return l

    raise NotImplementedError


#### Recursion #################################################################

def fibonacci(n):
    "Given a positive int n, uses recursion to return the nth Fibonacci number."
    if n==1:
        return 1
    elif n==2:
        return 1
    else:
        return fibonacci(n-2) + fibonacci(n-1)
    
    raise NotImplementedError

def expression_depth(expr):
    """Given an expression expressed as Python lists, uses recursion to return
    the depth of the expression, where depth is defined by the maximum number of
    nested operations."""
    
    if not isinstance(expr, list):
        return 0
    
    return max(map(expression_depth, expr)) + 1

    raise NotImplementedError


#### Built-in data types #######################################################

def remove_from_string(string, letters):
    """Given a string and a list of individual letters, returns a new string
    which is the same as the old one except all occurrences of those letters
    have been removed from it."""
    
    strlist = list(string)
    newstr = ''.join(c for c in strlist if c not in letters)
    
    return newstr
    
    raise NotImplementedError

def compute_string_properties(string):
    """Given a string of lowercase letters, returns a tuple containing the
    following three elements:
        0. The length of the string
        1. A list of all the characters in the string (including duplicates, if
           any), sorted in REVERSE alphabetical order
        2. The number of distinct characters in the string (hint: use a set)
    """

    
    a = len(string)
    
    b = sorted(list(string.lower()))
    b.reverse()
    
    c = len(set(string))
    
    return (a, b, c)
    raise NotImplementedError

def tally_letters(string):
    """Given a string of lowercase letters, returns a dictionary mapping each
    letter to the number of times it occurs in the string."""
    d = {}
    
    orilist = list(string.lower())
    setlist = list(set(string))
    
    for i in setlist:
        d[i] = orilist.count(i)
        
    return d
    raise NotImplementedError


#### Functions that return functions ###########################################

def create_multiplier_function(m):
    "Given a multiplier m, returns a function that multiplies its input by m."
    def multiplier(x):
        return x * m    
    return multiplier

    raise NotImplementedError

def create_length_comparer_function(check_equal):
    """Returns a function that takes as input two lists. If check_equal == True,
    this function will check if the lists are of equal lengths. If
    check_equal == False, this function will check if the lists are of different
    lengths."""
    
    def comparer(x,y):
        if check_equal == True and len(x) == len(y):
            return True
        elif check_equal == False and len(x) != len(y):
            return True
        else: 
            return False
        
    return comparer
    
    raise NotImplementedError


#### Objects and APIs: Copying and modifing objects ############################

def sum_of_coordinates(point):
    """Given a 2D point (represented as a Point object), returns the sum
    of its X- and Y-coordinates."""
    return point.sum_xy()
    raise NotImplementedError

def get_neighbors(point):
    """Given a 2D point (represented as a Point object), returns a list of the
    four points that neighbor it in the four coordinate directions. Uses the
    "copy" method to avoid modifying the original point."""
    
    x = point.getX()
    y = point.getY()
    
    a = point.copy()
    a.setX(x-1)
    
    b = point.copy()
    b.setX(x+1)
    
    c = point.copy()
    c.setY(y-1)
    
    d = point.copy()
    d.setY(y+1)
    
    return (a,b,c,d)
    raise NotImplementedError


#### Using the "key" argument ##################################################

def sort_points_by_Y(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "sorted"
    with the "key" argument to create and return a list of the SAME (not copied)
    points sorted in decreasing order based on their Y coordinates, without
    modifying the original list."""

    d={}
    
    for point in list_of_points:
        d[(point.getY(),point.getX())] = point
        
    l = sorted(d, reverse=True)
    
    finallist=[]
    
    for item in l:
        newpt = d[item]
        
        finallist.append(newpt)
        
    return finallist
        
    raise NotImplementedError

def furthest_right_point(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "max" with
    the "key" argument to return the point that is furthest to the right (that
    is, the point with the largest X coordinate)."""
    
    d={}
    
    for point in list_of_points:
        d[(point.getX(),point.getY())] = point
        
    l = sorted(d, reverse=True)
    
    maxXpt = d[l[0]]
    
    return maxXpt

    raise NotImplementedError


#### SURVEY ####################################################################

# How much programming experience do you have, in any language?
#     A. No experience (never programmed before this lab)
#     B. Beginner (just started learning to program, e.g. took one programming class)
#     C. Intermediate (have written programs for a couple classes/projects)
#     D. Proficient (have been programming for multiple years, or wrote programs for many classes/projects)
#     E. Expert (could teach a class on programming, either in a specific language or in general)

PROGRAMMING_EXPERIENCE = "B"


# How much experience do you have with Python?
#     A. No experience (never used Python before this lab)
#     B. Beginner (just started learning, e.g. took 6.0001)
#     C. Intermediate (have used Python in a couple classes/projects)
#     D. Proficient (have used Python for multiple years or in many classes/projects)
#     E. Expert (could teach a class on Python)

PYTHON_EXPERIENCE = "C"


# Finally, the following questions will appear at the end of every lab.
# The first three are required in order to receive full credit for your lab.

NAME = "TUO SUN"
COLLABORATORS = "SEN DAI"
HOW_MANY_HOURS_THIS_LAB_TOOK = 8
SUGGESTIONS = None #optional
