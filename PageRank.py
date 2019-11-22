import pandas as pd

out_edges = {}                          # adjacency list for all the out edges
in_edges = {}                           # adjacency list for all the in edges
pages_ranks = {}                        # the page ranks of all the vertexes
calculate_pagerank_activated = False    # flag which tells if we calculated the page ranks or not


# get a path to a csv file and initialize our three global dictionaries
def load_graph(path):
    # csv file loading:
    try:
        df = pd.read_csv(path, header=None)
    except FileNotFoundError:
        print("an error occurred while trying to read the file")
        exit(1)

    for row in df.iterrows():
        source = str(row[1][0])
        dest = str(row[1][1])

        # initialize the out_edges and in_edges dicts:
        if not out_edges.get(source):
            out_edges[source] = [dest]
        else:
            out_edges[source].append(dest)

        if not in_edges.get(dest):
            in_edges[dest] = [source]
        else:
            in_edges[dest].append(source)

        # initialize pages_rank_dict:
        if not pages_ranks.get(source):
            pages_ranks[source] = 0
        if not pages_ranks.get(dest):
            pages_ranks[dest] = 0

        # fill additional empty nodes in out_edges and in in_edges:
        for page in pages_ranks:
            if page not in out_edges:
                out_edges[page] = []
            if page not in in_edges:
                in_edges[page] = []


# calculate the page ranks
def calculate_page_rank(beta, delta, maxIterations):
    # iteration 0:
    for page in pages_ranks:
        pages_ranks[page] = 1 / len(pages_ranks)

    cur_iteration = 0
    diff = float('inf')
    ranks_saver = {}

    # the iterations loop:
    while cur_iteration < maxIterations and diff > delta:
        s = 0
        diff = 0
        # the calculation of the temporary page ranks:
        for page in pages_ranks:
            temporary_page_rank = 0    # the new page rank value for the current page in the current iteration
            for in_neighbor in in_edges[page]:
                temporary_page_rank += beta * (pages_ranks[in_neighbor] / len(out_edges[in_neighbor]))
            s += temporary_page_rank
            ranks_saver[page] = temporary_page_rank
            diff += abs(temporary_page_rank - pages_ranks[page])

        # the calculation of the final (not temporary) page ranks:
        for page in pages_ranks:
            pages_ranks[page] = ranks_saver[page] + ((1 - s) / len(pages_ranks))

        cur_iteration += 1

    global calculate_pagerank_activated
    calculate_pagerank_activated = True


# gets a node name and return it's page rank
def get_PageRank(node_name):
    if not calculate_pagerank_activated:
        return -1
    if node_name not in pages_ranks:
        return -1
    else:
        return pages_ranks[node_name]


# get number n and return the n nodes with the highest page rank ordered form the highest to the lowest
def get_top_nodes(n):
    highest_pagerank_n_pages = list()
    sorted_pagerank_dict = get_all_PageRank()
    if 0 < n < len(pages_ranks):
        i = 0
        while i < n:
            highest_pagerank_n_pages.append(sorted_pagerank_dict[i])
            i = i + 1
        return highest_pagerank_n_pages
    if n > len(pages_ranks):
        return get_all_PageRank()


# return all the page ranks
def get_all_PageRank():
    all_page_rank = list()
    if not calculate_pagerank_activated:
        return all_page_rank
    sorted_pagerank_dict = sorted(pages_ranks.items(), key=lambda x: x[1], reverse=True)
    return sorted_pagerank_dict