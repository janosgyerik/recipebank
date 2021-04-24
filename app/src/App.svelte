<script>
  import {
    recipes as rawRecipes,
    ingredients as rawIngredients,
  } from "./recipes.json";

  import RecipeFilter from "./RecipeFilter.svelte";
  import RecipeList from "./RecipeList.svelte";

  import { onMount } from "svelte";

  let recipes = rawRecipes;
  const ingredients = rawIngredients;
  const ingredientsIndex = {};

  for (let ingredient of ingredients) {
    if (ingredient.subtype) {
      ingredient.search = `${ingredient.name} (${ingredient.subtype})`;
    } else {
      ingredient.search = ingredient.name;
    }

    ingredientsIndex[ingredient.id] = ingredient;
  }

  class RecipeFilterModel {
    constructor() {
      this.ingredients = [];
    }

    addIngredient(ingredient) {
      this.ingredients.push(ingredient);
    }

    removeIngredient(ingredientToRemove) {
      const filteredIngredients = [];
      for (let ingredient of this.ingredients) {
        if (ingredient !== ingredientToRemove) {
          filteredIngredients.push(ingredient);
        }
      }
      this.ingredients = filteredIngredients;
    }

    clear() {
      this.ingredients = [];
    }

    isEmpty() {
      return this.ingredients.length == 0;
    }
  }

  const recipeFilter = new RecipeFilterModel();
  // recipeFilter.addIngredient(ingredients[0]);
  // recipeFilter.addIngredient(ingredients[1]);

  function onIngredientSelected(event) {
    const selectedIngredient = event.detail;
    recipeFilter.addIngredient(selectedIngredient);
    recipeFilter = recipeFilter;
    updateRecipeList();
  }

  function onRemoveIngredient(event) {
    const selectedIngredient = event.detail;
    recipeFilter.removeIngredient(selectedIngredient);
    recipeFilter = recipeFilter;
    updateRecipeList();
  }

  function onClearFilters(event) {
    recipeFilter.clear();
    recipeFilter = recipeFilter;
    updateRecipeList();
  }

  function updateRecipeList() {
    let intersection = recipeFilter.isEmpty()
      ? new Set()
      : new Set(recipeFilter.ingredients[0].recipe_refs);

    for (let i = 1; i < recipeFilter.ingredients.length; i++) {
      intersection = new Set(
        [...recipeFilter.ingredients[i].recipe_refs].filter((x) =>
          intersection.has(x)
        )
      );
    }

    for (let recipe of recipes) {
      recipe.hidden = !intersection.has(recipe.id);
    }

    // trigger reactive update
    recipes = recipes;
  }

  function randomRecipeList() {
    let indexes = [];
    for (let index = 0; index < recipes.length; index++) {
      indexes.push(index);
    }
    // inefficient and biased, but simple and good enough for our purposes
    indexes.sort(() => 0.5 - Math.random());

    let selected = new Set(indexes.slice(0, 10));

    for (let index = 0; index < recipes.length; index++) {
      recipes[index].hidden = !selected.has(index);
    }

    // trigger reactive update
    recipes = recipes;
  }

  onMount(randomRecipeList);
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
  />
  <style>
    body {
      background: url("images/bg.png");
      background-size: cover;
      background-repeat: no-repeat;
      background-attachment: fixed;
      background-position: center center;
    }
  </style>
</svelte:head>

<main>
  <div class="d-flex justify-content-center">
    <RecipeFilter
      {ingredients}
      {recipeFilter}
      on:ingredientSelected={onIngredientSelected}
      on:removeIngredient={onRemoveIngredient}
      on:clearFilters={onClearFilters}
    />
  </div>

  <RecipeList {recipes} />
</main>
