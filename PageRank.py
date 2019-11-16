import pandas as pd


out_edges_dict = {}
in_edges_dict = {}
pages_rank_dict = {}
calculate_pagerank_activated = False


def load_graph(path):
    df = pd.read_csv(path, header=None)
    for row in df.iterrows():
        source = str(row[1][0])
        dest = str(row[1][1])

        # initialize the out_edges and in_edges dicts:
        if not out_edges_dict.get(source):
            out_edges_dict[source] = [dest]
        else:
            out_edges_dict[source].append(dest)

        if not in_edges_dict.get(dest):
            in_edges_dict[dest] = [source]
        else:
            in_edges_dict[dest].append(source)

        # initialize pages_rank_dict:
        if not pages_rank_dict.get(source):
            pages_rank_dict[source] = 0
        if not pages_rank_dict.get(dest):
            pages_rank_dict[dest] = 0


def calculate_page_rank(beta, delta, maxIterations):
    next_pages_rank_dict = {}
    exist_smaller_then_delta = False
    sum = 0 #TODO: S from equetion, check if needed
    # iteration 0
    for page in pages_rank_dict:
        pages_rank_dict[page] = 1/len(pages_rank_dict)

    while maxIterations > 0 and not exist_smaller_then_delta:
        for page in pages_rank_dict:
            sum_indeg = 0
            if page not in in_edges_dict:
                pages_rank_dict[page] = 0
            if page in in_edges_dict:
                prev_pagerank = pages_rank_dict[page]
                for in_deg in in_edges_dict[page]:
                    sum_indeg = sum_indeg + beta * (pages_rank_dict[in_deg] / len(out_edges_dict[in_deg]))
                next_pages_rank_dict[page] = sum_indeg
                sum = sum + sum_indeg #TODO: check if neeeded
                current_delta = abs(sum_indeg - prev_pagerank)
                if current_delta >= 0:
                    if current_delta < delta:
                        exist_smaller_then_delta = True
        maxIterations = maxIterations - 1
        for i in next_pages_rank_dict:
            pages_rank_dict[i] = next_pages_rank_dict[i] + (1-sum) / len(pages_rank_dict) #TODO: check if needed
        next_pages_rank_dict = {}
        sum = 0
    calculate_pagerank_activated = True


def get_PageRank(node_name):
    if not calculate_pagerank_activated:
        return -1
    if node_name not in pages_rank_dict:

        return -1
    else:
        return pages_rank_dict[node_name]


def get_top_nodes(n):
    highest_pagerank_n_pages = list()
    if not calculate_pagerank_activated:
        return highest_pagerank_n_pages
    sorted_pagerank_dict = sorted(pages_rank_dict.items(), key=lambda x: x[1])
    if n > 0:
        i = 0
        while i < n:
            highest_pagerank_n_pages.append(sorted_pagerank_dict[i])
            i = i + 1
        return highest_pagerank_n_pages
    if n > len(pages_rank_dict):
        get_all_PageRank()


def main():
    load_graph("C:\\Users\\Inbar\\Downloads\\myGraph.csv")
    print(out_edges_dict)
    print(in_edges_dict)
    print(pages_rank_dict)
    calculate_page_rank(1, 0.001, 20)
    print(pages_rank_dict)
    print(get_PageRank("A"))
    print(get_top_nodes(5))


if __name__ == '__main__':
    main()
