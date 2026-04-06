from fastapi import FastAPI
import json
from pathlib import Path
from app.orchestrator import run_recipe_workflow
from pydantic import BaseModel
from typing import List
from fastapi.responses import PlainTextResponse

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
RECIPES_FILE = BASE_DIR / "data" / "recipes.json"


@app.get("/")
def home():
    return {"message": "Leftover Chef is running 🚀"}


@app.get("/recipes")
def get_recipes():
    with open(RECIPES_FILE, "r", encoding="utf-8") as file:
        recipes = json.load(file)
    return recipes


@app.get("/recommend")
def recommend(ingredients: str):
    user_ingredients = [item.strip() for item in ingredients.split(",")]

    with open(RECIPES_FILE, "r", encoding="utf-8") as file:
        recipes = json.load(file)

    return run_recipe_workflow(user_ingredients, recipes)


class IngredientInput(BaseModel):
    ingredients: List[str]


@app.post("/recommend")
def recommend_post(data: IngredientInput):
    user_ingredients = data.ingredients

    with open(RECIPES_FILE, "r", encoding="utf-8") as file:
        recipes = json.load(file)

    return run_recipe_workflow(user_ingredients, recipes)

@app.get("/recommend-text-simple")
def recommend_text_simple(ingredients: str):
    user_ingredients = [item.strip() for item in ingredients.split(",")]

    with open(RECIPES_FILE, "r", encoding="utf-8") as file:
        recipes = json.load(file)

    result = run_recipe_workflow(user_ingredients, recipes)

    best_recipe = result.get("best_recipe")

    if not best_recipe:
        return "❌ No good recipe found."

    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(best_recipe["steps"])])

    response_text = f"""
🍽️ Recommended Recipe: {best_recipe['name']}

🧠 Reason:
{result['reason']}

⭐ Match Score: {best_recipe['match_score']}
🔥 Difficulty: {result.get('difficulty', 'unknown')}
⏱️ Estimated Time: {result.get('estimated_time', 'unknown')}

✅ Ingredients you have:
{", ".join(best_recipe['matched_ingredients'])}

🛒 Missing Ingredients:
{", ".join(result['shopping_list']) if result['shopping_list'] else "None"}

👨‍🍳 Steps:
{steps_text}

📁 Tool:
{result.get('tool_action', 'No tool used')}
""".strip()

    return PlainTextResponse(response_text)