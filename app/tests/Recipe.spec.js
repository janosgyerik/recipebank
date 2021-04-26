// see a bit more details on https://timdeschryver.dev/blog/how-to-test-svelte-components
import Recipe from '../src/Recipe.svelte'
import { render } from '@testing-library/svelte'

it('it works', async () => {
  const { getByTestId } = render(Recipe, {
    recipe: {
      ingredients: [],
      source_name: 'Foo',
      page_num: 123,
    },
  })

  const footer = getByTestId('footer')

  expect(footer.textContent).toBe('Foo (page 123)')
})
