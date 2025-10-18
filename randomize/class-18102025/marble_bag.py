import random

class marble_bag:
    def __init__(self, items, probs):
        self.bag = []
        self.items = items
        self.probs = probs
        self.fill_bag()

    def fill_bag(self):
        for i in range(len(self.items)):
            self.bag += [self.items[i]] * self.probs[i]

    def draw(self):
        item = random.choice(self.bag)
        self.bag.remove(item)
        if len(self.bag) <= 0:
            self.bag = self.fill_bag()
        return item

items = ['dirt', 'monster', 'gold']
probs = [7, 2, 1]
marblebag = marble_bag(items, probs)

for i in range(10):
    draw_item = marblebag.draw()
    print(draw_item, end=' ')