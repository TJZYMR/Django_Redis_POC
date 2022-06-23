import django
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, View
from .models import *
from django.core.cache import cache

# Create your views here.
class RecipesView(ListView):
    queryset = Recipe.objects.all()
    context_object_name = "recipes"
    template_name = "recipes/recipes.html"


class RecipeView(View):
    template_name = "recipes/recipe.html"

    def get(self, request, *args, **kwargs):
        recipe_id = kwargs.get("pk")
        if cache.get(recipe_id):
            recipe = cache.get(recipe_id)
            print("Cache hit")
        else:
            try:
                recipe = Recipe.objects.get(id=recipe_id)
                cache.set(recipe_id, recipe)
                print("DB hit")
            except Recipe.DoesNotExist:
                return HttpResponse("Recipe not found")

        context = {
            "recipe": recipe,
        }
        return render(request, self.template_name, context)
