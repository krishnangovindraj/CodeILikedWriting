## What it does.
Given 2 predicates representing a relation -
1. Ground_Form: A few seed facts of the relation,
2. Query_Form : A rule by which more true instances of the relation can be derived.

`grind/2` produces (and asserts) all ground facts entailed by the seed facts and the relation.
`grind/3` calls `grind/2`, then returns the list of all ground facts of interest.

Hence, it derives the LHM of the relation, assuming it is the only predicates which exists.

## Illustrative example
`factors.pl` contains: 
1. For each natural number from 2 to 12, exactly one fact `divisible/3` per number.
divisible(X,Y,Z) means Y divides X (perfectly) and Z is the quotient.
2. A rule `div(X,Y,Z)` by which all `divisible/3` can be derived.


### Command: 
`grind(div(X,Y,Z), divisible(X,Y,Z), PartialLHM).`