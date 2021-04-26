<script>
  export let recipe;
</script>

<main>
  <div class="card recipe">
    <div class="card-header bg-info text-white">{recipe.name}<br/><small>({recipe.category})</small></div>
    <!-- <div style="text-align: center">
      <img class="card-img-top" src="images/nosmoothie.jpeg" alt="smoothie" style="width: 10rem; display: inline">
    </div> -->
    <div class="card-body">
      <ul>
        {#each recipe.ingredients as ingredient}
          <li>{ingredient.search_key}</li>
        {/each}
      </ul>
    </div>
    <div class="card-header">{recipe.source_name} (page {recipe.page_num})</div>
  </div>
</main>

<style>
  .card {
    margin: 1em;
  }
</style>
