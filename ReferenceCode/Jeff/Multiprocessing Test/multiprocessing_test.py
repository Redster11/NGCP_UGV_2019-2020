import concurrent.futures as cf
import multiprocessing as mp
import time




def factorial(num):
    fact = 1
    #print(f'Caculating {num} factorial')
    for x in range(num):
        if x!=0:
            fact = fact*x

    return fact



if __name__ == '__main__':
    startTime = time.perf_counter()

    numbers = [1,2,3,4]
    result = []

    startTime = time.perf_counter()

    #for x in numbers:
    #    result.append(factorial(x))

    with cf.ProcessPoolExecutor() as executor:
        result.append(executor.map(factorial, numbers))

    endTime = time.perf_counter()

    print(f'Time elapsed: {endTime - startTime}')
    for x in result:
        print(x)

