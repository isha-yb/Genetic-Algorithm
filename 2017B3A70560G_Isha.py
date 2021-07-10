import random
import matplotlib.pyplot as plt
import pandas as pd
import math

distances = []

def queens_fitness(queens):
	attacking = 0
	for i in range(8):
		for j in range(i+1, 8):
			# rows and diagonals
			if (queens[i] == queens[j]):
				attacking += 1
			elif (abs(queens[i]-queens[j]) == abs(i-j)):
				attacking += 1
	non_attacking = 28 - attacking
	return 1 + non_attacking

def get_item(population):
	item_list = []
	for x in population:
		item_list.append(x[1])
	return item_list

def get_weights(population):
	weight_list = []
	for x in population:
		weight_list.append(x[0])
	return weight_list

def queens_reproduce(parents):
	c = random.randint(1, 7)
	new_children = []
	new_children.append(parents[0][:c] + parents[1][c:])
	new_children.append(parents[1][:c] + parents[0][c:])
	return new_children

def queens_mutate(child):
	position = random.randint(0,7)
	value = child[position]
	new_value = value
	while(new_value == value):
		new_value = random.randint(0,7)
	child[position] = new_value
	return child

def tsp_fitness(tsp):
	path_cost = 0
	for i in range(13):
		city_1 = tsp[i]
		city_2 = tsp[i+1]
		d = distances[city_1][city_2] 
		path_cost += d
	path_cost += distances[tsp[13]][tsp[0]]
	return (1/path_cost)*1400000

def tsp_reproduce(parents):
	set_copied_1 = set()
	set_copied_2 = set()
	s = random.randint(0, 13)
	e = random.randint(0, 13)
	if (s > e):
		s, e = e, s
	new_child_1 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
	new_child_2 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
	for i in range(s, e+1):
		new_child_1[i] = parents[0][i]
		set_copied_1.add(new_child_1[i])
		new_child_2[i] = parents[1][i]
		set_copied_2.add(new_child_2[i])

	index=0
	for i in range(0, 14):
		if parents[1][i] in set_copied_1:
			continue
		while (s <= index and index <= e):
			index += 1
		new_child_1[index] = parents[1][i]
		index += 1

	index=0
	for i in range(0, 14):
		if parents[0][i] in set_copied_2:
			continue
		while (s <= index and index <= e):
			index += 1
		new_child_2[index] = parents[0][i]
		index += 1
	return [new_child_1, new_child_2]

def tsp_mutate(child):
	pos_1 = random.randint(0, 13)
	pos_2 = pos_1
	while(pos_2 == pos_1):
		pos_2 = random.randint(0, 13)
	child[pos_1], child[pos_2] = child[pos_2], child[pos_1]
	return child

def GA_Queens():
	queens = [1, 1, 1, 1, 1, 1, 1, 1]
	population = []
	for i in range(50):
		population.append( (queens_fitness(queens), queens) )

	for gen in range(10000):
		new_population = []
		for j in range(50):
			parents = random.choices(get_item(population), get_weights(population), k = 2)
			child = queens_reproduce(parents)
			child_1 = child[0]
			child_2 = child[1]
			prob_1 = child_1[0]
			prob_2 = child_2[0]

			if(prob_1 < 25):
				child_1 = queens_mutate(child[0])
			if(prob_2 < 25):
				child_2 = queens_mutate(child[1])
			new_population.append( (queens_fitness(child_1), child_1) )
			new_population.append( (queens_fitness(child_2), child_2) )
		new_population.sort()
		new_population.reverse()
		population = new_population[:50]
		print("=== Generation: %d , Best fitness value: %d === " % (gen, new_population[0][0]))
	
		if(population[0][0] >28):
			break
	print("Best solution: ", population[0][1], " with fitness: ", population[0][0])
	
def GA_TSP():
	
	for i in range(14):
		d = []
		for j in range(14):
			d.append(100000)
		distances.append(d)
	for i in range(14):
		distances[i][i] = 0

	distances[0][6]=0.15*1000
	distances[0][9]=0.2*1000
	distances[0][11]=0.12*1000

	distances[1][7]=0.19*1000
	distances[1][8]=0.4*1000
	distances[1][13]=0.13*1000

	distances[2][3] = 0.6*1000
	distances[2][4] = 0.22*1000
	distances[2][5] = 0.4*1000
	distances[2][8] = 0.2*1000

	distances[3][2] = 0.6*1000
	distances[3][5] = 0.21*1000
	distances[3][10] = 0.3*1000

	distances[4][2] = 0.22*1000
	distances[4][8] = 0.18*1000

	distances[5][2] = 0.4*1000
	distances[5][3] = 0.21*1000
	distances[5][10] = 0.37*1000
	distances[5][11] = 0.6*1000
	distances[5][12] = 0.26*1000
	distances[5][13] = 0.9*1000

	distances[6][0] = 0.15*1000 
	distances[6][10] = 0.55*1000
	distances[6][11] = 0.18*1000

	distances[7][1] = 0.19*1000
	distances[7][9] = 0.56*1000
	distances[7][13] = 0.17*1000

	distances[8][1] = 0.4*1000
	distances[8][2] = 0.2*1000
	distances[8][4] = 0.18*1000
	distances[8][13] = 0.6*1000

	distances[9][0] =0.2*1000
	distances[9][7] = 0.56*1000
	distances[9][11]= 0.16*1000
	distances[9][13] = 0.5*1000

	distances[10][3] = 0.3*1000
	distances[10][5] = 0.37*1000
	distances[10][6] = 0.55*1000
	distances[10][12] = 0.24*1000

	distances[11][0] = 0.12*1000
	distances[11][5] = 0.6*1000
	distances[11][6] = 0.18*1000
	distances[11][9] = 0.16*1000
	distances[11][12] = 0.4*1000

	distances[12][5] = 0.26*1000
	distances[12][10] = 0.24*1000
	distances[12][11] = 0.4*1000

	distances[13][1] = 0.13*1000
	distances[13][5] = 0.9*1000
	distances[13][7] = 0.17*1000
	distances[13][8] = 0.6*1000
	distances[13][9] = 0.5*1000

	tsp = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
	population = []
	for i in range(50):
		population.append( (tsp_fitness(tsp), tsp) )

	for gen in range(50000):
		new_population = []
		for i in range(50):
			parents = random.choices(get_item(population), get_weights(population), k = 2)
			child = tsp_reproduce(parents)
			probability = random.uniform(0,1)
			if(probability > 0.4):
				child[0] = tsp_mutate(child[0])
				child[1] = tsp_mutate(child[1])
			new_population.append( (tsp_fitness(child[0]), child[0]) )
			new_population.append( (tsp_fitness(child[1]), child[1]) )
		new_population.sort()
		new_population.reverse()
		population = new_population[:50]
		print("=== Generation: %d , Best fitness value: %d === " % (gen, new_population[0][0]))
		
		if(population[0][0] >= 350):
			break
	print("Best solution: ", population[0][1], " with fitness: ", population[0][0])


def main():
	val = input("For 8-Queens, press 1. For Travelling salesperson, press 2: ")
	if(val == '1'):
		GA_Queens()
	elif(val == '2'):
		GA_TSP()
	else:
		print("Invalid input")


if __name__=='__main__':
    main()