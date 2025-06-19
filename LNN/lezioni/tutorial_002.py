from configurations_log import logger
from model_setup import (
    model,
    target_formulas
)

found = set()


for node in model.nodes.values():
    print(str(node))
#
# for node in model.nodes.values():
#     formula_str = str(node.formula)
#     if formula_str in target_formulas:
#         logger.info(f"{formula_str} → truth interval = [{node.state.lower:.2f}, {node.state.upper:.2f}]")
#         found.add(formula_str)
#
# missing = target_formulas - found
# for m in missing:
#     logger.warning(f"Formula {m} non trovata nel modello.")
#
# # 8. Stato completo (opzionale): esplorazione di tutti i nodi
# logger.info("---- Stato completo dei nodi ----")
# for node in model.nodes.values():
#     logger.info(f"- {node.formula}: [{node.state.lower:.2f}, {node.state.upper:.2f}]")
#
# logger.info("==== Fine script ====")
