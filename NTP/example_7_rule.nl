(('p0', 'X', 'Y'), ('p1', 'X', 'Z'), ('p2', 'Z', 'Y'))
0.23208558559417725	nationality(X,Y) :- hasFather(X,Z), nationality(Z,Y)
0.1063181534409523	nationality(X,Y) :- placeOfBirth(X,Z), locatedIn(Z,Y)

(('p0', 'X', 'Y'), ('p1', 'X', 'Y'))
0.321990430355072	bornIn(X,Y) :- nationality(X,Y)
0.5807282328605652	nationality(X,Y) :- bornIn(X,Y)

