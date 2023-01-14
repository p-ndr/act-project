#done in python 3.9

labels_list = ['A', 'B', 'C', 'D', 'E'] #List of Labels, ordered based on Davis's Book
vars_list = ['X', 'Z'] #List of Variables, Ordered based on Davis's Book

def decode(program_code):

    """
    Input (int): program_code - a command's respective code
    Output (string): The command's form in Davis's language

    Receives a command's respective code, and transforms it to a command of strings.

    Example:
            input: 21
            output: [A1] X1 <- X1 + 1
    """

    a, b, c = decompose(program_code)

    command = transform_to_command(a, b, c)

    return command

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

def transform_to_command(a, b, c):

    """
    Inputs (int): a, b, c, three integers representing label, command type and variable, respectively
    Output (string): The rescpective instruction in the form of Davis's language

    Gets a, b, c and transforms them to the instruction they code, based on the algorithm in s1 ch4 of Davis.

    Example:
            input: 1, 1, 1
            output: [A1] X1 <- X1 + 1
    """

    l, var, command = "", "", ""
    if a != 0:
        l = label(a)
    
    var = find_var(c + 1)

    command = ""
    if b == 0:
        if a == 0:
            command = f"{var} <- {var}"
        else:
            command = f"[{l}] {var} <- {var}"

    elif b == 1:
        if a == 0:
            command = f"{var} <- {var} + 1"
        else:
            command = f"[{l}] {var} <- {var} + 1"
    
    elif b == 2:
        if a == 0:
            command = f"{var} <- {var} - 1"
        else:
            command = f"[{l}] {var} <- {var} - 1"

    else:
        forward_label = label(b - 2) 
        if a == 0:
            command = f"IF {var} != 0 GOTO {forward_label}"
        else:
            command = f"[{l}] IF {var} != 0 GOTO {forward_label}"

    return command

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

########################## THE MAIN SECTION ###############################

codes = list(map(int, input().split()))

for code in codes:
    print(decode(code))