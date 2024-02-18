import random

class Value:
    def __init__(self, value):
        self.value = value
    
arr = [Value(1), Value(2), Value(3), Value(0.0)]

rand1 = random.choices(arr)[0]
rand2 = random.choices(arr)[0]
rands = [rand1, rand2]
rands[0].value = 100

for value in arr:
    print(value.value)

