import networkx as nx
import math
import matplotlib.pyplot as plt
import json
import numpy as np

file_name = 'moscow'
# 1 -  with star; 0 - without star
what_draw = 1
with open(file_name + '.json') as data_file:
    data_item = json.load(data_file)
G = nx.Graph()

def make_graph_without_limitation():
    number = 0
    while number < len(data_item):
        G.add_node(number, pos=(data_item[number]['lng'], data_item[number]['lat']))
        if number > 0:
            G.add_edge(number-1, number)
        number = number + 1


def angle_between_vectors(lat1,lng1,lat2,lng2,lat3,lng3):
    x1 = lng1 * np.pi / 180
    y1 = lat1 * np.pi / 180

    x2 = lng2 * np.pi / 180
    y2 = lat2 * np.pi / 180

    x3 = lng3 * np.pi / 180
    y3 = lat3 * np.pi / 180

    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x3 - x2
    dy2 = y3 - y2

    top = dx1 * dx2 + dy1 * dy2
    bottom1 = np.sqrt(dx1 * dx1 + dy1 * dy1)
    bottom2 = np.sqrt(dx2 * dx2 + dy2 * dy2)
    bottom = bottom1*bottom2
    answer = top/bottom
    rad = np.arccos(answer)
    angle = rad * 180 / np.pi
    return angle

def sorting(file_name):
    sorting_true = 1
    for j in range(len(data_item)):
        if sorting_true == 0:
            break
        else:
            sorting_true = 0
        k = 0
        while(k < (len(data_item) - 1)):
            if data_item[k]['ts'] > data_item[k + 1]['ts']:
                if 'sat_cnt' in data_item[k + 1]:
                    sat_cnt = data_item[k + 1]['sat_cnt']
                    if 'sat_cnt' in data_item[k]:
                        data_item[k + 1]['sat_cnt'] = data_item[k]['sat_cnt']
                    else:
                        data_item[k + 1].pop('sat_cnt')
                    data_item[k]['sat_cnt'] = sat_cnt
                else:
                    if 'sat_cnt' in data_item[k]:
                        data_item[k + 1]['sat_cnt'] = data_item[k]['sat_cnt']
                        data_item[k].pop('sat_cnt')

                if 'direction' in data_item[k + 1]:
                    direction = data_item[k + 1]['direction']
                    if 'direction' in data_item[k]:
                        data_item[k + 1]['direction'] = data_item[k]['direction']
                    else:
                        data_item[k + 1].pop('direction')
                    data_item[k]['direction'] = direction
                else:
                    if 'direction' in data_item[k]:
                        data_item[k + 1]['direction'] = data_item[k]['direction']
                        data_item[k].pop('direction')

                if 'speed' in data_item[k + 1]:
                    speed = data_item[k + 1]['speed']
                    if 'speed' in data_item[k]:
                        data_item[k + 1]['speed'] = data_item[k]['speed']
                    else:
                        data_item[k + 1].pop('speed')
                    data_item[k]['speed'] = speed
                else:
                    if 'speed' in data_item[k]:
                        data_item[k + 1]['speed'] = data_item[k]['speed']
                        data_item[k].pop('speed')

                lng = data_item[k + 1]['lng']
                lat = data_item[k + 1]['lat']
                ts = data_item[k + 1]['ts']

                data_item[k + 1]['lng'] = data_item[k]['lng']
                data_item[k + 1]['lat'] = data_item[k]['lat']
                data_item[k + 1]['ts'] = data_item[k]['ts']

                data_item[k]['lng'] = lng
                data_item[k]['lat'] = lat
                data_item[k]['ts'] = ts

                sorting_true = 1

            k = k + 1
    file_name = file_name + "-sorting"
    obj = open(file_name + ".json", "w")
    obj.write(json.dumps(data_item))
    obj.close
    return file_name

def delete_duplicate(file_name):
        duplicate_true = 1

        for j in range(len(data_item)):
            if duplicate_true == 0:
                break
            else:
                duplicate_true = 0
            k = 0
            while (k < (len(data_item) - 1)):
                if data_item[k]['ts'] == data_item[k + 1]['ts']:
                    if 'sat_cnt' in data_item[k]:
                        if 'sat_cnt' in data_item[k + 1]:
                            if data_item[k]['sat_cnt'] == data_item[k + 1]['sat_cnt']:
                                if 'direction' in data_item[k]:
                                    if 'direction' in data_item[k + 1]:
                                        if data_item[k]['direction'] == data_item[k + 1]['direction']:
                                            if 'speed' in data_item[k]:
                                                if 'speed' in data_item[k + 1]:
                                                    if data_item[k]['speed'] == data_item[k + 1]['speed']:
                                                        # print k
                                                        data_item.pop(k)
                                                        duplicate_true = 1
                                            else:
                                                if 'speed' not in data_item[k + 1]:
                                                    # print k
                                                    data_item.pop(k)
                                                    duplicate_true = 1
                                else:
                                    if 'direction' not in data_item[k + 1]:
                                        if 'speed' in data_item[k]:
                                            if 'speed' in data_item[k + 1]:
                                                if data_item[k]['speed'] == data_item[k + 1]['speed']:
                                                    # print k
                                                    data_item.pop(k)
                                                    duplicate_true = 1
                                        else:
                                            if 'speed' not in data_item[k + 1]:
                                                # print k
                                                data_item.pop(k)
                                                duplicate_true = 1
                    else:
                        if 'sat_cnt' not in data_item[k + 1]:
                            if 'direction' in data_item[k]:
                                if 'direction' in data_item[k + 1]:
                                    if data_item[k]['direction'] == data_item[k + 1]['direction']:
                                        if 'speed' in data_item[k]:
                                            if 'speed' in data_item[k + 1]:
                                                if data_item[k]['speed'] == data_item[k + 1]['speed']:
                                                    # print k
                                                    data_item.pop(k)
                                                    duplicate_true = 1
                                        else:
                                            if 'speed' not in data_item[k + 1]:
                                                # print k
                                                data_item.pop(k)
                                                duplicate_true = 1
                            else:
                                if 'direction' not in data_item[k + 1]:
                                    if 'speed' in data_item[k]:
                                        if 'speed' in data_item[k + 1]:
                                            if data_item[k]['speed'] == data_item[k + 1]['speed']:
                                                # print k
                                                data_item.pop(k)
                                                duplicate_true = 1
                                    else:
                                        if 'speed' not in data_item[k + 1]:
                                            # print k
                                            data_item.pop(k)
                                            duplicate_true = 1
                k = k + 1
        file_name = file_name + "-delete-duplicate"
        obj = open(file_name + ".json", "w")
        obj.write(json.dumps(data_item))
        obj.close
        return file_name

def angle_between_vectors(lat1,lng1,lat2,lng2,lat3,lng3):
    x1 = lng1 * np.pi / 180
    y1 = lat1 * np.pi / 180

    x2 = lng2 * np.pi / 180
    y2 = lat2 * np.pi / 180

    x3 = lng3 * np.pi / 180
    y3 = lat3 * np.pi / 180

    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x3 - x2
    dy2 = y3 - y2

    top = dx1 * dx2 + dy1 * dy2
    bottom1 = np.sqrt(dx1 * dx1 + dy1 * dy1)
    bottom2 = np.sqrt(dx2 * dx2 + dy2 * dy2)
    bottom = bottom1*bottom2
    answer = top/bottom
    rad = np.arccos(answer)
    angle = rad * 180 / np.pi
    return angle

def calculation_of_angles(file_name):
    f = open(file_name + '.txt', 'w')
    length = len(data_item)
    number = 0
    while number < length:
        if number > 1:
            latA = data_item[number]['lat']
            latB = data_item[number - 1]['lat']
            latC = data_item[number - 2]['lat']
            lngA = data_item[number]['lng']
            lngB = data_item[number - 1]['lng']
            lngC = data_item[number - 2]['lng']

            angle2 = angle_between_vectors(latC, lngC, latB, lngB, latA, lngA)

            if math.isnan(angle2) == True:
                val_angle = 1
            else:
                if angle2 > 0:
                     if angle2 < 90:
                         val_angle = 0
                     else:
                         val_angle = 1
                else:
                    val_angle = 1

            f.write(str(val_angle) + '\n')
        number = number + 1
    f.close()
    return file_name + '.txt'

def distance(latA,latB,lngA,lngB):
    dist = 2 * np.arcsin(np.sqrt(np.sin((latB * np.pi / 180 - latA * np.pi / 180) / 2) * np.sin(
        (latB * np.pi / 180 - latA * np.pi / 180) / 2) + np.cos(latA * np.pi / 180) * np.cos(
        latB * np.pi / 180) * np.sin((lngB * np.pi / 180 - lngA * np.pi / 180) / 2) * np.sin(
        (lngB * np.pi / 180 - lngA * np.pi / 180) / 2)))
    distM = dist * 6372795

    return distM

def draw(file_angles):
    f = open(file_angles, 'r')
    lines = f.readlines()
    w = 20
    window = w     #20
    frame = 3       #3
    count_star_behind = window

    counter_node = 0
    for number in range(len(lines) - window):
        counter = 0

        star = 'no'

        for i in range(window):
            if lines[number + i] == "1\n":
                counter = counter + int(lines[number + i])


        if counter > frame:
            star = 'yes'
            count_star_behind = count_star_behind + 1
            if count_star_behind > window:
                count_star_behind = window
            # print ("Window %d, %d bad of %d: star, behind=%d") % (number, counter, window,count_star_behind)
        else:
            star = 'no'
            count_star_behind = count_star_behind - 1
            if count_star_behind < 0:
                count_star_behind = 0
            # print ("Window %d, %d bad of %d: not star, behind=%d") % (number, counter, window,count_star_behind)


        #draw not star
        if star == 'no':
            if count_star_behind > window / 5:
                window = window / 2

            else:
                for j in range(window + 1):
                    G.add_node(number + j, pos=(data_item[number + j]['lng'], data_item[number + j]['lat']))
       #             s[number + j] = 1
                    counter_node = counter_node + 1
                for j in range(window):
                    dist = distance(data_item[number + j]['lat'], data_item[number + j + 1]['lat'],
                                    data_item[number + j]['lng'], data_item[number + j + 1]['lng'])
                    if dist < 300:
                        G.add_edge(number + j, number + j + 1)
                window = w
        else:
            for j in range(window + 1):
                G.add_node(number + j, pos=(data_item[number + j]['lng'], data_item[number + j]['lat']))
   #             s[number + j] = 1
            for j in range(window):
                G.add_edge(number + j, number + j + 1)
            for j in range(window):
                G.remove_edge(number + j, number + j + 1)


            for j in range(window + 1):
                G.remove_node(number + j)
   #             s[number + j] = 0
                #print (number + j - 1)

            window = w
    # print counter_node
    f.close()



if(what_draw == 1):
    make_graph_without_limitation()
else:
    print 'To sorting'
    file_name = sorting(file_name)
    print 'To delete duplicate'
    file_name = delete_duplicate(file_name)
    print 'To calculation of angles'
    file_angles = calculation_of_angles(file_name)

    #rewrite data_item without duplicate
    with open(file_name + '.json') as data_file:
        data_item = json.load(data_file)

    print 'To draw city'
    draw(file_angles)

pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos,node_size=[1])
plt.draw()
plt.show()

