#FSMD simulator - Ali El-Madani; Yuxuan Zhang; Andy Hansen
import sys
import xmltodict
from helpers import *

#Checking for number of input arguments
if len(sys.argv) < 3:
    print('Too few arguments.')
    sys.exit(-1)
elif (len(sys.argv) >4):
    print('Too many arguments.')
    sys.exit(-1)

maxCycles = int(sys.argv[1])

#Parsing the input files
with open(sys.argv[2]) as fd:
    fsmd_des = xmltodict.parse(fd.read())

fsmd_stim = {}
if len(sys.argv) == 4:
    with open(sys.argv[3]) as fd:
        fsmd_stim = xmltodict.parse(fd.read())


#Initializing the FSMD
states = fsmd_des['fsmddescription']['statelist']['state']
initial_state = fsmd_des['fsmddescription']['initialstate']
inputs = get_inputs(fsmd_des)
variables = get_variables(fsmd_des)
operations = get_operations(fsmd_des)
conditions = get_conditions(fsmd_des)
fsmd = get_FSMD(states, fsmd_des)

#Storing the different parts of the fsmd in a single dictionary
fsmdConf = {"states": states, "state": initial_state, "inputs": inputs,
    "variables": variables, "operations": operations, "conditions": conditions, "fsmd": fsmd}

#Execution loop
run = True
cycle = 0

while (run):
    #Update input based on stimuli
    updateFromStimuli(fsmdConf, fsmd_stim, cycle)
    #Print information
    #Run FSMD
    for transition in fsmdConf['fsmd'][fsmdConf['state']]:
        if evaluate_condition(transition["condition"], fsmdConf):
            print(f"Current State: {fsmdConf['state']}")
            print(f"Current variables: {fsmdConf['variables']}")
            execute_instruction(transition["instruction"], fsmdConf)
            fsmdConf['state'] = transition["nextstate"]
    #Print information

    #Update cycle and check, if FSMD_FINISH has been reached:
    cycle += 1
    run = not(checkEndstate(fsmdConf, fsmd_stim))
    if run:
        run = (cycle < maxCycles)
