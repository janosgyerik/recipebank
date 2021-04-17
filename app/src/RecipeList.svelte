<script>
  import Recipe from "./Recipe.svelte";

  export let recipes;
</script>

<main>
  <div class="d-flex flex-wrap justify-content-center">
    {#each recipes as recipe}
      {#if !recipe.hidden}
        <Recipe {recipe} />
      {/if}
    {/each}
  </div>
</main>
