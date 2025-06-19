from configurations_log import logger
from model_setup import (
    Cancer,
    model,
    fact_1,
    fact_2,
    Smokes,
)

model.add_data({**fact_1, **fact_2})

logger.info("Fatti aggiunti al modello via add_data")
# 6. Inferenza
model.infer()
logger.info("Inferenza completata")

# 7. Lettura puntuale dei risultati
#    Usa sempre oggetti Formula, non stringhe
alice_cancer = Cancer('Alice')
bob_smokes = Smokes('Bob')
bob_cancer = Cancer('Bob')

logger.info(f"Cancer(Alice) state = {model[alice_cancer].state}")
logger.info(f"Smokes(Bob)    state = {model[bob_smokes].state}")
logger.info(f"Cancer(Bob)    state = {model[bob_cancer].state}")

# 8. Stato completo (opzionale)
logger.info("---- Stato completo dei nodi ----")
for formula_obj, node in model.items():
    logger.info(f"{formula_obj}: state={node.state}")

logger.info("==== Fine script ====")
