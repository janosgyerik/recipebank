<script>
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  import AutoComplete from "simple-svelte-autocomplete";

  export let ingredients;
  export let recipeFilter;

  const dispatch = createEventDispatcher();

  let addIngredientInput;
  let selectedIngredient;

  function onIngredientSelected() {
    if (selectedIngredient === undefined) {
      return;
    }

    dispatch("ingredientSelected", selectedIngredient);

    // workaround to (addIngredientInput.value = "") not working when executed without delay
    setTimeout(() => (addIngredientInput.value = ""), 10);
    setTimeout(() => (addIngredientInput.value = ""), 100);
  }

  function onClearFilters() {
    dispatch("clearFilters");

    addIngredientInput.focus();
    addIngredientInput.value = "";
  }

  function onRemoveIngredient(ingredient) {
    dispatch("removeIngredient", ingredient);

    addIngredientInput.focus();
  }

  onMount(() => {
    addIngredientInput = document.getElementById("addIngredientInput");
    addIngredientInput.focus();
  });
</script>

<main>
  <div class="card recipe-filter">
    <div class="card-body">
      {#if recipeFilter.ingredients.length > 0}
        <ul class="list-group" style="margin: 1em 0">
          {#each recipeFilter.ingredients as ingredient}
            <li class="list-group-item py-1 justify-content-between d-flex">
              {ingredient.search_key}
              <button
                on:click|preventDefault={onRemoveIngredient.bind(this, ingredient)}
                class="btn btn-sm pull-right"
                data-ingredient={ingredient.id}>&#10006;</button
              >
            </li>
          {/each}
        </ul>
      {/if}

      <AutoComplete
        inputId="addIngredientInput"
        items={ingredients}
        keywordsFieldName="search"
        labelFieldName="search"
        bind:selectedItem={selectedIngredient}
        placeholder="add ingredient"
        noResultsText="Not a known ingredient, sorry!"
        maxItemsToShowInList="10"
        onChange={onIngredientSelected}
      />
    </div>
  </div>
</main>

<style>
  .card {
    margin: 1em;
  }
</style>
