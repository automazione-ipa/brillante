from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import uuid


class Message(BaseModel):
    """Model representing a Tweet object."""
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    testo: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def get_ingredient_names(self):
        """Method to easily access ingredients by name"""
        return [ingredient.name for ingredient in self.ingredients]


class Ingredient(BaseModel):
    name: str
    quantity: str
    type: str

    @classmethod
    def create_default(cls, name: str):
        """Valori di default per l'ingrediente, nel caso non siano definiti."""
        return cls(name=name, quantity="unknown", type="unknown")


class CocktailRecipe(BaseModel):
    cocktail_name: str
    ingredients: List[Ingredient]
    preparation: str

    @classmethod
    def create_default(cls, cocktail_name: str):
        """Valori di default per gli ingredienti, nel caso la lista sia vuota."""
        return cls(
            cocktail_name=cocktail_name,
            ingredients=[],
            preparation="Preparazione non disponibile"
        )
