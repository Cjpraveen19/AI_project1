def match_recipes(user_ingredients, recipes):
    user_ingredients = {item.strip().lower() for item in user_ingredients}
    results = []

    for recipe in recipes:
        recipe_ingredients = {item.strip().lower() for item in recipe["ingredients"]}

        matched = list(user_ingredients.intersection(recipe_ingredients))
        missing = list(recipe_ingredients - user_ingredients)

        score = len(matched) / len(recipe_ingredients) if recipe_ingredients else 0

        results.append({
            "name": recipe["name"],
            "match_score": round(score, 2),
            "matched_ingredients": matched,
            "missing_ingredients": missing,
            "steps": recipe["steps"]
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results