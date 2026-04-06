from app.agents.recipe_agent import recipe_agent
from app.agents.kitchen_agent import kitchen_agent


def run_recipe_workflow(user_ingredients, recipes):
    recipe_results = recipe_agent(user_ingredients, recipes)
    kitchen_results = kitchen_agent(recipe_results)

    return {
        "input_ingredients": user_ingredients,
        "best_recipe": kitchen_results["best_recipe"],
        "shopping_list": kitchen_results["shopping_list"],
        "reason": kitchen_results["reason"],
        "other_matches": recipe_results["top_matches"][1:3]
    }