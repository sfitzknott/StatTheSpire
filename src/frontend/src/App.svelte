<script lang="ts">
	export let name: string;
	export let runs: string = '{}';


  async function hello() {
	const killed_by = "Gremlin Nob";
	const gold = 323;
	const ascension_level = 20;
	const character = "SILENT";
	const chose_seed = false;
	const master_deck = {'$all': [ 'Deadly Poison', 'Strike_G']}

	const res = await fetch('http://127.0.0.1:5000/runs', {
			method: 'POST',
			headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
			body: JSON.stringify({
				killed_by,
				//gold,
				ascension_level,
				character,
				chose_seed,
				//master_deck
			})
		})
		
		const json = await res.json()
		runs = JSON.stringify(json, null, 2)
	
  }
</script>

<main>
	<h1>Hello {name}!</h1>
	<button on:click={hello}> weee</button>
	<p>{runs}</p>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>