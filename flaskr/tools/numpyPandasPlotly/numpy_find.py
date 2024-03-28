import numpy as np

vals = np.array([-2,-1,1,2])
sings = np.sign(vals) # vals
diff_next = np.diff(sings) # [0, 2, 0]
zero_crossings = np.where(diff_next) # [[1], ]
print(vals[zero_crossings[0]]) # -1
