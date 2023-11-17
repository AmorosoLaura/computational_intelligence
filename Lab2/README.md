# LAB 2:NIM GAME 
In the Nim game, players take turns removing objects from distinct piles. In each turn, a player can choose to take any number of objects from a single pile. In the misere version of the Nim game,the player who forces their opponent to take the last remaining object loses instead of winning. Players must employ strategic moves to control the state of the piles and ultimately manipulate the game in their favor. Nim is a game of mathematical strategy and can be played with various pile configurations and rule variations.

**Subtraction Game**

A possible modification is to impose a maximum number of objects that can be removed k for each row.

## Collaborations
I worked with Arturo Adelfio (s316716) to implement both the expert agent and the 1+ λ strategy. I then implemented the extended version of the chosen ES, the (μ+λ) Strategy.

## Task2.1

We implemented a strategy for an expert agent by improving the optimal one, since we noticed that in some matches against the pure random, the optimal strategy lost the game. Here an example:

INFO:root:init : <1 3 5 7 9>

INFO:root:ply: player 0 plays Nimply(row=3, num_objects=7)

INFO:root:status: <1 3 5 0 9>

INFO:root:ply: player 1 plays Nimply(row=4, num_objects=8)

INFO:root:status: <1 3 5 0 1>

INFO:root:ply: player 0 plays Nimply(row=2, num_objects=4)

INFO:root:status: <1 3 1 0 1>

INFO:root:ply: player 1 plays Nimply(row=0, num_objects=1)

INFO:root:status: <0 3 1 0 1>

INFO:root:ply: player 0 plays Nimply(row=4, num_objects=1)

INFO:root:status: <0 3 1 0 0>

INFO:root:ply: player 1 plays Nimply(row=1, num_objects=3)

INFO:root:status: <0 0 1 0 0>

INFO:root:ply: player 0 plays Nimply(row=2, num_objects=1)

INFO:root:status: <0 0 0 0 0>

INFO:root:status: Player 1 won!

As it can be noticed, only the rule of the nim sum != 0 brought the player to suboptimal choices in this move:
INFO:root:status: <0 3 1 0 1>

INFO:root:ply: player 0 plays Nimply(row=4, num_objects=1)

INFO:root:status: <0 3 1 0 0>

where he should have left <0 1 1 0 1> instead of INFO:root:status: <0 3 1 0 0>.

We also noticed that playing against an opposite optimal strategy (nim sum = 0) this won even though we made the first move. All this considerations made us implement the expert system.


## Sources
Here some links I used to better understand the problem and its implementation:

- [Nim_rules](https://en.wikipedia.org/wiki/Nim)

- [Scientific_Paper](https://www.researchgate.net/profile/Mihai-Oltean-2/publication/221330080_Evolving_Winning_Strategies_for_Nim-like_Games/links/55dac32508ae9d659491fb60/Evolving-Winning-Strategies-for-Nim-like-Games.pdf?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIn19)


