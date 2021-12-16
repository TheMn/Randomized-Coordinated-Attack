"""
    COORDINATED ATTACK ~~~ RANDOMIZED VERSION
    @author: TheMn
"""
import random
import networkx as nx
import matplotlib.pyplot as plt

# g = nx.Graph()
# for i in range(5):
#     for j in range(5):
#         if i != j:
#             g.add_edge(i, j)
# c = [['green', 'red'][random.randint(0, 1)] for i in range(5)]
# nx.draw(g, nodelist=g.nodes(), node_color=c, with_labels=True)
# plt.show()

def random_attack(number_of_processes, r):
    values_choice = [1] # 1/2 chance of 0 decision
    links_choice = [1 for _ in range(5-1)] + [0] # 1/r chance of fail
    
    # -------------------------------| Initialization |-------------------------------
    round = [0]*number_of_processes
    decision = [None]*number_of_processes
    key = None

    val = []
    level = []
    for i in range(number_of_processes):
        val.append([random.choice(values_choice) if i==j else None for j in range(number_of_processes)])
        level.append([0 if i==j else -1 for j in range(number_of_processes)])
    # colors = ['green' if val[i][i] else 'red' for i in range(number_of_processes)]

    # -------------------------------| Random Attack Algorithm |-------------------------------
    key = random.randint(1, r-1)
    has_key = [True] + [False for _ in range(1, number_of_processes)]

    new_key = has_key
    new_val = val
    new_level = level
    while None in decision:
        # print(round[0])
        links = [[random.choice(links_choice) for _ in range(number_of_processes)] for _ in range(number_of_processes)]

        for i in range(number_of_processes): # sender 
            round[i] += 1
            for j in range(number_of_processes): # receiver
                if links[i][j]:
                    if has_key[i]:
                        new_key[j] = True
                    if i != j:
                        for k in range(number_of_processes):
                            if val[i][k] is not None:
                                new_val[j][k] = val[i][k]
                            if level[i][k] > new_level[j][k]:
                                new_level[j][k] = level[i][k]
                    new_level[j][j] = 1 + min([level[j][t] for t in range(number_of_processes) if t != j])
            if round[i] == r:
                if has_key[i] and level[i][i] > key and (not 0 in val[i]):
                    decision[i] = 1
                else:
                    decision[i] = 0
        has_key = new_key # to feel like a synchronous system
        val = new_val
        level = new_level
    # print("-------------------------------|", decision, "|-------------------------------")
    return not(0 in decision)

agreement = []
for R in range(2, 21):
    count = [0, 0]
    for i in range(1000):
        count[random_attack(number_of_processes=10, r=R)] += 1
    agreement.append(count[1])

# count = [0, 0]
# for i in range(1000):
#     count[random_attack(number_of_processes=5, r=10)] += 1
# plt.pie(count,
#         labels=['zero', 'one'],
#         explode=[0.2, 0], 
#         autopct='%1.1f%%', 
#         colors=['red', 'green'])

one_per_r = [(1-1/x)*(1000) for x in range(2, 21)]

plt.plot([i for i in range(2, 21)], agreement, c='green')
plt.plot([i for i in range(2, 21)], one_per_r, c='blue')
plt.xlabel("r")
plt.ylabel("agreement")
plt.show()

# g = nx.Graph()
# for i in range(number_of_processes):
#     for j in range(number_of_processes):
#         if links[i][j] and i != j:
#             g.add_edge(i, j)

# nx.draw(g, nodelist=g.nodes(), node_color=colors, with_labels=True)
# plt.show()

# r=20, n=5