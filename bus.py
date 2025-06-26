import requests
import os

culo = 'y'

RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

casa = '8591346'
eth_z = '8591123'
eth_h = '8591122'
HB = '8503000'
oerlikon = '8503006'

def get_location(name):

    name = name.replace(' ', '\ ')
    request = requests.get(f'http://transport.opendata.ch/v1/locations?query={name}').json()['stations']
    result = []
    for i in request:
        tmp = [i['name'],i['id']]
        result.append(tmp)
    return result

def get_connection(dep, arr, time = None):
    request = requests.get(f'http://transport.opendata.ch/v1/connections?from={dep}&to={arr}').json()['connections']
    connections = []
    for i in request:

        sections = i['sections']
        means, depName, depTime, depDelay, arrName, arrTime = [[] for _ in range(6)]
        for j in sections:
            if j['journey']:
                means.append(j['journey']['category']+j['journey']['number']+' '+j['journey']['to'])
                depName.append(j['departure']['station']['name'])
                depTime.append(j['departure']['departure'])
                depDelay.append(j['departure']['delay'])
                arrName.append(j['arrival']['station']['name'])
                arrTime.append(j['arrival']['arrival'])

        connections.append([means, depName, depTime, depDelay, arrName, arrTime])

    return connections


def main():

    print(f'''
          ~ manual mode ~
          ''')

    departure = input('Search a departure station: \n')
    departure = get_location(departure)

    for i in range(len(departure)):
        print(f'({i+1})' + ' ' + departure[i][0])

    index = 0 
    while index not in [f'{i+1}' for i in range(len(departure))]:
        index = input(f'Select the correct station: (1-{len(departure)}) \n')

    departure = departure[int(index)-1]



    arrival = input('Search a destination: \n')
    arrival = get_location(arrival)

    for i in range(len(arrival)):
        print(f'({i+1})' + ' ' + arrival[i][0])

    index = 0
    while index not in [f'{i+1}' for i in range(len(arrival))]:
        index = input(f'Select the correct station: (1-{len(arrival)}) \n')

    arrival = arrival[int(index)-1]

    print(f'''
          {departure[0]} ---> {arrival[0]}
          ''')

    display_connection(departure[1], arrival[1])

def display_connection(departure, arrival):


    connections = get_connection(departure, arrival)

    for connection in connections:

        means, depName, depTime, depDelay, arrName, arrTime = connection
        journey = ''

        for i in range(len(means)):
            depTime[i] = depTime[i][11:-8] + f'{RED} +{depDelay[i]}{NC}' if f'{depDelay[i]}' not in ['0', 'None'] else depTime[i][11:-8]
            arrow = f'  --{BLUE}{means[i]}{NC}-->  {arrTime[i][11:-8]} | ' if i != len(means)-1 else f'  --{BLUE}{means[i]}{NC}-->  {arrName[i]} | {arrTime[i][11:-8]}'
            journey += depTime[i] + ' | ' + depName[i] + arrow if i == 0 else depName[i] + ' | ' + depTime[i] + arrow

        os.system(f'echo "{journey} \n"')


def mode():

    mode = int(input('enter mode (1 or 2): \n'))
    if mode == 1:
        print(f'''
              ~ easy mode ~
              Select your connection: (1-8)
              (1) casa -> hoengg
              (2) hoengg -> casa
              (3) casa -> zentrum
              (4) zentrum -> casa
              (5) casa -> HB
              (6) HB -> casa
              (7) casa -> oerlikon
              (8) oerlikon -> casa


              ''')
        connection_index = int(input()) - 1
        connections_list = [[casa, eth_h], [casa, eth_z], [casa, HB], [casa, oerlikon]]
        connection = connections_list[connection_index//2]
        departure = connection[int(connection_index % 2 == 1)]
        arrival = connection[int(connection_index % 2 == 0)]
        display_connection(departure, arrival)
    elif mode == 2:
        main()

while culo == 'y':

    mode()
    culo = input('Check new connection? [y/N]')
    while culo not in ['y', 'N', '']:
        culo = input('Check new connection? [y/N]')



