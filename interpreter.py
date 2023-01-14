# done in python 3.9

import time

labels_list = ['A', 'B', 'C', 'D', 'E'] #List of Labels, ordered based on Davis's Book
vars_list = ['X', 'Z'] #List of Variables, Ordered based on Davis's Book

def find_all_vars(list_of_command_codes, count_vars, var_values) -> tuple:

    """

    Input:
            - list_of_command_codes (list, str): a list of codes, each representing a line of program
            - count_vars (int): the number of input variables
            - var_values (list, int): values of inputs, assumed in order (i.e. X1, X2, ...)

    Output:
            - outputs_dict (dict, str:int): variables, (in order, each category sorted based on index)
                                          inputs, locals, output

            - labels_line (dict, str:int): labels and their respective lines, to change the pointer
                                         accordingly.
     
    Note: The variables list consists of inputs from X1 to X{max_x_id} - e. g. if the program includes only
          X1 and X3, and X2 is just given in the inputs, without being mentioned throughout the program,
          X2 is also included in outputs_dict; or if it only includes X3 and X1 and X2 are inputs without
          being mentioned, they are still included in outputs_dict. The same goes for the local variables.

    Function: 
            Passes through the program, and extracts variables and labels. Then assigns each variable
            its respective value (locals and output initiated to zero, inputs being assigned if given)
            and finds the respective lines of the labels, to set the pointer when reaching the conditional
            branches.

    Example:
            Input: [45 34 350 2 46], 2, [2, 1]
            Output: {X1: 2, X2: 1, X3: 0, Z1: 0, Z2: 0, Y: 0}
    """
    
    outputs_dict = {} #contains the variables
    labels_line = {} # labels and their appearance in the lines

    max_x_id = -1 #storing the max id of Xs
    max_z_id = -1 #storing the max id of Zs

    # Setting max ids and labels_line
    for i in range(len(list_of_command_codes)):
        code = list_of_command_codes[i]
        a, _, c = decompose(code) # the operation matters not to us here, hence we discard b with an underline.
        l = ""

        if a != 0: # only add the label if existent, to reduce redunduncy.
            l = label(a)
            labels_line[l] = i + 1

        if c + 1 > 1: # Y is included in the end. 

            if (c + 1) % 2 == 0: # finding the maximum id of X. More on ids in find_var() doc.
                if int((c + 1)/2) > max_x_id:
                    max_x_id = int((c + 1)/2)
            
            else: # finding the maximum id of Z. More on ids in find_var() doc.
                if int((c + 1)/2) > max_z_id:
                    max_z_id = int((c + 1)/2)

    # Traverse the list of Xs, assign values.
    for i in range(1, max_x_id + 1):
        if i <= count_vars: # if mentioned in the inputs...
            outputs_dict[f"X{i}"] = var_values[i - 1]
        else:
            outputs_dict[f"X{i}"] = 0

    # Assigning values to Zs
    for i in range(1, max_z_id + 1):
        outputs_dict[f"Z{i}"] = 0

    outputs_dict["Y"] = 0 # add Y

    return outputs_dict, labels_line


def execute(command_code, pointer, variable_dict, labels_line, program_length) -> tuple:

    """
    Inputs:
            - command_code (int): the code of a line in the program. 
            - pointer (int): # of the line to be executed
            - variable_dict (str:int): a dictionary of variables, to be updated after the execution of the
                           a given command

            - labels_line (str:int): a dictionary of labels and their respective lines,
                                   to decide what to do post-execution of a conditional branch.
            
            - program_length (int): # of program's lines, to determine where to stop execution.

    Outputs:
            - continue_execution (boolean): Whether the program stops after the execution of a given command.
            - no_output (boolean): Kind of a dummy thing, to stop the duplication of the final lines in looping
                                   programs.
            
            - new_pointer (int): the next line that has to be executed.
            - variable_dict (str:int): the updated values of the variables post-execution.

    Function:
            Interprets a line, executes it, sets the next line, updates the variables
            until termination.
    """
    
    # interpret the code: what variable, which operation, ignore its label, find the destination of a 
    # conditional branch.
    variable, operation, _, forward_label = transform_to_executable(command_code)
    new_pointer = -1
    continue_execution = True # by default, the game is on!
    no_output = False # by default, we print the output of the snapshot

    if operation == "+1": # V <- V + 1
        variable_dict[variable] += 1
        if pointer == program_length: 
            # in case it is the final line - plus, I didn't add one to the
            # pointer to make the final snapshot's i = n + 1, per directions by
            # TA. Anyways the final snapshot must have i = n + 1, do please forgive this small bug
            new_pointer = pointer # + 1    
            continue_execution = False 
        else:
            new_pointer = pointer + 1
    
    elif operation == "-1": # V <- V - 1
        if variable_dict[variable] != 0:
            variable_dict[variable] -= 1
        if pointer == program_length: # in case it is the final line
            new_pointer = pointer # + 1
            continue_execution = False
        else:
            new_pointer = pointer + 1

    elif operation == "assign": # V <- V
        if pointer == program_length: # in case it is the final line
            new_pointer = pointer # + 1
            continue_execution = False
        else:
            new_pointer = pointer + 1
    
    else: # IF V != 0 GOTO L
        if forward_label in labels_line.keys():
            if variable_dict[variable] == 0: # if V == 0

                if pointer == program_length: # in case it is the final line
                    new_pointer = program_length
                    continue_execution = False
                    no_output = True # no duplication of the final snapshot

                else:
                    new_pointer = pointer + 1 # Go to the next line

            else:
                new_pointer = labels_line[forward_label] # jump to the destination

        else: # the label is not in the program, i.e. Exit

            if variable_dict[variable] == 0: # in case it is the final line

                if pointer == program_length:
                    new_pointer = program_length
                    continue_execution = False
                    no_output = True

                else:
                    new_pointer = pointer + 1 # Goto the next line

            else:
                new_pointer = labels_line[forward_label] # jump to the destination

    return continue_execution, no_output, new_pointer, variable_dict



def transform_to_executable(command_code) -> tuple:

    """
    Input:
            command_code (int): the code of a line of the program
    Outputs:
            var (str): The variable the command operates on.
            operation (str): The operation done on the operand, that can be:
                                - V += 1
                                - V -= 1
                                - V = V 
                                - conditional branch
            
            l (str): the label of the line
            forward_label (str): The destination label, in case of having a conditional branch.

    Function:
            Receives a line's code and extracts the outputs for use.

    Example:
            Input: 10
            Output: X1, "+1", "A1" , ""(empty string)
    """
    
    a, b, c = decompose(command_code) # <a, <b, c>>

    l, var, operation, forward_label = "", "", "", ""

    # find the instruction's label
    if a != 0:
        l = label(a)
    
    # Find the operand
    var = find_var(c + 1)

    # find the operation
    operation = ""
    if b == 0: # V <- V
        operation = "assign" 

    elif b == 1: # V <- V + 1
        operation = "+1" 
    
    elif b == 2: # V <- V - 1
        operation = "-1" 

    else: # IF V != 0 GOTO L
        forward_label = label(b - 2) 
        operation = "GOTO"
        

    return var, operation, l, forward_label

def decompose(program_code):

    """
    Input (int): program_code - a command's respective code
    Output (string): a structure in the form of <a, <b, c>, which represent label,
            command type and variable, respectively.
    
    Calculates a, b, c based on the pairing function 2^x(2y + 1) = z + 1 

    Example:
            input: 21
            output: 1, 1, 1 (<1, <1, 1>>)
    """

    a, b, c = 0, 0, 0 #<a, <b, c>>
    
    # Extracting a and <b, c>
    temp_code = program_code + 1
    twos = 0
    T = 0 # <b, c>
    while temp_code % 2 == 0:
        twos += 1
        temp_code = int(temp_code/2)

    a = twos
    twos = 0
    T = int((temp_code - 1)/2)

    # Extracting b and c
    T += 1
    while T % 2 == 0:
        twos += 1
        T = int(T/2)

    b = twos
    c = int((T - 1)/2)

    return a, b, c

def label(n):

    """
    Input (int): Receives a label's place in their ordering
    Output (string): The Label
    
    Based on s1 ch4 of the book. The labels can be ordered like below:
        A1 B1 C1 D1 E1
        A2 B2 C2 D2 E2
        A3 B3 C3 D3 E3
              .
              .
              .

    As they have a one-to-one relation to the natural numbers, the above ordering
    becomes as follows:
        1 2 3 4 5
        6 7 8 9 10
        11 12 13 14 15
              .
              .
              .

    Paying attention, we can notice a pattern:
        i) Indices of A_i % 5 = 1
        ii) Indices of B_i % 5 = 2
        iii) Indices of C_i % 5 = 3
        iv) Indices of D_i % 5 = 4
        v) Indices of E_i % 5 = 0
    
    Using the above knowledge, we can find the correct label.

    Example:
            Input: 1
            Output: A1
    """
    if n % 5 == 0:
        return f"E{int(n/5)}"

    else:
        num_label = int(n/5) + 1
        alph_label = labels_list[int(n%5) - 1]
        return f"{alph_label}{num_label}"

def find_var(n):

    """
    Input (int): A variable's place in their ordering
    Output (string): The variable

    Based on Davis s1 ch4. The variables can be ordered like below:

            Y
        X1      Z1
        X2      Z2
        X3      Z3
            .
            .
            .
            .

    As they have a one-to-one relation to the natural numbers, we can write:

            1
        2       3
        4       5
        6       7
            .
            .
            .

    The pattern is obvious: Indices of X_i is even, and Z_i's are odd.

    Example:
            Input: 1
            Output: 'Y'

            Input: 2
            Output: X1

            Input: 3
            Output: Z1
    """

    if n == 1:
        return 'Y'
    else:
        return f"{vars_list[int(n%2)]}{int(n/2)}"

##############################MAIN SECTION##############################

program_lines = list(map(int, input().split()))
inputs = list(map(int, input().split()))

variables_dict, labels_line = find_all_vars(program_lines, len(inputs), inputs) # find variables and labels

pointer = 1 # go to the first line

# print the names of the vars in a line with the inital pointer: i [X_i] [Z_i] Y (i = 1, 2, ...)
print("i", end=" ")
var_line = " ".join(variables_dict.keys())
print(var_line)
print("-"*(len(var_line) + 3)) # for more beauty :)

# print the init state
print(pointer, end=" ")
print(" ".join(map(str, variables_dict.values())))

while(True): # Execute till die!
    continue_execution, no_output, new_pointer, variables_dict = execute(program_lines[pointer - 1], pointer, variables_dict, labels_line, len(program_lines))
    pointer = new_pointer
    time.sleep(3) # added a timer so that the infinite output is easier to see.
    if no_output == False: # avoid duplication
        print(pointer, end=" ")
        print(" ".join(map(str, variables_dict.values())))
    if continue_execution == False:
        break