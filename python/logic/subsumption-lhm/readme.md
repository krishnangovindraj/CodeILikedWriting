## What it does.
(Tries to) Use the [subtle](https://dtai.cs.kuleuven.be/software/subtle/) theta-subsumption engine to construct the LHM (Least Herbrand Model) of the knowledgebase. (Whether that achieves that or not will only become clear when I test this more.)

Since subtle is a prolog program, pyswip is used to interface with swi-prolog and run subtle. 

Internally, the problog.logic module of the [problog python library](https://problog.readthedocs.io/en/latest/python.html) is used for representation, but no functionality of problog is used. 

## Files
`factors.bg` is the knowledge base in a prolog format.
`test_lhm.py` is a driver program to demonstrate
`ts_lhm.py` contains ThetaSubsumptionLHM - the class which constructs the LHM.

## Illustrative example
We explore the `divides/3` relation. `divides(X,Y,Z)` means Y divides X (perfectly) and Z is the quotient.
`factors.bg` contains two forms of the `divides/3` predicate.
1. For each natural number from 2 to 12, exactly one fact `divides/3` per number.
2. Two rules `div(X,Y,Z)` by which all `divides/3` can be derived for the known numbers.
