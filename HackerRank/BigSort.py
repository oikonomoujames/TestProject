import sys
from sys import getsizeof

unsorted = [31415926535897932384626433832795, 1, 3, 10, 3, 5]

# unsorted.sort()
"""
for each in unsorted:
    print(getsizeof(each))
"""
dict = {}
result = []

for each in unsorted:
    print(len(str(each)))
    if len(str(each)) in dict.keys():
        print("in")
        dict[len(str(each))].append(each)
    else:
        print("not in")
        newlist = [each]
        dict.update({len(str(each)):[each]})

keys = list(dict.keys())
keys.sort()
print(keys)

for val in dict.values():
    val.sort()

for each in keys:
    result.append(dict[each])

result = [item for sublist in result for item in sublist]

print(result)


