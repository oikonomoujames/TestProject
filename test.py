import math
import os
import random
import re
import sys
import collections

s = "1 3 9 9 27 81"
r = 3

arr = list(map(int, s.rstrip().split()))
dict1 = {}

count = 0

for each in arr:
    dict1[each] = arr.count(each)
    if (each/r) in dict1.keys() and (each/r/r) in dict1.keys():
        count += dict1[each]*dict1[each/r]*dict1[each/r/r]
        print("Found for: {}:{}:{}".format(each, (each/r), (each/r/r)))

print(count)
