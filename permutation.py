# def perm(l):
#     # Compute the list of all permutations of l
#     if len(l) <= 1:
#         return [l]
#     r = []
#     for i in range(len(l)):
#         s = l[:i] + l[i + 1:]
#         p = perm(s)
#         for x in p:
#             r.append(l[i:i + 1] + x)
#     return r
#
# perm('hello')

levels = set([l[0] for l in groupby(self.score, key=lambda x: x[1])])
        total = {}
        for move in self.score:
            firstmv = str(move[2][0])
            if firstmv not in total.keys():
                total.update({firstmv: {move[1]: move[0]}})
            else:
                if move[1] not in total[firstmv].keys():
                    total[firstmv].update({move[1]: move[0]})
                else:
                    total[firstmv][move[1]] += move[0]
        for k, v in total.items():
            print(k + ' ' + str(v))
prev_value = None
for level in levels:
    tmp = 0
    for k, v in total.items():
        if prev_value:
            if v[level] < prev_value and level % 2 == 1:
                tmp = v[level]
            if v[level] > prev_value and level % 2 == 0:
                tmp = v[level]
        else:
            tmp = v[level]
    print(level)
    print(tmp)