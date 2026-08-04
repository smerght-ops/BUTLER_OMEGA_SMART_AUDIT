"""Graph projections derived exclusively from the published index."""

from collections import defaultdict, deque


class ProjectGraphBuilder:
    def build(self, index, edge_types=None):
        allowed = set(edge_types or ())
        edges = [dict(edge) for edge in index.edges if not allowed or edge["edge_type"] in allowed]
        node_ids = {item["identifier"] for item in index.nodes}
        adjacency, reverse = defaultdict(list), defaultdict(list)
        for edge in edges:
            adjacency[edge["source"]].append(edge["target"]); reverse[edge["target"]].append(edge["source"])
        components, unseen = [], set(node_ids)
        while unseen:
            root, current = min(unseen), []
            queue = deque([root]); unseen.remove(root)
            while queue:
                node = queue.popleft(); current.append(node)
                for target in sorted(set(adjacency[node] + reverse[node])):
                    if target in unseen: unseen.remove(target); queue.append(target)
            components.append(current)
        return {"index_version":index.index_version,"nodes":[dict(item) for item in index.nodes],
            "edges":edges,"adjacency_map":{key:sorted(set(value)) for key,value in adjacency.items()},
            "reverse_adjacency_map":{key:sorted(set(value)) for key,value in reverse.items()},
            "connected_components":components,"root_nodes":sorted(node_ids-set(reverse)),
            "leaf_nodes":sorted(node_ids-set(adjacency)),"node_types":sorted({item["type"] for item in index.nodes}),
            "edge_types":sorted({item["edge_type"] for item in edges})}

    def dependency(self, index):
        return self.build(index, {"imports","depends_on","inherits","uses","owns","permission"})

    def runtime(self, index):
        return self.build(index, {"dispatch","execute","permission","return","nested_call","ownership"})
