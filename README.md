# ACT Project
A (hastily-written) interpreter for the simple program described in Computability, Complexity and Languages, M. Davis, R. Segal, E. Weyuker, 2nd Edition, taught in Advanced Computability Theory course.

The decoder program simply decodes a list of program codes based on the formula: 

<dl>
<h3 align="center"> 2<sup>x</sup>(2y + 1) = z + 1 </h3>
</dl> 


The interpreter interprets the program line by line and outputs a snapshot every 3 seconds. It makes use of some functions in the decoder, however, due to some technical complexities, they are not directly imported from decoder.py. 
More info in the comments of the .py files. 
Note that this is not a command-line script: You must download it and run it via an IDE. 

Some further objectives for this code: 

* Adding support for running cli-based 

* Writing it wholly in C, or CPP, or cython.
