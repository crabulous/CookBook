from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Recipe, RecipeProduct


def add_product_to_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    product_id = request.GET.get('product_id')
    weight = request.GET.get('weight')

    if not (recipe_id and product_id and weight):
        return HttpResponse("Недостаточно параметров", status=400)

    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        product = Product.objects.get(pk=product_id)
        weight = int(weight)
    except (Recipe.DoesNotExist, Product.DoesNotExist, ValueError):
        return HttpResponse("Неверные данные", status=400)

    RecipeProduct.objects.update_or_create(
        recipe=recipe,
        product=product,
        defaults={'weight': weight}
    )
    return HttpResponse("Продукт добавлен в рецепт")


def cook_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    if not recipe_id:
        return HttpResponse("Отсутствует recipe_id", status=400)

    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        for product in recipe.products.all():
            product.times_used += 1
            product.save()
    except Recipe.DoesNotExist:
        return HttpResponse("Рецепт не найден", status=404)

    return HttpResponse("Рецепт приготовлен")


def show_recipes_without_product(request):
    product_id = request.GET.get('product_id')
    if not product_id:
        return HttpResponse("Отсутствует product_id", status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponse("Продукт не найден", status=404)

    recipes = Recipe.objects.exclude(
        recipeproduct__product=product,
        recipeproduct__weight__gte=10
    )
    return render(request, 'recipes_without_product.html', {'recipes': recipes})
