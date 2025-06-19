from lnn import (
    Propositions,
    Fact,
    Predicate,
)

# propositional
P, Q = Propositions("P", "Q")
P.add_data(Fact.TRUE)
Q.add_data((.1, .4))

# first-order logic (FOL)
Person = Predicate("Person")
Person.add_data({
    "Barack Obama": Fact.TRUE,
    "Bo": (.1, .4)
})

# FOL with arity > 2
BD = Predicate("Birthdate", 2)
BD.add_data({
    ("Barack Obama", "04 August 1961"): Fact.TRUE,
    ("Bo", "09 October 2008"): (.6, .75)
})
