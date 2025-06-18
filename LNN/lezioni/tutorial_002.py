import logging
from lnn import (
    Model,
    Predicates,
    Variables,
    Implies,
    Iff,
    Fact,
    World
)

# 1. Configurazione del logger (console + file)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    handlers=[
        logging.FileHandler("model_log.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("==== Inizio creazione del modello LNN ====")

# 2. Inizializzazione del modello e delle variabili FOL
x, y = Variables('x', 'y')
model = Model()
logger.info("Modello LNN creato")

# 3. Definizione dei predicati
Smokes, Cancer = Predicates('Smokes', 'Cancer')   # predicati unari
Friends = Predicates('Friends', arity=2)          # predicato binario
logger.info("Predicati definiti: Smokes, Cancer, Friends")

# 4. Costruzione delle regole logiche (assiomi)
rule1 = Implies(Smokes(x), Cancer(x))                                  # chi fuma -> possibile cancro
rule2 = Implies(Friends(x, y), Iff(Smokes(x), Smokes(y)))              # amici hanno stesso stato di fumo
model.add_knowledge(rule1, rule2, world=World.AXIOM)
logger.info("Assiomi aggiunti al modello (World.AXIOM)")

# 5. Aggiunta di fatti tramite add_data
#    - Alice fuma (TRUE)
#    - Bob è sconosciuto sul fumo (UNKNOWN)
#    - Alice e Bob sono amici (TRUE)
model.add_data({
    Smokes: {
        'Alice': Fact.TRUE,
        'Bob':   Fact.UNKNOWN
    },
    Friends: {
        ('Alice', 'Bob'): Fact.TRUE
    }
})
logger.info("Fatti aggiunti al modello via add_data")

# 6. Esecuzione dell’inferenza
model.infer()
logger.info("Inferenza completata")

# 7. Lettura puntuale di alcuni nodi (usando gli oggetti Formula, non stringhe)
q_alice_cancer = Cancer('Alice')
q_bob_smokes    = Smokes('Bob')
q_bob_cancer    = Cancer('Bob')

alice_cancer_state = model[q_alice_cancer].state
bob_smokes_state   = model[q_bob_smokes].state
bob_cancer_state   = model[q_bob_cancer].state

logger.info(f"Cancer(Alice): {alice_cancer_state}")
logger.info(f"Smokes(Bob):    {bob_smokes_state}")
logger.info(f"Cancer(Bob):    {bob_cancer_state}")

# 8. (Opzionale) Ispezione di tutti i nodi nel modello
logger.info("---- Stato completo dei nodi ----")
for formula_obj, node in model.items():
    logger.info(f"{formula_obj}: state={node.state}")

logger.info("==== Fine script ====")
