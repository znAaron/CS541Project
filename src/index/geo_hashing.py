# Morton curve
import logging
from RBTree import *

### temp
class Node:
    def __init__(self, id, lat, lon, name=None):
        self.id = id
        self.lat = lat
        self.lon = lon
        if name == None:
            self.name = str(id)
        else:
            self.name = name

    def location(self):
        return(self.lat, self.lon)
###


# 52 bit indexing
def geoToIndex(lat, lon):
    x = (lat + 90) * 67108864 / 180
    y = (lon + 180) * 67108864 / 360
    xstring = format(int(x), '026b')
    ystring = format(int(y), '026b')

    index_string = ''
    for i in range(26):
        index_string = index_string + xstring[i] + ystring[i]
    index = int(index_string, 2)

    return index

def common_prefix(str1, str2):
    prefix = ""
    for char1, char2 in zip(str1, str2):
        if char1 != char2:
            break
        prefix += char1
    return prefix

def is_point_in_rectangle(lat, lon, top_left, bottom_right):
    lat_in_range = top_left[0] >= lat >= bottom_right[0]
    lon_in_range = top_left[1] <= lon <= bottom_right[1]
    return lat_in_range and lon_in_range

node1 = Node(0, 40.387595008517565, -86.83694197890041, "Lafayette DQ")
node2 = Node(1, 40.41885820218638, -86.83954983820955, "Lafayette Chick-fil-A")
node3 = Node(2, 41.89089099113697, -87.61539023867564, "Chicago Rib")
node4 = Node(3, 37.64923160541447, -122.10684688701832, "California Olive Gardon")

tree_map = TreeMap()
tree_map.put(geoToIndex(node1.lat, node1.lon), node1)
tree_map.put(geoToIndex(node2.lat, node2.lon), node2)
tree_map.put(geoToIndex(node3.lat, node3.lon), node3)
tree_map.put(geoToIndex(node4.lat, node4.lon), node4)

n1 = geoToIndex(40.43064439174679, -86.87318931246699)
n2 = geoToIndex(40.3644383247257, -86.8171193789419)
bn1 = format(n1, '052b')
bn2 = format(n2, '052b')
prefix = common_prefix(bn1, bn2)
padded_string = prefix.ljust(52, '0')
start_index = int(padded_string, 2)

print(start_index)
iterator = tree_map.ceiling_iterator(start_index)

for key, value in iterator:
    if is_point_in_rectangle(value.lat, value.lon, (40.43064439174679, -86.87318931246699), (40.3644383247257, -86.8171193789419)):
        print(key, value.name)