import sys

class Node:
    def __init__(self, child_nodes, metadata):
        self.child_nodes = child_nodes
        self.metadata = metadata

    # First Part
    def tree_sum(self):
        return sum(self.metadata) + sum([c.tree_sum() for c in self.child_nodes])

    # Second part
    def get_value(self):
        if len(self.child_nodes) == 0:
            return sum(self.metadata)

        return sum([
            self.child_nodes[i-1].get_value() for i in self.metadata if i-1 < len(self.child_nodes)
        ])


def build_tree(nums_iterator):
    num_child_nodes = next(nums_iterator)
    num_metadata_entries = next(nums_iterator)

    child_nodes = list()
    for _ in range(num_child_nodes):
        child_nodes.append(build_tree(nums_iterator))

    metadata = list()
    for _ in range(num_metadata_entries):
        metadata.append(next(nums_iterator))

    return Node(child_nodes, metadata)


if __name__ == '__main__':
    numbers = map(int, sys.stdin.readline().rstrip().split(' '))
    root = build_tree(numbers)

    ## First part
    print(root.tree_sum())

    ## Second part
    print(root.get_value())