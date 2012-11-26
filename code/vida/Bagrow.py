__author__ = 'shirc'

class Bagrow(object):
    def get_community(self, graph, start):
        self.graph = graph
        self.start = start
        self.community = set()
        self.neighbours = set()
        self.outwards = {}
        self.merge(start)
        return self.find()

    def merge(self, node):
        self.community.add(node)
        if node in self.neighbours:
            self.neighbours.remove(node)
        for neighbour in node.all_neighbour():
            for nn in neighbour.all_neighbour():
                in_community = 0
                out_community = 0
                if nn in self.community:
                    in_community += 1
                else:
                    out_community += 1
            self.outwards[neighbour] = (float(out_community) - in_community) / (in_community+out_community)

    def continue_search(self):
        if len(self.community) < self.graph.num_vertices():
            return True
        inside = 0
        total = 0
        for node in self.community:
            in_community = 0
            out_community = 0
            for neighbour in node.all_neighbour():
                if neighbour in self.neighbours:
                    out_community += 1
                else:
                    in_community += 1
            if in_community > out_community:
                inside += 1
            total += 1
        return float(inside) / total < 0.9

    def find(self):
        while self.continue_search():
            best_outward = 1
            add_node = None
            for neighbour in self.neighbours:
                outward = self.outwards[neighbour]
                if outward < best_outward:
                    best_outward = outward
                    add_node = neighbour
            self.merge(add_node)
        return self.community