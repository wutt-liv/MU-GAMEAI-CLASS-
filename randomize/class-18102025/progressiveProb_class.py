import random

class progressiveProb
    def __init__(self, items, start_success_rate):
        self.bag = []
        self.items = items
        self.start_success_rate = []

    def draw(self):
        num = random.uniform(0,100)
        

start_success_rate = 99
success_rate = start_success_rate
items = ['dirt', 'monster', 'gold']
probs = [7, 2, 1]
itemsbag = progressiveProb(items, probs)

for i in range(10):
    draw_item = itemsbag.draw()
    print(draw_item, end=' ')

for i in range(10):
    num = random.uniform(0,100)

    if num <= success_rate:
        print("success!")
        success_rate = start_success_rate
    else:
        success_rate += 5
        print(" sad :( ")
  