import networkx as nx
import csv

CSV_FILENAME = "ratings_Electronics (1).csv"
REV2_ROUNDS = 10

def create_graph(filename):
    g = nx.DiGraph()
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] not in g:
                g.add_node(row[0], type="user", fairness=1)
            if row[1] not in g:
                g.add_node(row[1], type="product", goodness=1)
            g.add_edge(row[0], row[1], rating=(float(row[2])-3)/2, reliability=1)    
    return g

def update_fairness(g):
    for node, data in g.nodes(data=True):
        if data['type'] == 'user':
            reliability_sum = 0
            number_of_edges = 0
            for edge in g.edges(node, data=True):
                reliability_sum += edge[2]['reliability']
                number_of_edges += 1
            g.nodes[node]['fairness'] = reliability_sum / number_of_edges

def update_goodness(g):
    for node, data in g.nodes(data=True):
        if data['type'] == 'product':
            product_sum = 0
            number_of_edges = 0
            for edge in g.in_edges(node, data=True):
                product_sum += edge[2]['reliability'] * edge[2]['rating']
                number_of_edges += 1
            g.nodes[node]['goodness'] = product_sum / number_of_edges
    
def update_reliability(g):
    for edge in g.edges(data=True):
        reliability =  0.5 * g.nodes[edge[0]]['fairness'] + 0.5 * (1 - abs(edge[2]['rating'] - g.nodes[edge[1]]['goodness'])/2)
        g.edges[edge[0], edge[1]]['reliability'] = reliability

def rev2(g, rounds):
    for i in range(rounds):
        print(f'Round {i}')
        update_fairness(g)
        update_goodness(g)
        update_reliability(g)
    
def the_good_the_bad_and_the_ugly(g):    
    maliciosos = []
    honestos = []
    for node, data in g.nodes(data=True):
        if data['type'] == 'user' and data['fairness'] < 0.3 and g.out_degree(node) >= 5:      
            maliciosos.append(node)
        if data['type'] == 'user' and data['fairness'] > 0.9 and g.out_degree(node) >= 10:      
            honestos.append(node)
    print('USUARIOS HONESTOS:')
    print(",".join(honestos))
    print(f'TOTAL DE USUARIOS HONESTOS: {len(honestos)}')
    print('USUARIOS MALICIOSOS:')
    print(",".join(maliciosos))
    print(f'TOTAL DE USUARIOS MALICIOSOS: {len(maliciosos)}')

def main():
    g = create_graph(CSV_FILENAME)
    print(f'Nodes: {g.order()} Edges: {g.size()}')
    rev2(g, 10)
    the_good_the_bad_and_the_ugly(g)

    

if __name__ == "__main__":
    main()