allmoves = 'ABCD'

def find_next_move(allmoves, lev=1):
    if len(allmoves) <= 1:
        return [allmoves]
    r = []
    for x in range(len(allmoves)):
        s = allmoves[:x] + allmoves[x + 1:]
        p = find_next_move(s, lev + 1)
        for i in p:
            r.append(i + allmoves[x])
    print(lev)
    print(r)
    return r

find_next_move(allmoves)
# print(find_next_move(allmoves))