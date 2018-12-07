import sys
import re

def depends_on(first, second, dependency_map, visited=set()):
    """
    first depends on second ?
    """
    if second in visited:
        return False
    elif second in dependency_map[first]:
        return True
    for d in dependency_map[first]:
        visited.add(d)
        if depends_on(d, second, dependency_map, visited):
            return True
    return False

def build_dependency_map(dependencies):
    """
    maps elem to its first order dependencies
    """
    dependency_map = {elem: set() for elem in set([e for row in dependencies for e in row])}
    for first, second in dependencies:
        dependency_map[first].add(second)
    return dependency_map

def build_full_dependency_map(dependencies):
    """
    builds full dependency map, exhausting all recursive paths
    """
    dep_map = build_dependency_map(dependencies)
    def build_dependencies_of(first, visited=set()):
        for d in dep_map[first].copy():
            if d in visited:
                continue
            else:
                visited.add(d)
            dep_map[first] |= build_dependencies_of(d, visited)
        return dep_map[first]

    for k in dep_map.keys():
        build_dependencies_of(k, set())
    return dep_map

## Assuming dependencies aren't cyclic (not solvable otherwise)
def calc_path(dependencies):
    dep_map = build_full_dependency_map(dependencies)
    elems_with_no_dependencies = {e for e in dep_map.keys() if len(dep_map[e]) == 0}

    def remove_dependency(elem):
        del dep_map[elem]
        for e in dep_map.keys():
            dep_map[e] -= {elem}
            if len(dep_map[e]) == 0:
                elems_with_no_dependencies.add(e)

    path = list()
    while len(dep_map) > 0:
        print(elems_with_no_dependencies)
        elem = min(elems_with_no_dependencies)
        elems_with_no_dependencies.remove(elem)
        remove_dependency(elem)
        path.append(elem)

    return path

if __name__ == '__main__':
    lines = [l.rstrip() for l in open('../input/day07.in')]
    matches = [re.match(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.', l) for l in lines]
    dependencies = [(m.group(1), m.group(2)) for m in matches]

    ## First part
    print(''.join(calc_path(dependencies)))
    


