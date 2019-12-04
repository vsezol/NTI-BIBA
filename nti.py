import math


def length_from_origin(cords, origin):
    y0 = origin[2] - cords[2]
    x0 = math.sqrt((cords[0] - origin[0])**2 + (cords[1] - origin[1])**2)
    return -(y0/x0)

#5i + 2
n = int(input())
percy = []
size  = 4
origin = [22, 22, 50]
b = 50
cross = 0

for i in range(n):
    percy.append(list(map(float,input()[1:-1].split(','))))
    for k in range(2):
        percy[i][k] = percy[i][k]*5+2
    percy[i][2] = percy[i][2]*4
for i in range(len(percy)):
    k = length_from_origin(percy[i], origin)
    print(k)
    for k in range(len(percy)):
        x0 = -b/k
        print(math.sqrt((percy[i][0] - origin[0])**2 + (percy[i][1] - origin[1])**2))
        if math.sqrt((percy[k][0] - origin[0])**2 + (percy[k][1] - origin[1])**2) <= x0:# and math.sqrt((percy[k][0] - origin[0])**2 + (percy[k][1] - origin[1])**2) > math.sqrt((percy[i][0] - origin[0])**2 + (percy[i][1] - origin[1])**2):
            cross+=1

print(percy)