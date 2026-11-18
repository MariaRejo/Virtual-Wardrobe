def suggest_outfit(weather, items):
    recommendations = []
    for item in items:
        # Abstract-la sonna logic: Veyil-na tops, kuliru-na jacket
        if weather == "Hot" and item.category == "tops":
            recommendations.append(item)
        elif weather == "Cold" and "jacket" in item.category.lower():
            recommendations.append(item)
    
    # Top 3 suggestions mattum tharuvom
    return recommendations[:3]