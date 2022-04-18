# Goal Selection Strategies for Learning Goal-Oriented Value Functions

**Degree:** COMS

**Description:** Recent work in compositional reinforcement learning has demonstrated how to
combine skills to solve tasks specified using Boolean algebra operators. However, the algorithm
to do so uses standard Q-learning with epsilon greedy exploration. One aspect of the algorithm
is the way the agent decides on which goal to explore, which is currently done in a greedy
fashion. In this project, we propose extending this algorithm to **incorporate different ways of goal
selection**, such as through uniform random or bandit-based strategies. This project also involves
the creation of a virtual environment in Unity or mujoco-worldgen.

**Tags/topics:** Reinforcement learning, deep reinforcement learning, game design

**Algorithms:**
- Explore only
- Exploit only
- ε-greedy (Epsilon greedy)
- UCB (Upper Confidence Bound)
- EXP4
- Softmax
- Optimistic initialization
- Intrisic rewards
- Q-map

**References:** 
1. [Benureau, Fabien, and Pierre-Yves Oudeyer. "Diversity-driven selection of exploration strategies in multi-armed bandits." In 2015 Joint IEEE International Conference on Development and Learning and Epigenetic Robotics (ICDL-EpiRob), pp. 135-142. IEEE, 2015.](https://ieeexplore.ieee.org/abstract/document/7346130)
1. [Tasse, Geraud Nangue, Steven James, and Benjamin Rosman. A Boolean Task Algebra for Reinforcement Learning. Neurips 2020.](https://proceedings.neurips.cc/paper/2020/hash/6ba3af5d7b2790e73f0de32e5c8c1798-Abstract.html)
1. [Pardo, Fabio, Vitaly Levdik, and Petar Kormushev. "Q-map: a convolutional approach for goal-oriented reinforcement learning." (2018).](https://openreview.net/forum?id=rye7XnRqFm)
1. [H. Shi, Z. Lin, K. Hwang, S. Yang and J. Chen, "An Adaptive Strategy Selection Method With Reinforcement Learning for Robotic Soccer Games," in IEEE Access, vol. 6, pp. 8376-8386, 2018](https://ieeexplore.ieee.org/abstract/document/8301430)
1. [Sutton, Richard S., and Andrew G. Barto. Reinforcement learning: An introduction. MIT press, 2018.](https://books.google.com/books?hl=en&lr=&id=uWV0DwAAQBAJ&oi=fnd&pg=PR7&dq=+Reinforcement+learning:+An+introduction&ots=mirNs6X4i8&sig=Gh6KgbbNms8_OGtnKEmgvRtExck)
1. [Zhang, Taidong, Xianze Li, Xudong Li, Guanghui Liu, and Miao Tian. "Reinforcement Learning based Strategy Selection in StarCraft: Brood War." In Proceedings of the 2020 Artificial Intelligence and Complex Systems Conference, pp. 121-128. 2020.](https://dl.acm.org/doi/abs/10.1145/3407703.3407726?casa_token=wnvoVjGBR6EAAAAA:J1RzGZWcNtLMg7t25rBOZsYbiGEDENwPq30zBMBLeoKoLxDwMk3EIa5Kc6EY846-UMK_sWeS87h0)