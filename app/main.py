from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path
import json

from app.orchestrator import run_recipe_workflow


app = FastAPI(title="Leftover Chef API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
RECIPES_FILE = BASE_DIR / "data" / "recipes.json"


class IngredientInput(BaseModel):
    ingredients: List[str]


def load_recipes():
    if not RECIPES_FILE.exists():
        raise FileNotFoundError(f"recipes.json not found at: {RECIPES_FILE}")

    with open(RECIPES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/")
def home():
    return {"message": "Leftover Chef is running 🚀"}


@app.get("/recipes")
def get_recipes():
    return load_recipes()


@app.get("/recommend")
def recommend(ingredients: str):
    user_ingredients = [
        item.strip().lower()
        for item in ingredients.split(",")
        if item.strip()
    ]

    recipes = load_recipes()

    return run_recipe_workflow(user_ingredients, recipes)


@app.post("/recommend")
def recommend_post(data: IngredientInput):
    user_ingredients = [
        item.strip().lower()
        for item in data.ingredients
        if item.strip()
    ]

    recipes = load_recipes()

    return run_recipe_workflow(user_ingredients, recipes)


@app.get("/recommend-text-simple", response_class=PlainTextResponse)
def recommend_text_simple(ingredients: str):
    user_ingredients = [
        item.strip().lower()
        for item in ingredients.split(",")
        if item.strip()
    ]

    recipes = load_recipes()

    result = run_recipe_workflow(user_ingredients, recipes)

    best_recipe = result.get("best_recipe")

    if not best_recipe:
        return "❌ No good recipe found."

    steps_text = "\n".join(
        [f"{i + 1}. {step}" for i, step in enumerate(best_recipe.get("steps", []))]
    )

    matched_ingredients = best_recipe.get("matched_ingredients", [])
    shopping_list = result.get("shopping_list", [])

    response_text = f"""
🍽️ Recommended Recipe: {best_recipe.get('name', 'Unknown Recipe')}

🧠 Reason:
{result.get('reason', 'No reason provided.')}

⭐ Match Score: {best_recipe.get('match_score', 'N/A')}

✅ Ingredients you have:
{", ".join(matched_ingredients) if matched_ingredients else "None"}

🛒 Missing Ingredients:
{", ".join(shopping_list) if shopping_list else "None"}

👨‍🍳 Steps:
{steps_text if steps_text else "No steps available."}
""".strip()

    return response_text