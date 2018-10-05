Compiler Principle Project
===============
Mission
----------
* Read in a grammar file (without direct left recursion), construct a LL(1) parsing table and output.
* Read in a grammar file (with direct left recursion), construct a LL(1) parsing table and output.

Analysis
----------
The algorithms to build prediction analysis table is solid and clear as demonstrated in class. The main codes are divided into 3 parts: table construction, calculate FIRST, calculate FOLLOW. Further details are shown in parser.py. As for the second mission, what we need to do is to transform the direct left recursion into two parts(A->βA’ A’->αA’|ε). The details are also shown in parser.py.

The output of first mission will be created in mission1_out.txt, the output of second mission will be created in mission2_out.txt.

* The demonstration grammar files are grammar_noleft.txt and grammar_left.txt separately.

Run
----------
````python
python ./parser.py
````

* Note: I take ‘n’ to substitute the use of ‘ε’ and I use only ‘->’ in mission 1, so ‘|’ may not be useful. Also , some complicated signs may not be distinguished by the parser.py
