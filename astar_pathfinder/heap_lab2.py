import heapq

numbers = [1, 5, 9, 7, 0]

heapq.heapify(numbers) # create a heap tree
print(numbers)

heapq.heappush(numbers, 3) # ใส่เลข 3 พร้อม sort ใน heap tree

n = heapq.heappop(numbers) #ดึงค่าต่ำสุด
print(n)
print(numbers)