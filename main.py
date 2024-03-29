from itertools import permutations
import requests
import creds
import json
import urllib

# ** Below, you will need to paste in the API key you acquire from Distancematrix.ai
API_key = ""


results={}
other=[]
places=[]
name_with_address={}
print("Enter a name for your origin location")
origin=input()
places.append(origin)
print("Enter a name for your destination location")
destination=input()
print("How many places do you have to go for your errands? (Enter a number up to 5)")
num_places=int(input())
for x in range(num_places):
    print("Enter an errand name to add to the list: ")
    new_input=input()
    places.append(new_input)
places.append(destination)
for x,y in enumerate(places):

    print(f"\nEnter the address for {y}")
    print("Paste in the address that's shown on google")
    full_address=input()
    name_with_address[y]=full_address
fill_in="https://api.distancematrix.ai/maps/api/distancematrix/json?origins="

for x,y in enumerate(places):
    if x==0:
        address=name_with_address[y]+", USA|"
    elif x!=0 and x!=(len(places)-1):
        address = name_with_address[y] + ", USA|"
    elif x==(len(places)-1):
        address=name_with_address[y]+",USA"
    fill_in+=address
fill_in+="&destinations="
for x, y in enumerate(places):
    if x == 0:
        address = name_with_address[y] + ", USA|"
    elif x != 0 and x != (len(places) - 1):
        address = name_with_address[y] + ", USA|"
    elif x == (len(places) - 1):
        address = name_with_address[y] + ",USA"
    fill_in += address

fill_in+= "&key=" + API_key
url=fill_in
ok = requests.get(url).json()

u=ok['destination_addresses']
destinations=ok['destination_addresses']
origins = ok['origin_addresses']
pairings={}
other_pairings={}
start=0
for x in destinations:
    pairings[x]=start
    other_pairings[start]=x
    start+=1
nodes={}
rows=ok['rows']
start=0
end=0
for x in rows:
    ok=x['elements']
    end=0
    for o in ok:

        if o['status']=='ZERO_RESULTS':
            distance=0
            duration=0
        else:
            distance=o['distance']['value']
            duration=o['duration']['value']
        sting=f"{start}-{end}"
        nodes[sting]=[distance,duration]
        end+=1
    start+=1
l = list(permutations(range(0, len(destinations))))
min_distance1=10000000000000
min_time1=100000000000000
min_distance2=10000000000000
min_time2=100000000000000
lowest_series1=(0,0,0)
lowest_series2=(0,0,0)
for x in l:
    if x[0]!=0 or x[len(destinations)-1]!=(len(destinations)-1):
        continue
    total_distance=0
    total_time=0
    for index in range(len(x)-1):
        pair=str(x[index])+"-"+str(x[index+1])
        distance_for_pair=nodes[pair][0]
        time_for_pair=nodes[pair][1]
        total_distance+=distance_for_pair
        total_time+=time_for_pair
    if total_distance<min_distance1:
        min_distance1=total_distance
        lowest_series1=x
        min_time1=total_time

    print(total_time)
for x in l:
    if x[0]!=0 or x[len(destinations)-1]!=(len(destinations)-1):
        continue
    total_distance=0
    total_time=0
    for index in range(len(x)-1):
        pair=str(x[index])+"-"+str(x[index+1])

        distance_for_pair=nodes[pair][0]
        time_for_pair = nodes[pair][1]

        total_distance+=distance_for_pair
        total_time += time_for_pair
    if total_time<min_time2:
        min_distance2=total_distance
        lowest_series2=x
        min_time2 = total_time
print()
print("Minimizing Travel Time")
print()
print("Order of places to minimize Travel Time: ")
print()
for x in lowest_series2:
    print(places[x])
print()
print(f"Travel Distance: {min_distance2} meters or {(min_distance2 / 1000):.2f} kilometers")
print(f"Travel Time: {(min_time2/60):.2f} minutes or {(min_time2/3600):.2f} hours")
print()
print()
print("Minimizing Distance")
print()
print("Order of places to minimize Distance Traveled: ")
print()
for x in lowest_series1:
    print(places[x])
print()
print(f"Travel Distance: {min_distance1} meters or {(min_distance1/1000):.2f} kilometers")
print(f"Travel Time: {(min_time1/60):.2f} minutes or {(min_time1/3600):.2f} hours")