n = list(map(int, input().split()))
rows, cols = n[0], n[1]

ops = int(input())

M = [[0 for _ in range(0, cols)] for _ in range(0, rows)]

for _ in range(0, ops):
    n = input().split()
    op = n[0]
    top = (int(n[1])-1, int(n[2])-1)
    bot = (int(n[3])-1, int(n[4])-1)

    if op == "a":
        for i in range(top[0], bot[0]+1):
            for j in range(top[1], bot[1]+1):
                M[i][j] += 1
    elif op == "r":
        for i in range(top[0], bot[0]+1):
            for j in range(top[1], bot[1]+1):
                if M[i][j] > 0:
                    M[i][j] -= 1
    else:
        count = 0
        for i in range(top[0], bot[0]+1):
            for j in range(top[1], bot[1]+1):
                count += M[i][j]
        print(count)


#
# class Block:
#     def __init__(self, top, bot, op):
#         self.top = top
#         self.bot = bot
#         self.op = op
#
#     def is_in_block(self, point):
#         x_p, y_p = point
#         return (self.top[0] <= x_p <= self.bot[0]) and (self.top[1] <= y_p <= self.bot[1])
#
# n = list(map(int, input().split()))
# rows, cols = n[0], n[1]
#
# ops = int(input())
#
# blocks = []
# for _ in range(0, ops):
#     n = input().split()
#     op = n[0]
#     top = (int(n[1])-1, int(n[2])-1)
#     bot = (int(n[3])-1, int(n[4])-1)
#
#     if op == "q":
#         count = 0
#         for i in range(top[0], bot[0]+1):
#             for j in range(top[1], bot[1]+1):
#                 for b in blocks:
#                     if b.is_in_block((i,j)):
#                         if b.op == "a":
#                             count += 1
#                         else:
#                             if count > 0:
#                                 count -= 1
#         print(count)
#     else:
#         blocks.append(Block(top, bot, op))

