from time import *
import json
import os
import random
import argparse

path = '/home/user/Documents/infoIsFun/time_tracker/'

def status_reset():
    with open(path + "rsc/status_file.txt", 'w') as file:
        file.write('')
    return

def trackings_reset():
    with open(path + "rsc/time_tracked.json", 'w') as file:
        file.write('')
    return

def start(topic):
    startTime = time()
    file = open(path + "rsc/status_file.txt", "w")
    file.write(topic + '|' + str(startTime))
    return

def get_status():
    with open(path + "rsc/status_file.txt", 'r') as file:
        status = file.read()
        return status != ''

def stop(): #ONLY CALL STOP IF 'status_file' IS NON EMPTY
    endTime = time()
    with open(path + "rsc/status_file.txt", 'r') as file:
        status = file.read()
        assert(status != '')
        topic, startTime = status.split('|')
    startTime = float(startTime)
    timeInterval = [startTime, endTime]
    add_tracking(topic, timeInterval)
    return

def add_tracking(topic, timeInterval):
    #read existing trackings
    with open(path + "rsc/time_tracked.json", "r") as trackingFile:
        trackings = trackingFile.read()
        trackingTime = json.loads(trackings) if trackings !='' else {}

    if topic in trackingTime:
        trackingTime[topic].append(timeInterval)
    else:
        trackingTime[topic] = [timeInterval]
    #write new tracking by updating or creating a record
    with open(path + "rsc/time_tracked.json", "w") as trackingFile:
        trackingFile.write(json.dumps(trackingTime, indent=4))
    #reset the status_file
    status_reset()
    return 

def get_total_time(topic):
    #read existing trackings
    with open(path + "rsc/time_tracked.json", "r") as trackingFile:
        trackings = trackingFile.read()
        trackingTime = json.loads(trackings) if trackings !='' else {}

    total_time = 0
    if topic in trackingTime:
        for interval in trackingTime[topic]:
            total_time += interval[1]-interval[0]
    return total_time

def sec_to_hours(time):

    hours = time // 3600
    mins = time%3600 // 60
    secs = time%3600%60

    return [int(hours), int(mins), int(secs)]

def graph(topic, x='x'):
    
    with open(path + "rsc/time_tracked.json", "r") as trackingFile:
        trackings = trackingFile.read()
        trackingTime = json.loads(trackings) if trackings !='' else {}
    if topic in trackingTime:
        topic_intervals = {}
        for interval in trackingTime[topic]:
            day = asctime(localtime(interval[0])).split(' ')
            day.pop(3)
            day = ' '.join(day)
            if not topic_intervals.get(day):
                trace = ['' for _ in range(24)]
            else:
                trace = topic_intervals[day]
            for i in range(localtime(interval[0])[3], localtime(interval[1])[3]):
                trace[i] = x
            topic_intervals[day] = trace

        return topic_intervals
    else:
        print('topic does not exist...')
        return

def merge_graphs(dict_graph_list):
    
    complete_graph = {}
    for key in {k: v for d in dict_graph_list for k, v in d.items()}.keys():
        graph_list = []
        for graph in dict_graph_list:
            if graph.get(key):
                graph_list.append(graph[key])
        complete_graph[key] = merge_schedule(graph_list)
    return complete_graph

            
def merge_schedule(graph_list):
    merged_graph = []
    for i in range(len(graph_list[0])):
        res = ''
        for graph in graph_list:
            res += graph[i]
        merged_graph.append(res)
    return merged_graph

def main():
    parser = argparse.ArgumentParser(
        description="Time tracking CLI tool"
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # start [topic]
    start_parser = subparsers.add_parser('start', help='Start tracking a topic')
    start_parser.add_argument('topic', help='The topic to start tracking')

    # stop
    subparsers.add_parser('stop', help='Stop the current tracking')

    # records
    subparsers.add_parser('records', help='Show all tracking records')

    # time [topic]
    time_parser = subparsers.add_parser('time', help='Show total time for a topic')
    time_parser.add_argument('topic', help='The topic to summarize time for')

    # graph [all/topic]
    graph_parser = subparsers.add_parser('graph', help='Show schedule as a graph')
    graph_parser.add_argument('target', help='"all" or a specific topic')

    # reset
    subparsers.add_parser('reset', help='Reset all tracking data (irreversible!)')

    args = parser.parse_args()

    if args.command == 'start':
        if not get_status():
            start(args.topic)
            print(f'Time tracking started for {args.topic}')
        else:
            print(f'A job is running already!')

    elif args.command == 'stop':
        if get_status():
            stop()
            print(f'The active time tracking was stopped.')
        else:
            print('No running jobs.')

    elif args.command == 'records':
        os.system('cat /home/user/Documents/infoIsFun/time_tracker/rsc/time_tracked.json && echo \n')

    elif args.command == 'time':
        total_time = get_total_time(args.topic)
        if total_time:
            h, m, s = sec_to_hours(total_time)
            print(f'Total time tracked for {args.topic}: {h}h {m}m {s}s')
        else:
            print(f'No trackings for {args.topic}')

    elif args.command == 'graph':
        if args.target == 'all':
            dict_graph_list = []
            char_list = ['x', 'o', '#', '@', '¬', chr(92), '-']
            legend = []

            with open("/home/user/Documents/infoIsFun/time_tracker/rsc/time_tracked.json", "r") as trackingFile:
                trackings = trackingFile.read()
                trackingTime = json.loads(trackings) if trackings else {}

                for topic in trackingTime:
                    x = char_list.pop(random.randint(0, len(char_list)-1))
                    legend.append(f'{x} = {topic}')
                    dict_graph_list.append(graph(topic, x))

            complete_graph = merge_graphs(dict_graph_list)

            headers = " " * 15 + ''.join(key + " " * 5 for key in complete_graph)
            print(headers)

            for i in range(24):
                line = f'{i:2d}' + " " * 21
                for value in complete_graph.values():
                    line += value[i] + " " * 19
                print(line)

            print("\n" + " " * 10 + "Here is the legend:")
            for item in legend:
                print(" " * 10 + item)

        else:
            topic = args.target
            print(graph(topic))

    elif args.command == 'reset':
        confirm = input('This action is irreversible. Are you sure? [y/N] ')
        if confirm.lower() == 'y':
            status_reset()
            trackings_reset()
            print("All records have been reset.")
        else:
            print("Reset cancelled.")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()

