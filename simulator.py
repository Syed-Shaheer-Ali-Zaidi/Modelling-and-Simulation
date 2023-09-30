import math
import random

mew = 8.98
Lambda = 2.25
num_of_cust = 10

def CP(Lambda):
    array = []
    i=1
    total = 0
    num_of_cust = 0
    while total != 1:
        total = 0
        for x in range (0, i):
            temp = ((Lambda**x)*(math.e**-Lambda))/math.factorial(x)
            total += temp
        array.append(total)
        i+=1
        num_of_cust+=1
    return array, num_of_cust

def CPlook(Lambda, num_of_cust):
    array = []
    for i in range (0, num_of_cust):
        total = 0
        for x in range (0, i):
            temp = ((Lambda**x)*(math.e**-Lambda))/math.factorial(x)
            total += temp
        array.append(total)
    return array

arr1, num_of_cust = CP(Lambda)
arr2 = CPlook(Lambda, num_of_cust)
IA = []

for j in range (1, num_of_cust):
    temp = random.random()
    for i in range (0, num_of_cust - 1):
        if (temp<arr1[i] and temp>arr2[i]):
            IA.append(i)

arrivals = [0]
temp = 0
for i in range (0, num_of_cust - 1):
    temp += IA[i]
    arrivals.append(temp)
IA.insert(0, 0)

service = []
for i in range (0, num_of_cust):
    temp = -mew * math.log(random.random())
    service.append(round(temp))