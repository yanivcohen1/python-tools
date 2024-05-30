import numpy as np

# if else inline
# x=np.random.randint(100, size=(10,5))
x = np.array([[1,2,3], [3,2,1]])
out_x = np.where(x<=2, x+1, x-1) # like list comprehension
print(out_x) # [[2 3 2], [2 3 2]]

# filter only (x<2) | (x>2)
x = np.array([1,2,3,4])
out_x = x[(x<2) | (x>2)]
print(out_x) # [1 3 4] no 2

# find indexs where x>2
out_x = np.where(x<=2) # return indexs
print(out_x) # [0, 1] indexs
print(x[out_x]) # [1 2] values

# find val where changing sing (-1 to 1 changing sing) return val -1
vals = np.array([-2,-1,1,2])
sings = np.sign(vals) # vals
diff_next = np.diff(sings) # [0, 2, 0]
zero_crossings = np.where(diff_next) # [[1], ]
print(vals[zero_crossings[0]]) # -1
