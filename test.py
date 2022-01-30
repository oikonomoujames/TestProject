arr =[4, 5, 3, 7, 2]

pivot = arr[0]
left = []
right = []
equal = []

for each in arr:
    if each == pivot:
        equal.append(each)
    elif each > pivot:
        right.append(each)
    elif each < pivot:
        left.append(each)
    else:
        print("error")

print(left + equal + right)