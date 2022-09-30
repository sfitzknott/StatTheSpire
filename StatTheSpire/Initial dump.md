## StatTheSpire
### What
- An analysis tool for Slay The Spire
- Insights on Win%, cards/relics/potions, etc.
- It will have a GUI
- Possible silly ML expansion?

### Why
 - Because I like Slay The Spire and want to be able to interact with this information
 - It sounds fun

### How
- STS runs are saved in a .run file, which is JSON
- This can be read in and aggregated as required for desired results
- Because the project will have a GUI, I will need to decide on how to present the information
- Driven by the statistical component of the project, I plan on using Python because I have experience with basic ML and data processing libraries in it.
- With the backend being Python-based, I will probably use Flask as I have some experience with it. Django is an alternative however I have not used it before and don't want to overload on the new information required.
- Using Flask and data-handling libraries in Python will allow for easy handling and serving of the aggregated run data.
- For the UI, I would like to use Sveltekit. I haven't used it before but it is interesting and it would be a good opportunity to learn it. It seems more straightforward than other TS/JS frameworks.

