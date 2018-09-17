# FSMD simulator - Ali El-Madani; Yuxuan Zhang; Andy Hansen
import sys
import xmltodict
from helpers import *

# Checking for number of input arguments
if len(sys.argv) < 3:
    print('Too few arguments.')
    sys.exit(-1)
elif (len(sys.argv) > 4):
    print('Too many arguments.')
    sys.exit(-1)

maxCycles = int(sys.argv[1])

# Parsing the input files
with open(sys.argv[2]) as fd:
    fsmd_des = xmltodict.parse(fd.read())

fsmd_stim = {}
if len(sys.argv) == 4:
    with open(sys.argv[3]) as fd:
        fsmd_stim = xmltodict.parse(fd.read())


# Initializing states
states = fsmd_des['fsmddescription']['statelist']['state']
initial_state = fsmd_des['fsmddescription']['initialstate']

inputs = get_inputs(fsmd_des)
variables = get_variables(fsmd_des)
operations = get_operations(fsmd_des)
conditions = get_conditions(fsmd_des)

fsmd = get_FSMD(states, fsmd_des)


# Execution loop
run = True
cycle = 0
state = initial_state

# while (run):
#     # Update input based on stimuli
#     # Print information
#     # Do FSMD thing and somehow update state
#     # Print information
#
#     # Update cycle and check, if FSMD_FINISH has been reached:
#     cycles += 1
#     run = not(checkEndstate())
#     if run:
#         run = (cycles < maxCycles)


while True:
    if state == "DONE":
        break
    for transition in fsmd[state]:
        if evaluate_condition(transition["condition"]):
            print(f"Current State: {state}")
            print(f"Current variables: {variables}")
            print("Transitioning:")
            execute_instruction(transition["instruction"])
            state = transition["nextstate"]

            print(f"Next State: {state}")
            print(f"Variable: {variables}")
            print("----------------------------")
