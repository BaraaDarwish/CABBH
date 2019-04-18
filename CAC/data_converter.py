import numpy as np
selection=[False,
 False, False, True, False, False, False, False, False, True, False, False, True, True, False, False, True, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, True, True, True, False, False, False, False, False, False, True, False, True, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, False, True, False, False, False, True, False]
mask = [False,
 True, True, True, True, True, False, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]

def convert_int(obj , bits):
    obj = int(obj)
    if obj < 0 :
        binary_arr = [int(d) for d in str(0b111111111111 - bin(abs(obj)))[2:]]
    else:    
        binary_arr = [int(d) for d in str(bin(abs(obj)))[2:]]
    while len(binary_arr) < bits  :
              binary_arr.insert(0 , 0)         
    return binary_arr
       
            
def convert_objects(data):
    bits =[6, 9, 8, 8, 10, 10, 11, 8]
    converted = []
    for i in range(len(data)):
        converted += convert_int(data[i] ,bits[i])
    converted = np.array(converted)
    converted = converted[mask]
    converted = converted[selection]
    return converted

