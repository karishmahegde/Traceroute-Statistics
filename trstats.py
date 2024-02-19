'''
====================================================================================================================
Project 1: Using traceroute, parsing its output, and performing a statistical analysis of the traceroute results.
Author: Karishma Hegde 
CSCI 6760 Computer Netwroks | University of Georgia (Spring 2024)
References:
- www.geeksforgeeks.org
- www.w3schools.com
- www.digitalocean.com
- jsonformatter.org/json-parser
- plotly.com/python/box-plots
====================================================================================================================
'''

import argparse
import json
import subprocess
import os
import plotly.express as px
import plotly.graph_objects as go
import plotly.io

def runTraceroute(target, num_runs, run_delay, max_hops):   #run traceroute command
    results = []
    for _ in range(num_runs):
        tracerouteOutput = subprocess.run(
            ['traceroute', '-m', str(max_hops), target],    
            capture_output = True,
            text = True
        ).stdout
        processedResults = processTracerouteVal(tracerouteOutput)   #extract hop data for each traceroute output
        
        results.append(processedResults)
    return results

def processTracerouteVal(tracerouteOutput):     #Parse the traceroute command output with hop, address and latency
    hopStatistics = []
    for line in tracerouteOutput.split('\n'):
        if line.strip() and not line.startswith('traceroute'):
            hopInfo = line.split()
            hopNumber =  str(hopInfo[0])    #checking if the line is hop information or other data
            if (len(hopInfo) >= 4 and hopNumber.isdigit()):
                hopNum = int(hopInfo[0])
                latencyArr = []
                hostsArr = []
                for i in range(1, len(hopInfo) - 1):
                    data = hopInfo[i]
                    if (data.replace('.','').isnumeric() and hopInfo[i+1] == "ms"):
                        latencyArr.append(float(data))
                    elif ("ms" not in data):
                        hostsArr.append(data)
                if len(latencyArr) != 3:
                    while (len(latencyArr) != 3):
                        latencyArr.append(0.0)
                hopStatistics.append({
                    'hop': hopNum,
                    'hosts': hostsArr,
                    'latency': latencyArr
                })
    return hopStatistics

def readTraces(test_dir):   #read traceroute output text file
    results = []
    for filename in os.listdir(test_dir):
        with open(os.path.join(test_dir, filename), 'r') as file:
            tracerouteOutput = file.read()
            parsed_results = processTracerouteVal(tracerouteOutput)
            results.append(parsed_results)
    return results

def computeStatistics(results, maxHops): #calculate min, max, avg and med latencies for each hop
    statistics = []
    groupedData = {} #Dictionary to store grouped data

    #Group data as per hop number
    for sublist in results:
        for entry in sublist:
            hop = entry['hop']
            if hop not in groupedData:
                groupedData[hop] = []
            groupedData[hop].append(entry)

    #Calculate the minimum, maximum, average and medium for each hop in all the runs
    for hopNum in range(1,maxHops+1):
        groupedLatencyArr = []  #Store all the run's latency in an array
        hostsArr = []   #Host address of that hop
        entries = groupedData[hopNum]  # Get entries corresponding to the hop value
        for entry in entries:
            latencyArr = entry['latency']
            hostsArr = entry['hosts']
            for latencyVal in latencyArr:
                groupedLatencyArr.append(latencyVal)

        #calculation and updating JSON object
        hopAvg = round(sum(groupedLatencyArr) / len(groupedLatencyArr),3)
        hopMax = max(groupedLatencyArr)
        hopMed = sorted(groupedLatencyArr)[len(groupedLatencyArr) // 2]
        hopMin = min(groupedLatencyArr)
        statistics.append({ #json obejct
            'avg': hopAvg,
            'hop': hopNum,
            'hosts': hostsArr,
            'max': hopMax,
            'med': hopMed,
            'min': hopMin
        })
    return statistics

def resultJson(results, fileName):
    with open(fileName, 'w') as file:   #open file in write mode and save the JSON
        json.dump(results, file, indent = 4)

def plotFunction(results, fileName, target):
    targetStr = ""
    traces = []
    
    if target is None:
        targetStr = ""
    else:
        targetStr = " ("+target+")"
    
    for entry in results:   #iterate over each hop
        hop = entry["hop"]  #x-axis
        latencyVal = [entry["min"], entry["avg"], entry["med"], entry["max"]]   #y-axis

        trace = go.Box(
            y = latencyVal,
            name = f"hop {hop}",  #legend name
            boxmean = True,  #show mean
            boxpoints = "all", #show all outliers
            jitter = 0.5,  #set jitter
        )
        traces.append(trace)

    layout = go.Layout( #axes and graph labelling
        title = 'Traceroute Latency Distribution per Hop' + targetStr,
        xaxis = dict(
            title = 'Hop Number',   #x-axis label
            tickangle = 90  #rotate the text vertically
        ),
        yaxis = dict(
            title = 'Latency (ms)'  #y-axis label
        ),
    )

    fig = go.Figure(data = traces, layout = layout)
    plotly.io.write_image(fig, fileName, format = 'pdf')    #saving image file to PDF file

def main():
    #pass arguments
    parser = argparse.ArgumentParser(description = 'Traceroute Latency Statistics')
    parser.add_argument('-n', dest = 'num_runs', type = int, default = 1, help = 'Number of times traceroute will run')
    parser.add_argument('-d', dest = 'run_delay', type = int, default = 0, help = 'Number of seconds to wait between two consecutive runs')
    parser.add_argument('-m', dest = 'max_hops', type = int, default = 30, help = 'Number of max hops per traceroute run')
    parser.add_argument('-o', dest = 'output', required = True, help = 'Path and name of output JSON file containing the stats')
    parser.add_argument('-g', dest = 'graph', required = True, help = 'Path and name of output PDF file containing stats graph')
    parser.add_argument('-t', dest = 'target', help = 'A target domain name or IP address')
    parser.add_argument('--test', dest = 'test_dir', help = 'Directory containing pre-generated traceroute output traces')
    args = parser.parse_args()

    if args.test_dir:   #if traceroute output is available, process it
        results = readTraces(args.test_dir)
    else:
        if not args.target:
            parser.error('Target is required if --test is absent')
        results = runTraceroute(args.target, args.num_runs, args.run_delay, args.max_hops)

    statistics = computeStatistics(results, args.max_hops) #compute values for return JSON
    resultJson(statistics, args.output) #store calculated values in JSON
    plotFunction(statistics, args.graph, args.target)    #Plot graph and store in PDF file

if __name__  ==  "__main__":
    main()