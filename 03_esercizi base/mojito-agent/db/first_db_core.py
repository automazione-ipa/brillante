from db_core import DBCore

db = DBCore()

rum_id = db.save_ingredient("rum bianco", {"type": "alcoholic"})
gin_id = db.save_ingredient("gin", {"type": "alcoholic"})
limone_id = db.save_ingredient("limone", {"type": "fruit"})

# Aggiungi ricetta
recipe_id = db.save_cocktail_recipe(
    "mojito",
    [rum_id, limone_id],  # Ingredienti referenziati tramite gli ID
    "Pestare menta e zucchero, aggiungere rum e succo di limone, mescolare con ghiaccio e completare con acqua gassata."
)

# Recupera la ricetta
recipe = db.get_cocktail_recipe("mojito")
print(recipe)
