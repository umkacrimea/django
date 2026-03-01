from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def show_recipe(request, dish):
    """
    Отображает рецепт блюда с учётом количества порций.
    :param request: HTTP-запрос
    :param dish: Название блюда (например, omlet, pasta)
    :return: Рендер страницы с рецептом
    """
    recipe_data = DATA.get(dish)
    if not recipe_data:
        return render(request, 'calculator/error.html', {'message': f'Рецепт {dish} не найден'})

    # Получаем количество порций из GET-параметра
    servings = int(request.GET.get('servings', 1))

    # Умножаем ингредиенты на количество порций
    scaled_recipe = {}
    for ingredient, amount in recipe_data.items():
        scaled_recipe[ingredient] = round(amount * servings, 2)

    context = {
        'recipe': scaled_recipe,
        'title': dish.capitalize(),
    }
    return render(request, 'calculator/index.html', context)


def homepage_view(request):
    message = "Выберите рецепт блюда:"
    available_recipes = list(DATA.keys())  # Список доступных рецептов
    return render(request, 'calculator/index.html', {'message': message, 'recipes': available_recipes})
