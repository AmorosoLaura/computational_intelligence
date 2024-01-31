# Quixo

## Goal

The goal of the project was to provide a player for the Quixo game that is able to win most of the times against a Random player. 

## Collaborations

I worked with Arturo Adelfio.

## Adopted strategies

We implemented some players according to the algorithms learned during the course: in particular, we implemented a Minmax player with the alpha beta pruning and two players trained with the Reinforcement Learning algorithm, a Q learning agent and a Montecarlo Reinforcement Learning agent.

For the Minmax we adopted the alpha beta pruning to reduce the huge search space and we also limited the depth, trying with different values and we ended up in choosing the value of 2.

For the 2 Reinforcement Learning agents we chose to store in the Q Table the state-action values, and to reduce the number of entries we took advantage of the simmetries of the board to transform it in a canonical form and check wheter that state is already in the Q Table.

# References

- https://www.researchgate.net/publication/343390362_Quixo_Is_Solved
- slides of the course