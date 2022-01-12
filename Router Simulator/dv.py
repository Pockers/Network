'''
    Author: Michaela Hay
    Student ID: 1001649623
    Lab 2: Simulate Router Behavior using Bellman Ford Algorithm
    Finished: 11/20/2021
    Professor: Liu, Yongh
    Class: 4344-001
    Python Vers: 3.8.
'''
import time
import numpy

# Stores all file info
fileInfo = []
# Keeps track of all individual nodes
nodes = []
# Keeps track of neighbors of node - the index is the node itself
neighbors = []
# A is a matrix array of the DV tables
A = []
# Keeps track of how many iterations are done
iterations = 0

def countVertices(file):
    f = open(file,"r")
    verticesCount = 0

    for row in f:
        row = row.split(" ")
        u = row[0]
        v = row[1]
        cost = row[2]
        fileInfo.append((u,v,cost))
        if (row[0] not in nodes):
            nodes.append(row[0])
            verticesCount += 1
        if (row[1] not in nodes):
            nodes.append(row[1])
            verticesCount += 1
    return verticesCount

# Initialize all DV tables with file info
def initialGraph(g, node):
    # g starts as a matrix of 0's
    # node_neighbors holds all neighbors for the node of the current index --
    # node_neighbors[node] = neighbors of [node]
    node_neighbors = []
    for i in range(0,len(fileInfo)):
        for j in range(0,2):
            # Find node in file
            if node == fileInfo[i][j]:
                # Shove values of its neighor nodes + costs in g
                # Also keep track of neighboring nodes to current node
                if j == 1:
                    g[int(node)-1][int(fileInfo[i][0])-1] = fileInfo[i][2]
                    node_neighbors.append([fileInfo[i][0]])
                if j == 0:
                    g[int(node)-1][int(fileInfo[i][1])-1] = fileInfo[i][2]
                    node_neighbors.append([fileInfo[i][1]])
    neighbors.append(node_neighbors)
    # Replace all currently unreachable nodes with 16
    # Replace cost of node to itself to 0
    g = numpy.where(g == 0,16,g)
    g[int(node)-1][int(node)-1] = 0
    global iterations
    iterations += 1
    return g

# Updates passed graph with its neighbors' information - Bellman Ford Algorithm
# is implemented here
def updateDV(g, node):
    # Send a graph into here, check its neighbors' graphs and update with Bellman
    # Return confirmation if DV was updated (denoted by stability)

    # Find all neighbors to the current node and save them to a list
    for i in range(0, len(nodes)):
        if str(node) == str(nodes[i]):
            node_neighbors = neighbors[i]
    # Look at the neighbor list for current node and update tables for current node
    # Update current node V with neighbor's info
    # Grab a neighbor's DV table
    for i in range(0,len(node_neighbors)):
        # Set neighbor_table equal to the neighbor DV table
        current_neighbor = int(node_neighbors[i][0])
        for m in range(0, len(nodes)):
            if int(current_neighbor) == int(nodes[m]):
                neighbor_table = A[m]
                break

        # Look inside DV table and GRAB INFO node does not already have
        for j in range(0,len(g)):
            # Skip own personal row
            if j == int(node)-1:
                j = 1+j
                if j > len(g)-1:
                    break

            # Check if row contains all 16s - if it does then skip
            test_array = numpy.unique(neighbor_table[j])
            if (len(test_array) != 1):
                total_costs_neighbor = 0
                total_costs_for_self = 0
                # Check if neighbor table has numbers less than current
                for n in range(0,len(neighbor_table[j])):
                    total_costs_neighbor = total_costs_neighbor + neighbor_table[j][n]
                    total_costs_for_self = total_costs_for_self + g[j][n]
                    if total_costs_neighbor < total_costs_for_self:
                        g[j] = neighbor_table[j]

    # UPDATE current node with least cost weight
    # Row for current node whose weight should be adjusted
    nodeRow = g[int(node)-1]
    # Takes you inside of the row under examination
    for i in range(0,len(nodes)):
        # i = destination node
        cost = nodeRow[i]

        # Examine current cost [i] of row against other costs
        for node_1 in range(0, len(nodes)):
            source_to_node_1 = g[int(node)-1][node_1]
            node_1_to_node_2 = g[node_1][i]
            interCost = source_to_node_1 + node_1_to_node_2
            if (interCost < cost):
                cost = interCost
                g[int(node)-1][i] = cost

    # CHECK if reached stable state (All graphs are the same)
    check = True
    for i in range(0,len(A)):
        for j in range(1,len(A)):
            if numpy.array_equal(A[i],A[j]):
                check = True
            # If there is one difference in a graph, break out because
            # the system is not stable, still
            else:
                check = False
                break
    global iterations
    iterations += 1
    return check

if __name__ == '__main__':
    print("Enter name of file: ")
    file_name = input("")
    print("Mode:\n[1] By iteration\n[2] Live output")
    mode = input("")
    print("\n\n")
    print("\n\n|==== Print Tables ====|\n\n")
    # Count total vertices
    vertices = countVertices(file_name)
    # Create the matrices
    for i in range(0,vertices):
        dv = numpy.zeros((vertices,vertices))
        A.append(dv)
    # Initialize all the tables
    for i in range(0,vertices):
        A[i] = initialGraph(A[i],nodes[i])

    # Run Bellman Ford on A - is stable only if graphs are no longer being updated
    stable = False
    # Keep running Bellman if system is not stable
    user_input = ""
    while (stable is not True):
        if (mode == str(1)):
            for i in range(0, len(A)):
                if user_input == str(2):
            	    stable = True
            	    break
                print("DV for node " + nodes[i] + ":")
                print(A[i])
                if (i < len(A)):
                    user_input = input("==============\n[Enter] to Continue\n[1] Change Cost\n[2] Stop\n==============\n")
                    if user_input == str(1):
                        source = input("Enter source node: ")
                        destination = input("Enter destination node: ")
                        cost = input("Enter cost between nodes: ")

                        # Search A for source node and destination node. Change cost for each matrix.
                        for j in range(0,len(A)):
                            for i in range(0, len(nodes)):
                                if str(nodes[i]) == str(source):
                                    A[j][i][int(destination)-1] = cost
                                    break
                            for i in range (0, len(nodes)):
                                if str(nodes[i]) == str(destination):
                                    A[j][i][int(source)-1] = cost
                                    break
        if (mode == str(2)):
            start = time.time()
            for i in range(0, len(A)):
                print("DV for node " + nodes[i] + ":")
                print(A[i])
                print("\n")
        # Update the values thru Bellman Ford algorithm
        for i in range(0, len(nodes)):
            # Per each node and its own DV, update its table
            # If reach stable state, then break out of loop with stable == True
            if user_input == str(2):
                stable = True
                break
            stable = updateDV(A[i], nodes[i])

	# Print out the rest of the complete, stable DV tables
    if (mode == str(1)):
        for i in range(0, len(A)):
            print("DV for node " + nodes[i] + ":")
            print(A[i])
            print("\n")
        print("System took " + str(iterations) + " cycles to reach stable state.")
    if (mode == str(2)):
        for i in range(0, len(A)):
            print("DV for node " + nodes[i] + ":")
            print(A[i])
            print("\n")
            end = time.time()
            total_time = end-start
        print("Program took " + str(total_time) + " seconds to execute.")
        print("System took " + str(iterations) + " cycles to reach stable state.")

