import logging
from lnn import (
    Model,
    Predicates,
    Variables,
    Implies,
    Iff,
    World
)

# Configurazione del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Dynamic LNN Models: empty container populated on-demand with the knowledge and data required to compute over
# Discoverable information that requires reasoning over the new information while simultaneously retaining previously stored or inferred facts.
# Model knowledge and facts can be initiated with model constructors or populated with content on-demand
logger.info("Inizio creazione del modello LNN")
model = Model()

x, y = Variables('x', 'y')

Smokes, Cancer = Predicates('Smokes', 'Cancer')
Friends = Predicates('Friends', arity=2)

logger.info("Predicati definiti: Smokes, Cancer, Friends")

Smoking_causes_Cancer = Implies(Smokes(x), Cancer(x))
Smokers_befriend_Smokers = Implies(Friends(x, y), Iff(Smokes(x), Smokes(y)))

logger.info("Formule logiche costruite")

formulae = [
    Smoking_causes_Cancer,
    Smokers_befriend_Smokers
]

model.add_knowledge(*formulae, world=World.AXIOM)
logger.info("Formule aggiunte al modello")

logger.info("Modello pronto")
