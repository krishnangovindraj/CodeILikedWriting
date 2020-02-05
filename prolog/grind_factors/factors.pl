% This file contains the seed knowledge-base and the rules.
% To grind out all factors, do:
%   consult('grind.pl').
%   grind( div(X,Y,Z), divides(X,Y,Z), PartialLHM). 

divides(2,2,1).
divides(3,3,1).
divides(4,2,2).
divides(5,5,1).
divides(6,2,3).
divides(7,7,1).
divides(8,2,4).
divides(9,3,3).
divides(10,2,5).
divides(11,11,1).
divides(12,2,6).

div(X,Y,Z):-
    divides(X, Z, Y).

    
div(X,Y,Z):-
    divides(X, Y1, Z1),
    divides(Z1, Y, Z2),
    divides(Z, Y1, Z2).
