(('p0', 'X', 'Y'), ('p1', 'X', 'Z'), ('p2', 'Z', 'Y'))
0.3508525490760803	nationality(X,Y) :- hasFather(X,Z), nationality(Z,Y)
0.1705099642276764	nationality(X,Y) :- placeOfBirth(X,Z), locatedIn(Z,Y)

(('p0', 'X', 'Y'), ('p1', 'X', 'Y'))
0.29969117045402527	nationality(X,Y) :- nationality(X,Y)
0.03153398633003235	nationality(X,Y) :- nationality(X,Y)

