from configurations_log import logger
from lnn import (
    Fact,
    Model,
    Predicates,
    Variables,
    Implies,
    Iff,
    World
)


logger.info("==== Inizio creazione del modello LNN ====")
# 1. Dynamic LNN Model
# Note: it's an empty container populated on-demand with the knowledge and data required to compute over
# Discoverable information that requires reasoning over the new information while simultaneously retaining previously stored or inferred facts.
# Model knowledge and facts can be initiated with model constructors or populated with content on-demand
model = Model()

# 2. Variabili FOL
x, y = Variables('x', 'y')

# 3. Predicati
Smokes, Cancer = Predicates('Smokes', 'Cancer')  # unari
Friends = Predicates('Friends', arity=2)  # binario

logger.info("Predicati definiti: Smokes, Cancer, Friends")

# 4. Regole logiche (assiomi)
Smoking_causes_Cancer = Implies(Smokes(x), Cancer(x))
Smokers_befriend_Smokers = Implies(Friends(x, y), Iff(Smokes(x), Smokes(y)))

formulae = [
    Smoking_causes_Cancer,
    Smokers_befriend_Smokers
]

logger.info("Formule logiche costruite")

# 5. add_knowledge()
model.add_knowledge(*formulae, world=World.AXIOM)

logger.info("Assiomi aggiunti al modello (World.AXIOM)")
logger.info("Prima parte del modello pronta.")

# 6. Define facts
#    - Alice fuma (TRUE)
#    - Bob è sconosciuto sul fumo (UNKNOWN)
#    - Alice e Bob sono amici (TRUE)
fact_1 = {
    Smokes: {
        'Alice': Fact.TRUE,
        'Bob': Fact.UNKNOWN
    }
}

fact_2 = {
    Friends: {
        ('Alice', 'Bob'): Fact.TRUE
    }
}

facts = {**fact_1, **fact_2}

target_formulas = {
    "Cancer(Alice)",
    "Smokes(Bob)",
    "Cancer(Bob)"
}

model.add_data(facts)

logger.info("Fatti aggiunti al modello via add_data")
# 6. Inferenza
model.infer()
logger.info("Inferenza completata")
