def kitchen_agent(recipe_results):
    top_matches = recipe_results.get("top_matches", [])

    if not top_matches:
        return {
            "best_recipe": None,
            "shopping_list": [],
            "reason": "No recipes found.",
            "difficulty": "unknown",
            "estimated_time": "unknown"
        }

    best_recipe = top_matches[0]

    # Estimate difficulty
    steps_count = len(best_recipe["steps"])
    if steps_count <= 3:
        difficulty = "easy"
    elif steps_count <= 5:
        difficulty = "medium"
    else:
        difficulty = "hard"

    # Estimate cooking time
    estimated_time = f"{steps_count * 5} minutes"

    # Smart explanation
    reason = (
        f"This recipe is the best match because {len(best_recipe['matched_ingredients'])} "
        f"out of {len(best_recipe['matched_ingredients']) + len(best_recipe['missing_ingredients'])} "
        f"ingredients are already available."
    )

    return {
        "best_recipe": best_recipe,
        "shopping_list": best_recipe["missing_ingredients"],
        "reason": reason,
        "difficulty": difficulty,
        "estimated_time": estimated_time
    }