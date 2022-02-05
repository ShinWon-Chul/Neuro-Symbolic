(('p0', 'X', 'Y'), ('p1', 'X', 'Z'), ('p2', 'Z', 'Y'))
0.23208559	nationality(X,Y) :- hasFather(X,Z), nationality(Z,Y)
0.10631815	nationality(X,Y) :- placeOfBirth(X,Z), locatedIn(Z,Y)

(('p0', 'X', 'Y'), ('p1', 'X', 'Y'))
0.58072823	nationality(X,Y) :- bornIn(X,Y)
0.32199043	bornIn(X,Y) :- nationality(X,Y)

