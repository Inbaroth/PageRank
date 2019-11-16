import pandas as pd

out_edges_dict = {}
in_edges_dict = {}
pages_rank_dict = {}


def load_graph(path):
    try:
        df = pd.read_csv(path, header=None)
    except FileNotFoundError:
        print("an error occurred while trying to read the file")
    finally:
        exit(1)

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
    exist_smaller_then_delta = False
    # iteration 0
    for page in pages_rank_dict:
        pages_rank_dict[page] = 1 / len(pages_rank_dict)

    while maxIterations > 0 or not exist_smaller_then_delta:
        for page in pages_rank_dict:
            if page not in in_edges_dict:
                pages_rank_dict[page] = 0
            if page in in_edges_dict:
                prev_pagerank = pages_rank_dict[page]
                for in_deg in in_edges_dict[page]:
                    pages_rank_dict[page] = pages_rank_dict[page] + beta * (
                                pages_rank_dict[page] / len(out_edges_dict[in_deg]))

                # TODO: check if this calculation is needed before submiting
                ranks_sum = 0
                for node in pages_rank_dict:
                    ranks_sum = ranks_sum + pages_rank_dict[node]
                pages_rank_dict[node] = pages_rank_dict[page] + ranks_sum / len(pages_rank_dict)
                # TODO: end of extra calculation
                current_delta = pages_rank_dict[page] - prev_pagerank
                if current_delta >= 0:
                    if current_delta < delta:
                        exist_smaller_then_delta = True
        maxIterations = maxIterations - 1


def get_PageRank(node_name):
    if node_name not in pages_rank_dict:

        return -1
    else:
        return pages_rank_dict[node_name]


def get_all_PageRank():
    all_page_rank = list()
    if not calculate_pagerank_activated:
        return all_page_rank

    sorted_pagerank_dict = sorted(pages_rank_dict.items(), key=lambda x: x[1])

    return sorted_pagerank_dict


def main():
    load_graph("C:\\Users\\amiri\\Desktop\\myGrph.csv")


if __name__ == '__main__':
    main()


