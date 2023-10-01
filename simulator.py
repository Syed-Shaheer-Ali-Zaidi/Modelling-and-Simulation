import math
import random

mew = 8.98
Lambda = 2.25

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

def CPlookUp(Lambda, num_of_cust):
    array = []
    for i in range (0, num_of_cust):
        total = 0
        for x in range (0, i):
            temp = ((Lambda**x)*(math.e**-Lambda))/math.factorial(x)
            total += temp
        array.append(total)
    return array

def InterArrival(CP, CPlo, num_of_cust):
    IA = []
    for j in range (1, num_of_cust):
        temp = random.random()
        for i in range (0, num_of_cust - 1):
            if (temp<CP[i] and temp>CPlo[i]):
                IA.append(i)
    return IA

def Arrivals(arrivals, IA, num_of_cust):
    temp = 0
    for i in range (0, num_of_cust - 1):
        temp += IA[i]
        arrivals.append(temp)

def Service(num_of_cust):
    service = []
    for i in range (0, num_of_cust):
        temp = -mew * math.log(random.random())
        service.append(round(temp))
    return service

def generate_priority(A, M, Z0, C, a, b, num_of_cust):
    Z = [Z0]
    R = []
    RanNum = []
    GP =[]
    for i in range (0, num_of_cust):
        temp = (A*(Z[i])+C) % M
        Z.append(temp)
        R.append(Z[i+1])
        RanNum.append(R[i]/M)
        priority = a + RanNum[i] * (b - a)
        GP.append(round(priority))
    Z.remove(Z[-1])
    return Z, R, RanNum, GP

def main():
    arr1, num_of_cust = CP(Lambda)
    arr2 = CPlookUp(Lambda, num_of_cust)
    IA = InterArrival(arr1, arr2, num_of_cust)
    arrivals = [0]
    Arrivals(arrivals, IA, num_of_cust)
    IA.insert(0, 0)
    service = Service(num_of_cust)

if __name__ == "__main__":
    main()