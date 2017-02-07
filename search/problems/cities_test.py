from cities import cities

dists = [45, 44, 151, 100, 100, 118, 189, 175, 156, 66, 109, 191, 89, 130, 180, 116, 101, 128, 85, 137, 126, 150, 174, 70, 130, 135, 121, 65, 140, 103, 156, 110, 157, 74, 142, 68, 61, 72, 74, 46, 80, 100, 94, 60, 85, 104, 90, 193, 81, 120, 151, 67, 128, 80, 115, 69, 85, 96, 63, 116, 99, 69, 74, 76, 47, 95, 80]

real_sld = 9881

assert(len(dists) == 67)

print(len(cities.keys()))
print(len(set(cities.keys())))

sld = 0
distance = 0
count = 0
for city in cities:
    sld += cities[city]['sld']
    for neighbour in cities[city]:
        if neighbour != 'sld':
            assert(list(cities.keys()).index(neighbour) > -1)
            print(city)
            print(neighbour)
            d = cities[city][neighbour]
            assert(dists.index(d) > -1)
            distance += d
            count += 1
            assert(cities[neighbour][city] == d)

print(count)
assert(count == 134)

print(distance)
assert(distance == 14202)

print(sld)
print(real_sld)
assert(sld == real_sld)
