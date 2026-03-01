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

def show_recipe(request, dish=None):
    """
    Отображение рецепта с возможностью изменения количества порций.
    """
    if dish is None:
        # Если блюдо не указано, выводим список рецептов
        available_recipes = list(DATA.keys())
        return render(request, 'calculator/index.html', {'recipes': available_recipes})
    else:
        # Определяем рецепт
        recipe_data = DATA.get(dish)
        if not recipe_data:
            return render(request, 'calculator/index.html', {'message': f'Рецепт "{dish}" не найден.'})

        # Получаем количество порций из POST или GET
        if request.method == 'POST':
            servings = int(request.POST.get('servings', 1))
        else:
            servings = int(request.GET.get('servings', 1))

        # Масштабируем рецепт на указанное количество порций
        scaled_recipe = {}
        for ingredient, amount in recipe_data.items():
            scaled_recipe[ingredient] = round(amount * servings, 2)

        context = {
            'recipe': scaled_recipe,
            'title': dish.capitalize()
        }
        return render(request, 'calculator/index.html', context)