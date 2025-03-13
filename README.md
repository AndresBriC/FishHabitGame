# FishHabitGame
This is a little game I made to motivate me to wake up early (or maybe even to help me build positive habits) :)

## Concept and vision

TL;DR Do good habits, get cool fish.

The general idea is that each day we a group of fish show up, and that's when you'll have an opportunity to grow your collection of fish. By working on positive habits, you'll get rewards that help you build that collection in different ways (either by improving catch rate, upping the chances of finding rare fish and other things I haven't thought about :O), so I'll be leaning on rewarding positive behaviour rather than harshly punishing misses.

I want this to be a very chill experience that takes a small amount of time off your day, but has a big impact. My vision is to have a growing and ever more beautiful collection of fish that reflects your growth though your habits.

Some inspirations for this are: Habitica, Webfishing, Duolingo, Animal Crossing and Pokémon.

## Game loop

This is how I visualize the day to day interaction with the game:

At the start of a new day, new fish show up in your pond and your habits are unticked. At any time, you can tick for completion of a habit, this gives you a random item that helps you with the fishing part of the game.

You can decide to catch the fish whenever you like. When fishing you are presented with all the options for fish, (I will test with showing the fish species or all of them being unknown). Before you fish, you can decide to use any item to help your odds. 

Since fish have a rarity that decides their chance of showing up and and a catch rate that decides the probability of successfuly catching it, the items affect those parts of the experience.

Once you decide to catch one, you'll roll the odds, and if you are successful, you'll add that to your inventory and if it's a new species, it will also be added to you collection (the Pokedex).

## Tech stack

The prototype will be a Discord bot using Python to handle the game and habit tracking logic and PostgreSQL to handle persistent data such as users, inventories, collections, etc.

I was thinking that MongoDB would be a good fit, especially for this phase of development, but I honestly just wanted to learn and practice PostgreSQL :>

I will be using Azure once I mount the project online.

## Prototype scope

For the prototype, I want to test the effectiveness of having a recurring and "tangible" reason to come back to an action on the daily. Also seeing if the idea even works.

_Note that everything here is subject to change since this is a prototype._

The features included are going to be: 
- X number of fish (I'll test with 3 to 5) will be taken from a pool (ha) and shown in the pond every day.
- Being able to fish a certain number of times per day.
- Items for improving catch rates, luring rarer fish and rerolling the pool.
- Registering new habits.
- Reporting success with a habit.
- Penalizing missed habits (I want to handle this with the same philosophy as Duolingo, where ending your streak is the punishment).
- An inventory for your caught fish.
- Your collection. Think of a Pokedex.
- 5 common fish, 3 uncommon, 2 rare and 1 exotic.

## Extended scope

These are features which would be nice to have but represent additional effort and aren't as crucial to the product.

- Economy. Selling fish, buying tank sizes or cosmetics.
- Visualizing your fish rather than them being text in a Discord bot.
    - Procedurally animating the fish. 
- Migrating to a web app or something more accesible.
- Upgrading the pond capacity.
- Having multiple fish tanks and variations of them.
- Making the action of fishing more interactive.
- Doing something exciting with the fish. (Fighting bugs or sth idk).


## References
Turns out my idea isn't that original :0

- https://store.steampowered.com/app/3051380/Lofi_aquarium/
- https://store.steampowered.com/app/2276930/Chillquarium/
- https://store.steampowered.com/app/3146520/WEBFISHING/
- https://habitica.com/static/home
- https://store.steampowered.com/app/3476790/Cozy_Aquarium/
- http://play.google.com/store/apps/details?id=com.superbyte.habitrabbit
- https://play.google.com/store/apps/details?id=co.au.goalhero
- https://play.google.com/store/apps/details?id=com.sixtostart.zombiesrunclient&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1
- https://play.google.com/store/apps/details?id=cc.forestapp&referrer=utm_source%3Dofficalwebsite%26utm_medium%3Dbutton
- https://habitsgarden.com/
- https://play.google.com/store/apps/details?id=seekrtech.sleep

### Why this may work
- https://youtu.be/_tpB-B8BXk0?feature=shared&t=346