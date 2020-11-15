
import  numpy as np

arr = np.array([[1,2,2],[2,2,2],[3,3,3]])

arr_flip = np.flip(arr,axis=1)
arr_flip = np.flip(arr_flip,axis=0)

pos_opt = np.unravel_index(arr_flip.argmax(), arr_flip.shape)

print(len(arr_flip))

max = arr[len(arr)-pos_opt[1]-1,len(arr)-pos_opt[0]-1]
