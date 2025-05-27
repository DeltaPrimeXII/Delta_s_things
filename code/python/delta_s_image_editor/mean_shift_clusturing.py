# function file to import

from math import sqrt, floor
from color_conversion import round_rgb

#----------------------------------------------------------------------------------------------------
def distance(a, b): #(x, y, z)

    x = b[0] - a[0]
    y = b[1] - a[1]
    z = b[2] - a[2]

    return sqrt(x**2 + y**2 + z**2)
#----------------------------------------------------------------------------------------------------
def mean(liste): #[(x, y, z), ...]

    if len(liste) == 0:
        return liste
    else:
        print(f"len(list) == {len(liste)}")
        x = sum([liste[i][0] for i in range(len(liste))]) / len(liste)
        y = sum([liste[i][1] for i in range(len(liste))]) / len(liste)
        z = sum([liste[i][2] for i in range(len(liste))]) / len(liste)

        return (x, y, z, 255)
#----------------------------------------------------------------------------------------------------
def re_range(tup, cell):
    xyz = [int(floor(tup[0]/(256/(cell)))), int(floor(tup[1]/(256/(cell)))), int(floor(tup[2]/(256/(cell))))]
    
    # for i in range(len(xyz)):
    #     if xyz[i] > 0:
    #         xyz[i] += -1
    return xyz
#----------------------------------------------------------------------------------------------------
def dico_mean(liste): #{(x, y, z): n, ...}

    # print(liste)
    if len(liste) == 0:
        return liste
    else:
        x = sum([k[0]*v for k,v in liste.items()]) / sum([v for v in liste.values()])
        y = sum([k[1]*v for k,v in liste.items()]) / sum([v for v in liste.values()])
        z = sum([k[2]*v for k,v in liste.items()]) / sum([v for v in liste.values()])

        return (x, y, z, 255)
#----------------------------------------------------------------------------------------------------
def celled_list(liste, cell= 8): #return a celled 3d list

    celled = []
    line = []
    column = []
    for y in range(cell):
        for x in range(cell):
            for z in range(cell):
                column.append({})
            line.append(column)
            column = []
        celled.append(line)
        line = []

    for y in range(len(liste)):
        for x in range(len(liste[y])):
            a, b, c = re_range(liste[y][x], cell)
            if not liste[y][x] in celled[a][b][c].keys():
               celled[a][b][c][liste[y][x]] = 1
            else:
                celled[a][b][c][liste[y][x]] += 1

    return celled
#----------------------------------------------------------------------------------------------------
def mean_shift_broken(list_3d, pos, cell= 8, r= 16): #BROKEN
    
    while True:
        pos_list = []
        print("POS_LIST",pos_list)
        print("POS",pos)
        a, b, c = int(round(pos[0]/(256/(cell-1)))), int(round(pos[1]/(256/(cell-1)))), int(round(pos[2]/(256/(cell-1))))
        for i in range(-1, 2):
            for e in range(-1, 2):
                for u in range(-1, 2):
                    if 0 <= a+i < cell and 0 <= b+e < cell and 0 <= c+u < cell:
                        for k, v in list_3d[a+i][b+e][c+u].items():
                            if distance(pos, k) <= r:
                                pos_list.append({k:v})
        if not pos_list:
            print(pos)
            return pos
        if dico_mean(pos_list) == pos:
            print(pos)
            return pos
        else:
            pos = dico_mean(pos_list)
#----------------------------------------------------------------------------------------------------
def mean_shift(list_3d, pos, cell= 8, r= 16):

    while True:
        pos_dico = {}
        a, b, c = re_range(pos, cell)
        for d in range(-1, 2):
            for e in range(-1, 2):
                for f in range(-1, 2):
                    if 0 <= a+d < cell and 0 <= b+e < cell and 0 <= c+f < cell:
                        for k in list_3d[a+d][b+e][c+f].keys():
                            if distance(pos, k) <= r:
                                pos_dico[k] = list_3d[a+d][b+e][c+f][k]

        # print(pos_dico)
        if len(pos_dico) == 0:
            # print("NADA")
            return None
        m = dico_mean(pos_dico)
        if pos == m:
            # print("ZZZ", round_rgb(pos))
            return round_rgb(pos)
        else:
            # print("AGAIN", m)
            pos = m
#----------------------------------------------------------------------------------------------------
def mean_shift_clusturing(liste, cell=8, r=16):

    x = 256/cell
    cluster = []
    for d in range(cell):
        for e in range(cell):
            for f in range(cell):
                # print("number",d,e,f)
                a, b, c = d*x+(x/2), e*x+(x/2), f*x+(x/2)
                color = mean_shift(celled_list(liste, cell), (a,b,c,255), cell, r)
                if color != None and not color in cluster:
                    # print("new color", color)
                    cluster.append(color)
    # print(cluster)
    return cluster
#----------------------------------------------------------------------------------------------------
# print(celled_list([[(0,160,0,255), (32,50,255,255), (200,20,60,255), (255,255,255,255)],
# [(0,160,0,255), (16,50,255,255), (200,20,60,255), (255,255,255,255)],
# [(0,160,0,255), (16,50,255,255), (200,20,60,255), (255,255,255,255)],
# [(0,160,0,255), (16,50,255,255), (200,20,60,255), (255,255,255,255)]]))

# print(re_range((16,50,255,255),8))
# print(re_range((31,50,255,255),8))

print("mean_shift_clusturing.py LOADED")