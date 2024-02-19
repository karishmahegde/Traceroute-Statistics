# Traceroute Statistics 🌐📈
This project uses traceroute, parses its output, and performs a statistical analysis of the traceroute results.

**Programming Language used: Python 3.11.5**

This project creates a command line tool that automatically executes traceroute multiple times towards a target domain name or IP address specified as command line parameter. Based on multiple traceroute executions, the program will derive latency statistics for each hop between the traceroute client and the target machine.

To allow for repeatable tests, the program also allows reading pre-generated traceroute output traces stored on multiple text files (one text output trace per file). Based on this pre-generated output, the program can compute the latency statistics as for the case of live traceroute execution.

The Python file can be executed with the following command with the below CLI arguments:

```
trstats.py [-h] [-n NUM_RUNS] [-d RUN_DELAY] [-m MAX_HOPS] -o OUTPUT -g GRAPH [-t TARGET] [--test TEST_DIR]
```

| Argument  | Usage |
| ------------- | ------------- |
| -h | --help show this help message and exit |
| -n | NUM_RUNS Number of times traceroute will run |
| -d | RUN_DELAY Number of seconds to wait between two consecutive runs |
| -m | MAX_HOPS Number of max hops per traceroute run |
| -o | OUTPUT Path and name of output JSON file containing the stats |
| -g | GRAPH Path and name of output PDF file containing stats graph |
| -t | TARGET A target domain name or IP address (required if --test is absent) |
| --test | TEST_DIR Directory containing num_runs text files, each of which contains the output of a traceroute run. If present, this will override all other options and traceroute will not be invoked. Stats will be computed over the traceroute output stored in the text files. |

## Output
The main output of the project is a file in JSON format that looks like this example:
```json

[
  {
    "avg": 0.645,
    "hop": 1,
    "hosts": [
      [
        "172.17.0.1",
        "(172.17.0.1)"
      ]
    ],
    "max": 2.441,
    "med": 0.556,
    "min": 0.013
  },
  {
    "avg": 6.386,
    "hop": 2,
    "hosts": [
      [
        "testwifi.here",
        "(192.168.86.1)"
      ]
    ],
    "max": 16.085,
    "med": 5.385,
    "min": 3.108
  },
  {
    "avg": 26.045,
    "hop": 3,
    "hosts": [
      [
        "96.120.4.5",
        "(96.120.4.5)"
      ]
    ],
    "max": 65.753,
    "med": 20.298,
    "min": 12.287
  },
  {
    "avg": 26.819,
    "hop": 4,
    "hosts": [
      [
        "96.110.205.9",
        "(96.110.205.9)"
      ]
    ],
    "max": 65.847,
    "med": 20.51,
    "min": 17.444
  },
  {
    "avg": 168.84,
    "hop": 18,
    "hosts": [
      [
        "124.83.228.222",
        "(124.83.228.222)"
      ]
    ],
    "max": 172.869,
    "med": 166.869,
    "min": 166.781
  }
]
```
(NOTE: avg = average hop latency, max = maximum hop latency, med = median hop latency, min = minimum
hop latency)

The project also gives a boxplot graph showing the latency distribution per each hop, similar to this one:


![Graph Output](https://github.com/karishmahegde/Traceroute-Statistics/blob/main/Outputs/GraphOutput.png?raw=true)

## Execution
If you wish to run my code, run the requirements.txt files first using the below command in your terminal -
```
pip install -r requirements.txt
```
You can then run the Python code _trstats.py_ as follows -
```
python3 trstats.py -n 10 -d 1 -m 10 -o stats.json -g stats_graph.pdf -t www.wikipedia.com
```
Change the arguments as suited.

___
