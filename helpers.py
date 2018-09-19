#Helper functions
import sys
import xmltodict

#Function: Get inputs
def get_inputs(fsmd_des):
    inputs = {}

    if(fsmd_des['fsmddescription']['inputlist'] is None):
        inputs = {}
        #No elements
    else:
        if type(fsmd_des['fsmddescription']['inputlist']['input']) is str:
            # One element
            inputs[fsmd_des['fsmddescription']['inputlist']['input']] = 0
        else:
            # More elements
            for input_i in fsmd_des['fsmddescription']['inputlist']['input']:
                inputs[input_i] = 0

    return inputs

#Function: Get variables
def get_variables(fsmd_des):
    variables = {}

    if(fsmd_des['fsmddescription']['variablelist'] is None):
        variables = {}
        #No elements
    else:
        if type(fsmd_des['fsmddescription']['variablelist']['variable']) is str:
            # One element
            variables[fsmd_des['fsmddescription']['variablelist']['variable']] = 0
        else:
            # More elements
            for variable in fsmd_des['fsmddescription']['variablelist']['variable']:
                variables[variable] = 0

    return variables

#Function: Get operations
def get_operations(fsmd_des):
    operations = {}

    if(fsmd_des['fsmddescription']['operationlist'] is None):
        operations = {}
        #No elements
    else:
        for operation in fsmd_des['fsmddescription']['operationlist']['operation']:
            if type(operation) is str:
                # Only one element
                operations[fsmd_des['fsmddescription']['operationlist']['operation']['name']] = \
                    fsmd_des['fsmddescription']['operationlist']['operation']['expression']
                break
            else:
                # More than 1 element
                operations[operation['name']] = operation['expression']

    return operations

#Function: Get conditions
def get_conditions(fsmd_des):
    conditions = {}

    if(fsmd_des['fsmddescription']['conditionlist'] is None):
        conditions = {}
        #No elements
    else:
        for condition in fsmd_des['fsmddescription']['conditionlist']['condition']:
            if type(condition) is str:
                #Only one element
                conditions[fsmd_des['fsmddescription']['conditionlist']['condition']['name']] = fsmd_des['fsmddescription']['conditionlist']['condition']['expression']
                break
            else:
                #More than 1 element
                conditions[condition['name']] = condition['expression']

    return conditions

#Function: Initialize FSMD
def get_FSMD(states, fsmd_des):
    fsmd = {}

    for state in states:
        fsmd[state] = []
        for transition in fsmd_des['fsmddescription']['fsmd'][state]['transition']:
            if type(transition) is str:
                #Only one element
                fsmd[state].append({'condition': fsmd_des['fsmddescription']['fsmd'][state]['transition']['condition'],
                                    'instruction': fsmd_des['fsmddescription']['fsmd'][state]['transition']['instruction'],
                                    'nextstate': fsmd_des['fsmddescription']['fsmd'][state]['transition']['nextstate']})
                break
            else:
                #More than 1 element
                fsmd[state].append({'condition' : transition['condition'],
                                    'instruction' : transition['instruction'],
                                    'nextstate' : transition['nextstate']})

    return fsmd


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionary 'inputs'
#
def execute_setinput(operation, inputs):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    inputs[target] = eval(expression, {'__builtins__': None}, inputs)
    return


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionaries 'variables' and 'inputs'
#
def execute_operation(operation, fsmdConf):
    operation_clean = fsmdConf['operations'][operation].replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    fsmdConf['variables'][target] = eval(expression, {'__builtins__': None}, merge_dicts(fsmdConf['variables'], fsmdConf['inputs']))
    return


#
# Description:
# This function executes a list of operations passed as string and spaced by
# a single space using the expression defined in the dictionary 'operations'
#
def execute_instruction(instruction, fsmdConf):
    if instruction == 'NOP' or instruction == 'nop':
        return
    instruction_split = instruction.split(' ')
    for operation in instruction_split:
        execute_operation(operation, fsmdConf)
    return


#
# Description:
# This function evaluates a Python compatible boolean expressions of
# conditions passed as string using the conditions defined in the variable 'conditions'
# and using the operands stored in the dictionaries 'variables' and 'inputs
# It returns True or False
#
def evaluate_condition(condition, fsmdConf):
    if condition == 'True' or condition =='true' or condition == 1:
        return True
    if condition == 'False' or condition =='false' or condition == 0:
        return False
    condition_explicit = condition
    for element in fsmdConf['conditions']:
        condition_explicit = condition_explicit.replace(element, fsmdConf['conditions'][element])
    #print('----' + condition_explicit)
    return eval(condition_explicit, {'__builtins__': None}, merge_dicts(fsmdConf['variables'], fsmdConf['inputs']))


#
# Description:
# Support function to merge two dictionaries.
#
def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


#Function: updateFromStimuli
def updateFromStimuli(fsmdConf, fsmd_stim, cycle):
    try:
        if (not(fsmd_stim['fsmdstimulus']['setinput'] is None)):
            for setinput in fsmd_stim['fsmdstimulus']['setinput']:
                if type(setinput) is str:
                    #Only one element
                    if int(fsmd_stim['fsmdstimulus']['setinput']['cycle']) == cycle:
                        execute_setinput(fsmd_stim['fsmdstimulus']['setinput']['expression'], fsmdConf['inputs'])
                    break
                else:
                    #More than 1 element
                    if int(setinput['cycle']) == cycle:
                        execute_setinput(setinput['expression'], fsmdConf['inputs'])
    except:
        pass

#Function: checkEndstate
def checkEndstate(fsmdConf, fsmd_stim):
    try:
        if (not(fsmd_stim['fsmdstimulus']['endstate'] is None)):
            if state == fsmd_stim['fsmdstimulus']['endstate']:
                return True
                #print('End-state reached.')
                repeat = False
            else:
                return False
    except:
        return False
        pass
