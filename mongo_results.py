from mongo_handler import MongoHandler

def calculate_statistics():
    mongo_handler = MongoHandler()

    # Aggregation pipeline to calculate average ingredients and stages
    pipeline = [
        {
            "$group": {
                "_id": None,
                "avg_ingredients": {"$avg": {"$size": {"$ifNull": ["$რეცეპტის ინგრედიენტები", []]}}},
                "avg_stages": {"$avg": {"$size": {"$ifNull": ["$რეცეპტის მომზადების ეტაპები", []]}}}
            }
        }
    ]

    # Execute the aggregation pipeline
    stats = list(mongo_handler.collection.aggregate(pipeline))
    avg_ingredients = stats[0]["avg_ingredients"] if stats else 0
    avg_stages = stats[0]["avg_stages"] if stats else 0

    # Find the recipe with the most servings
    most_servings_recipe = mongo_handler.collection.find_one(
        {"ულუფების რაოდენობა": {"$exists": True}},
        sort=[("ულუფების რაოდენობა", -1)]
    )

    # Find the author with the most recipes
    author_stats = mongo_handler.collection.aggregate([
        {"$group": {"_id": "$ავტორი სახელი", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ])

    author_result = next(author_stats, None)
    most_recipes_author = author_result["_id"] if author_result else None
    most_recipes_count = author_result["count"] if author_result else 0

    # Print the results
    print(f"ინგრედიენტების საშუალო რაოდენობა: {avg_ingredients:.2f}")
    print(f"მომზადების ეტაპების საშუალო რაოდენობა: {avg_stages:.2f}")

    if most_servings_recipe:
        print(f"რეცეპტი ყველაზე მეტი რაოცენობის ულუფით: {most_servings_recipe['რეცეპტის დასახელება']} "
              f"({most_servings_recipe['რეცეპტის მისამართი']})")

    if most_recipes_author:
        print(f"ყველაზე მეტი რეცეპტის ავტორი: {most_recipes_author} {most_recipes_count} რეცეპტით")

if __name__ == "__main__":
    calculate_statistics()



