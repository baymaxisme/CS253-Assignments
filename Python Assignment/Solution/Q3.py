def find_safe_route(graph, start, end, blocked_nodes):
    n = len(graph)
    # Check if start or end is blocked
    if start in blocked_nodes or end in blocked_nodes:
        return ([], -1)
    
    distances = [float('inf')]*n #distances[i] is the shortest time found from start to i
    distances[start] = 0 

    visited = [False]*n #A list to keep track of visited nodes

    predecessors= [None]*n #list to remember the path
    
    for i in range(n):
        #Finding the unvisited , non-blocked node with the minimum distance
        u = -1 
        min_dist = float('inf')
        for j in range(n):
            if not visited[j] and j not in blocked_nodes:
                if distances[j] < min_dist:
                    min_dist = distances[j]
                    u = j
        
        #The destination is inaccessible if the node is unreachable
        if u==-1 or distances[u] == float('inf'):
            break

        visited[u] = True

        #Stopping if the target node is reached
        if u == end:
            break

        #Updating neighbours of u
        for v in range(n):
            if graph[u][v] > 0 and not visited[v] and v not in blocked_nodes:
                new_time = distances[u] + graph[u][v]
                if new_time < distances[v]:
                    distances[v] = new_time
                    predecessors[v] = u
    
    if distances[end] == float('inf'):
        return([], -1)
    
    #Path construction
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()

    return (path, int(distances[end]))

#TO SEE OUTPUT
#if __name__ == "__main__":
#    graph = [
#        [0, 5, 0, 8, 0],
#        [5, 0, 3, 0, 0],
#        [0, 3, 0, 2, 7],
#        [8, 0, 2, 0, 4],
#        [0, 0, 7, 4, 0]
#    ]
#
#   start_node = 0
#    end_node = 4
#    blocked = [3]  # Lecture Hall Complex is closed
#
#    print(find_safe_route(graph, start_node, end_node, blocked))