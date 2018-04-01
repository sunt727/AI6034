import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sql
import pandas as pd

# alist = [i**i for i in range(10)]
# print(alist)
#
# blist = [(i, j, i*j) for i in range(1, 11) for j in range(1, 11) if i != j]
# print(blist)
# print(max(blist, key=lambda x: x[1]))
# bset = set(blist)
# print(bset)
# maxone, *middleone, minone = sorted(blist, key=lambda x: x[2], reverse=True)
# print(maxone, minone)
# clist = filter(lambda x: x[0]>5, blist)
# print(clist)

#
# L = [[1, 2], [3, 4], [5, 6, 7]]
#
# def deep_reverse(L):
#     """ assumes L is a list of lists whose elements are ints
#     Mutates L such that it reverses its elements and also
#     reverses the order of the int elements in every element of L.
#     It does not return anything.
#     """
#     for x in L:
#         x.reverse()
#     L.reverse()
#
# print(L)
# deep_reverse(L)
# print(L)
#
# def f(i):
#     return i + 2
# def g(i):
#     return i > 5
#
#
# def applyF_filterG(L,f,g):
#     L[:] = [i for i in L if g(f(i))]
#     return max(L) if L else -1
#
#
# L = [0, -10, 5, 6, -4]
# print(applyF_filterG(L, f, g))
# print(L)
#
#
# ### Do not change the Location or Campus classes. ###
# ### Location class is the same as in lecture.     ###
# class Location(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def move(self, deltaX, deltaY):
#         return Location(self.x + deltaX, self.y + deltaY)
#
#     def getX(self):
#         return self.x
#
#     def getY(self):
#         return self.y
#
#     def dist_from(self, other):
#         xDist = self.x - other.x
#         yDist = self.y - other.y
#         return (xDist ** 2 + yDist ** 2) ** 0.5
#
#     def __eq__(self, other):
#         return (self.x == other.x and self.y == other.y)
#
#     def __str__(self):
#         return '<' + str(self.x) + ',' + str(self.y) + '>'
#
#
# class Campus(object):
#     def __init__(self, center_loc):
#         self.center_loc = center_loc
#
#     def __str__(self):
#         return str(self.center_loc)
#
#
# class MITCampus(Campus):
#     """ A MITCampus is a Campus that contains tents """
#
#     def __init__(self, center_loc, tent_loc=Location(0, 0)):
#         """ Assumes center_loc and tent_loc are Location objects
#         Initializes a new Campus centered at location center_loc
#         with a tent at location tent_loc """
#         self.center_loc = center_loc
#         self.tent_loc = tent_loc
#         self.list_tent = [tent_loc]
#
#     def add_tent(self, new_tent_loc):
#         """ Assumes new_tent_loc is a Location
#         Adds new_tent_loc to the campus only if the tent is at least 0.5 distance
#         away from all other tents already there. Campus is unchanged otherwise.
#         Returns True if it could add the tent, False otherwise. """
#         is_valid = all(tent.dist_from(new_tent_loc) >= 0.5 for tent in self.list_tent)
#         if is_valid:
#             self.list_tent.append(new_tent_loc)
#         return is_valid
#
#     def remove_tent(self, tent_loc):
#         """ Assumes tent_loc is a Location
#         Removes tent_loc from the campus.
#         Raises a ValueError if there is not a tent at tent_loc.
#         Does not return anything """
#         if tent_loc in self.list_tent:
#             self.list_tent.remove(tent_loc)
#         else:
#             raise ValueError
#
#     def get_tents(self):
#         """ Returns a list of all tents on the campus. The list should contain
#         the string representation of the Location of a tent. The list should
#         be sorted by the x coordinate of the location. """
#         return [str(x) for x in sorted(self.list_tent, key=lambda a: a.x)]
#
#
# c = MITCampus(Location(1,2))
#
# print(c.add_tent(Location(2,3))) #should return True
# print(c.add_tent(Location(1,2))) #should return True
# print(c.add_tent(Location(0,0))) #should return False
# print(c.add_tent(Location(2,3))) #should return False
# print(c.get_tents()) #should return ['<0,0>', '<1,2>', '<2,3>']
#
# def longest_run(L):
#     """
#     Assumes L is a list of integers containing at least 2 elements.
#     Finds the longest run of numbers in L, where the longest run can
#     either be monotonically increasing or monotonically decreasing.
#     In case of a tie for the longest run, choose the longest run
#     that occurs first.
#     Does not modify the list.
#     Returns the sum of the longest run.
#     """
#     continues = [L[i:j] for i in range(len(L)) for j in range(len(L)+1)
#                  if L[i:j] == sorted(L[i:j], reverse=True) or L[i:j] == sorted(L[i:j])]
#     return sum(max(continues, key=lambda x: len(x)))
#
#
# L = [10, 4, 3, 8, 3, 4, 5, 7, 7, 2]
# print(longest_run(L))
# L = [5, 4, 10]
# print(longest_run(L))
# print(longest_run([-1, -10, -10, -10, -10, -10, -10, -100]))
#
#
# t1 = (1, 2, 3, 'abc')
# t2 = ( 5, 6, t1)
# print((t1+t2)[1:3])
#
# L1 = ['a', 'b', 'c']
# L2 = L1[:]
# print( 'L1 = ', L1 )
# print( 'L2 = ', L2 )
# L1.append('d')
# print( 'L1 = ', L1 )
# print( 'L2 = ', L2 )
#
# def fib(x):
#     assert type(x) == int and x >= 0
#     if x == 0 or x == 1:
#         return 1
#     else:
#         return fib(x-1) + fib(x-2)
#
# print(fib(20))
#
# def fib_u(x):
#     assert type(x) == int and x >= 1
#     fibs = [1,1]
#     while fibs[-2] + fibs[-1] <= x:
#         fibs.append(fibs[-2] + fibs[-1])
#     return fibs, max(fibs)
#
# print(fib_u(30))
# #
# a = [n for n in range(15)]
# b = [np.log(n) for n in range(15)]
# c = [2**n for n in range(15)]
# d = [n**2 for n in range(15)]
# e = [n * np.log(n) for n in range(15)]
#
#
# plt.plot(a, a, label='n')
# plt.plot(a, b, label='log(n)')
# plt.plot(a, c, label='2**n')
# plt.plot(a, d, label='n**2')
# plt.plot(a, e, label='n log(n)')
# plt.legend(loc='best')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.semilogy()
# plt.show()

# connection = sql.connect("new.db")
#
# cursor = connection.cursor()
#
# #delete
# #cursor.execute("""DROP TABLE employee;""")
#
# sql_command = """
# CREATE TABLE employee (
# staff_number INTEGER PRIMARY KEY,
# fname VARCHAR(20),
# lname VARCHAR(30),
# gender CHAR(1),
# joining DATE,
# birth_date DATE);"""
#
# cursor.execute(sql_command)
#
# sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#     VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
# cursor.execute(sql_command)
#
#
# sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
#     VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17");"""
# cursor.execute(sql_command)

# never forget this, if you want the changes to be saved:
# connection.commit()
#
# connection.close()
#
# dates = pd.date_range('20130101', periods=5)
# df = pd.DataFrame(np.random.randn(5,4), index=dates, columns=list('ABCD'))
#
# print(df)
# print(df.describe())
# df2 = df.sort_values(by='A')
# print(df2)
# print(df.loc[dates[0], 'B'])
# print(df.apply(lambda x: x.max() - x.min()))
# df = df.cumsum()
#
# plt.figure(); df.plot(); plt.legend(loc='best')
# plt.show()

# macsv = pd.read_csv('R11484002_SL140.csv')
# ma10 = macsv.head(100)
# ma10pop = ma10.loc[1:,['Census Tract', 'Total Population', 'Area (Land)', 'Total: Chinese, Except Taiwanese']]
# ma10pop = ma10pop.convert_objects(convert_numeric=True)
# ma10pop.loc[:,'Density'] = ma10pop.loc[:,'Total Population']/ma10pop.loc[:,'Area (Land)']
# ma10pop = ma10pop.sort_values(by='Density')
# #print(ma10pop)
# ma10pop = ma10pop.cumsum()
# plt.plot(ma10pop['Total Population']/ma10pop['Area (Land)'],
#          ma10pop['Total: Chinese, Except Taiwanese'],
#          label='Chinese')
# # plt.bar(ma10pop['Total Population']/ma10pop['Area (Land)'],
# #        ma10pop['Total: Chinese, Except Taiwanese'],
# #        1000,
# #        align='center',
# #        alpha=0.5)
# # plt.figure(); ma10pop.plot();
# plt.xlabel('Chinese')
# plt.ylabel('Population Density')
# plt.title('Chinese Distribution by Population Density')
# plt.legend(loc='best')
# plt.show()

def binToInt(s):
    """
    assumes: s is a str containing only 0's and 1's
    returns the int corresponding to the binary number
    represented by s. If s is empty, returns 0.
    """
    if len(s) == 0:
        return 0
    elif all((i in ['1', '0']) for i in s):
        return int(s,2)#sum((2 ** j) * int(s[-j - 1]) for j in range(len(s)))



print(binToInt('1010'))
print(binToInt('01010'))
print(binToInt('01010110'))
print(binToInt('00000110'))
print(binToInt(''))
#
# def rewrite(s):
#     """
#     assumes: s is a string
#     returns a new string, in which each character of the
#        original string appears sorted by the number of
#        occurrences, from most common to least common.
#        E.g., if the most common character occurs 5 times,
#        then 5 copies of that character would start the
#        returned string, followed by the second most common
#        character, etc. In the case of ties, any order is
#        acceptable.
#     """
#     dict = {}
#     for l in s:
#         dict[l] = dict.get(l, 0) + 1
#     outlist = [i*dict[i] for i in sorted(dict.keys(), key=lambda x: dict[x], reverse=True)]
#     return ''.join(outlist)
#
#
# test = "this is a test"
# print(rewrite(test))
#
#
# class strList(object):
#     # strLists are mutable lists of strs
#
#     def __init__(self):
#         """
#         creates an empty strList
#         """
#         self.strlist = []
#         self.strlistarchive = []
#
#     def append(self, s):
#         """
#         assumes s is a str
#         adds s to the end of self, returns None
#         """
#         self.strlist.append(s)
#         self.strlistarchive.append(s)
#
#
#     def delete(self, s):
#         """
#         assumes s is a str
#         deletes the first occurrence of s in self and returns None
#         if s does not occur in self, raises ValueError
#         """
#         if s in self.strlist:
#             self.strlist.remove(s)
#         else:
#             raise ValueError
#
#
#     def len(self):
#         """
#         Returns an int that is the sum of the length of the
#         strings in self
#         """
#         return sum(len(l) for l in self.strlist)
#
#     def uniqueAppends(self):
#         """
#         returns an int that is the total number of unique strings,
#         including deleted elements, that have ever been
#         appended to self
#         """
#         return len(set(self.strlistarchive))
#
#
#     def __str__(self):
#         """
#         returns a str that is the concatenation of all of the
#         strs in self
#         """
#         return ''.join(self.strlist)
#
#
# sl = strList()
# sl.append('john')
# sl.append('ana')
# sl.append('john')
# sl.append('ana')
# try:
#     sl.delete('an')
# except ValueError:
#     print('ValueError')
# sl.delete('ana')
# print(sl.len())
# print(sl.uniqueAppends())
# print(sl)
#
# class newStr(str):
#     def __init__(self, input):
#         """
#         creates an empty strList
#         """
#         self.s = input
#
#     def bicut(self):
#         if len(self.s) > 2:
#             return self.s[0]+self.s[-1]
#         else:
#             return newStr('')
#
# new = newStr('abcd')
# print(type(new))
# print(new.bicut())
# print(new.bicut())
#
#
# def f(a, b):
#     if len(b) == 0:
#         return a, b
#     else:
#         a.append(b[0])
#         b.pop(0)
#         return f(a,b)
#
# l1 = [1, 2]
# l2 = [3,4]
# print(f(l1, l2))
# l3 = l1
# #print(f(l3, l1))
