import random

start_success_rate = 20
success_rate = start_success_rate
attempts = 0
fixed_limit = 5

for i in range(10):
    num = random.uniform(0,100)

    if num <= success_rate or attempts >= fixed_limit:
        print("success!")
        attempts = 0
    else:
        attempts += 1
        print(" sad :( ")