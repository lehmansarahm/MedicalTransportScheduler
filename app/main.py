import mysql.connector
import numpy as np
import requests
from requests.auth import HTTPDigestAuth
import json

time_range = 30         # range for picking up time, like pick up all from 10:30 to 11:00
time_range_count = 16   # how many time ranges we have in one day
waiting_time = 15       # how much time beforehand patient should arrive
time_limit = 30         # how much longer the picking up route can be than the shortest one
capacity = 4            # basic car capacity

def getDistance(origin, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    key = "AIzaSyDQsoQIu0YpgcyoC_N-X6MdWWmYM36bTts"

    url += "origins=" + origin
    url += "&destinations=" + destination
    url += "&key=" + key
    url = url.replace(" ", "+")
    myResponse = requests.get(url)
    jData = json.loads(myResponse.content)
    return jData['rows'][0]['elements'][0]['distance']['value']

cnx = mysql.connector.connect(user='user', password="password", database='database')
cursor = cnx.cursor()

# query = "SELECT capacity, location FROM cars "
#
# cursor.execute(query)
#
# locations = []
# capacities = []
# cars = []
#
# for (capacity, location) in cursor:
#     locations.append(location)
#     capacities.append(capacity)
#
# for i in range(time_range_count):
#     cars.append(locations)

query = "SELECT start, end, appt FROM trips"

cursor.execute(query)

trips = []

for (start, end, appt) in cursor:
    trips.append([start, end, appt])

timelist = []
# make timelist
current_trips = []

pickups = []
for t in timelist:
    current_trips.clear()
    for trip in trips:
        if t - time_range < trip[2] <= t:
            current_trips.append(trip)

    checked = np.zeros([len(current_trips)])  # checked_current_trips
    p = 0  # current_trips_index //for trip in current_trips

    for trip in current_trips:  # build graph for the next destination
        if checked[p] == 1:
            continue

        vertices = []  # vertices are trips to the same place
        k = 0  # current_destination_index //for st in current_trips
        for st in current_trips:
            if st[1] == trip[1]:
                vertices.append(st)
                checked[k] = 1
            k += 1

        l = len(vertices)  # amount of vertices
        edges = np.zeros([l, l + 1])

        for i in range(l):
            for j in range(l):
                if i != j:
                    edges[i, j] = getDistance(vertices[i][0], vertices[j][0])
            edges[i, l] = getDistance(vertices[i][0], vertices[i][1])

        # generate pickups for all patients to current destination
        picked = np.zeros([l])
        n = 0  # checked vertices count
        while n < l:
            way = []
            cap = capacity  # capacity can be set to particular car but now it considered standard
            i = 0
            # find the furthest patient
            while i < l:
                if picked[i] == 0:
                    max_ind = i
                    max_val = edges[i][l]
                    break
                i += 1
            while i < l:
                if picked[i] == 0 and edges[i, l] > max_val:
                    max_ind = i
                    max_val = edges[i, l]
                    break
                i += 1
            current = max_ind
            picked[max_ind] = 1
            min_len = max_val
            length = 0
            way.append(vertices[max_ind])
            cap -= 1
            n += 1

            # try to pick more patient considering time limit
            while cap > 0 and n < l:
                i = 0
                while i < l:
                    if picked[i] == 0:
                        min_ind = i
                        min_val = edges[current, i] + edges[i, l]
                        break
                    i += 1
                while i < l:
                    if picked[i] == 0 and edges[current, i] + edges[i, l] < min_val:
                        min_ind = i
                        min_val = edges[current, i] + edges[i, l]
                    i += 1
                if length + min_val < min_len + time_limit:
                    picked[min_ind] = 1
                    way.append(vertices[min_ind])
                    length += edges[current, min_ind]
                    current = min_ind
                    cap -= 1
                    n += 1
                else:
                    break

            length = min_len + length + edges[current, l]
            pickups.append({'start_time': t - time_range - waiting_time - length,
                            'route': way, 'arrival_time': t - time_range - waiting_time})

        p += 1
    # checked should be [1, 1, ..., 1]
# timelist end

cursor.close()
cnx.close()

print(pickups)
