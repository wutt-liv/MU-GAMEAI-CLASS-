import random

start_success_rate = 20
success_rate = start_success_rate

for i in range(10):
    num = random.uniform(0,100)

    if num <= success_rate:
        print("success!")
        success_rate = start_success_rate
    else:
        success_rate += 5
        print(" sad :( ")
  