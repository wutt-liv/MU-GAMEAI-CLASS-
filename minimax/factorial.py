n = 5
#result = n*(n-1)*...*1

def cal_factorial(n, depth):

    #ending condition
    if n <= 1:
        return 1
    
    result = n*cal_factorial(n-1, depth+1)

    return result

result = cal_factorial(n, 0)

print(f"factorial is : {result}")