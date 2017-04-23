pos = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
# the last ones we need are 1,5,9 and 3,5,7
for y in range(0,3):
    tmp_hor = []
    tmp_ver = []
    for x in range(0,3):
       tmp_hor.append(pos[x][y])
       tmp_ver.append(pos[y][x])
    print(tmp_ver)
    print(tmp_hor)