from app.utils.matcher import match_recipes


def recipe_agent(user_ingredients, recipes):
    matched_recipes = match_recipes(user_ingredients, recipes)
    return {
        "top_matches": matched_recipes[:3]
    }