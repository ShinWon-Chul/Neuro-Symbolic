(('p0', 'X', 'Y'), ('p1', 'X', 'Z'), ('p2', 'Z', 'Y'))
0.35085255	nationality(X,Y) :- hasFather(X,Z), nationality(Z,Y)
0.17050996	nationality(X,Y) :- placeOfBirth(X,Z), locatedIn(Z,Y)

(('p0', 'X', 'Y'), ('p1', 'X', 'Y'))
0.29969117	nationality(X,Y) :- nationality(X,Y)
0.03153399	nationality(X,Y) :- nationality(X,Y)

