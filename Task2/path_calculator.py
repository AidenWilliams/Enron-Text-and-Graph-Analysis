from tqdm import tqdm


# graph is the networkx graph
# paths is a dictionary holding all 2 vertices in a tuple as key and the length as its value i.e. {(start, end): length}
# origin is the vertex for which the paths are being created
# v2 is an intermediary vertex
# p_length is the path length so far (to be saved as the value for paths)
# seen is a set of all the vertices visited while building these paths
# looping is a boolean variable that indicates whether the function has been stuck in a loop or not
def build_paths(graph, paths, origin, finished, looped, v2=None, p_length=1, seen=None, looping=False):
    if seen is None:
        seen = set()
    # get a list of all the vertices connected to v1 (directly)
    # if v2 is not defined (initial run)
    if v2 is None:
        # v1 is the origin
        if looping:
            # include finished vertices for accuracy
            connected_to_v1 = [t[1] for t in paths.keys() if t[0] == origin]
        else:
            # ignore finished vertices for speed
            connected_to_v1 = [t[1] for t in paths.keys() if t[0] == origin and t[0] not in finished]
    # if v2 is defined
    else:
        # v1 is the old v2
        if looping:
            # include finished vertices for accuracy
            connected_to_v1 = [t[1] for t in paths.keys() if t[0] == v2]
        else:
            # ignore finished vertices for speed
            connected_to_v1 = [t[1] for t in paths.keys() if t[0] == v2 and t[0] not in finished]

    # start checking these vertices
    for vertex in connected_to_v1:
        # identify if we are in a loop
        # treat loop as if vertex is origin
        if vertex in seen:
            # add tuple of the start and end vertices of a loop
            looped.add(tuple([vertex, v2]))
            # create a tuple of the origin and v2
            t = tuple([origin, v2])
            # has the path already been defined?
            if t not in paths:
                # if not
                # add it with p_length - 1
                # I subtract 1 here as one iteration has been done to "catch" the loop
                paths.update({t: p_length-1})
                continue
            # if yes (tuple already in paths)
            # if the new path length is less than the old length
            if (p_length - 1) < paths.get(t):
                # Update only the value/ path length
                # I subtract 1 here for the same reason as before
                paths.update({t: p_length - 1})
                continue
            continue

        # if the vertex isn't connected to any other vertices or the vertex is the origin
        # I consider this particular path to be completed
        if graph.out_degree(vertex) == 0 or vertex == origin:
            # if vertex doesnt connect to anything else mark it as finished
            if graph.out_degree(vertex) == 0:
                finished.add(vertex)

            # If the vertex is the origin
            if vertex == origin:
                # create a tuple of the origin and v2
                t = tuple([vertex, v2])
                # has the path already been defined?
                if t not in paths:
                    # if not
                    # add it with p_length - 1
                    # I subtract 1 here as origin has been visited twice
                    paths.update({t: p_length-1})
                    continue
                # if yes (tuple already in paths)
                # if the new path length is less than the old length
                if (p_length - 1) < paths.get(t):
                    # Update only the value/ path length
                    # I subtract 1 here for the same reason as before
                    paths.update({t: p_length-1})
                    continue
            # if the vertex isn't the origin
            else:
                # create a tuple of the origin and vertex
                t = tuple([origin, vertex])
                # has the path already been defined?
                if t not in paths:
                    # if not
                    # add it with p_length
                    paths.update({t: p_length})
                    continue
                # if yes (tuple already in paths)
                # if the new path length is less than the old length
                if p_length < paths.get(t):
                    # Update only the value/ path length
                    paths.update({t: p_length})
                    continue
        # If the vertex hasn't been visited yet, or isn't defined as an end vertex
        else:
            # add v2 to the set of seen vertices
            seen.add(v2)
            # if all the paths from this has been checked dont build them again (infinite loop)
            x = tuple([vertex, v2])
            y = tuple([v2, vertex])
            # is the function in a loop?
            b = y in looped or x in looped
            if vertex not in finished or b:
                # as the vertex has out degree and isn't the origin, hasn't had it's paths already created
                # or the function is in a loop
                # there are still paths to be found!
                # v2 is now the current vertex
                # p_length is incremented by 1
                # looping is updated
                build_paths(graph, paths, origin, finished, looped,  v2=vertex, p_length=p_length + 1, seen=seen,
                            looping=b)

# graph is the networkx graph
# edges is the dictionary of tuples as keys and weights as values created when building the mention graph
def get_average_path_length(graph, edges):
    # Holds a set of all the vertices that have had their paths created
    finished = set()
    # Holds a set of tuples of 2 vertices indicating there is a loop between both vertices
    looped = set()
    # define vertices as a list of the graph's nodes
    vertices = list(graph.nodes)
    # Get the basic 1 distance paths by getting the tuple in edges and paring it with 1
    paths = {e: 1 for e in edges}
    # paths key will be tuple source to destination: value is length of path
    #                        (source,   destination): p_length

    # start iterating over all the vertices
    for v1 in tqdm(vertices):
        # use degrees to make process faster
        # if the vertex doesnt have an out degree then don't bother trying to build paths emerging from it as there are none!
        # if the vertex is with the finished set, then its paths have already been added to paths
        if graph.out_degree(v1) == 0 or v1 in finished:
            # if it isn't added to the finished set add it
            if v1 not in finished:
                finished.add(v1)
            continue
        # build paths for v1
        build_paths(graph, paths, v1, finished, looped)
        # add v1 to the finished set
        finished.add(v1)

    # Add all the distances in paths' values
    sum = 0
    for distance in paths.values():
        sum += distance
    #       1
    # -------------
    # |V|^2 - |V|
    lG = \
        1 \
        / (len(vertices) * len(vertices) - len(vertices))
    # return the average path length
    return float(lG * sum)


# graph is the networkx graph
# edges is the dictionary of tuples as keys and weights as values created when building the mention graph
def get_diameter(graph, edges):
    # Holds a set of all the vertices that have had their paths created
    finished = set()
    # Holds a set of tuples of 2 vertices indicating there is a loop between both vertices
    looped = set()
    # define vertices as a list of the graph's nodes
    vertices = list(graph.nodes)
    # Get the basic 1 distance paths by getting the tuple in edges and paring it with 1
    paths = {e: 1 for e in edges}
    # paths key will be tuple source to destination: value is length of path
    #                        (source,   destination): p_length

    # start iterating over all the vertices
    for v1 in tqdm(vertices):
        # use degrees to make process faster
        # if the vertex doesnt have an out degree then don't bother trying to build paths emerging from it as there are none!
        # if the vertex is with the finished set, then its paths have already been added to paths
        if graph.out_degree(v1) == 0 or v1 in finished:
            # if it isn't added to the finished set add it
            if v1 not in finished:
                finished.add(v1)
            continue
        # build paths for v1
        build_paths(graph, paths, v1, finished, looped)
        # add v1 to the finished set
        finished.add(v1)

    # Add all the distances in paths' values
    shortest = 0
    for distance in paths.values():
        if distance > shortest:
            shortest = distance

    return shortest
