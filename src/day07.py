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
        elem = min(elems_with_no_dependencies)
        elems_with_no_dependencies.remove(elem)
        remove_dependency(elem)
        path.append(elem)

    return path

## Assuming dependencies aren't cyclic (not solvable otherwise)
def topological_dag_path(dependencies):
    """
    Khan's algorithm implementation.
    This does the same as 'calc_path(dependencies)', but more
     efficiently as it does not require a full depedency map.
    """
    incoming_edges = build_dependency_map(dependencies)    # elem -> {incoming edges}
    outgoing_edges = {e: set() for e in incoming_edges.keys()}
    for e1, inc_edges in incoming_edges.items():
        for e2 in inc_edges:
            outgoing_edges[e2].add(e1)

    elems_with_no_dependencies = {e for e in incoming_edges.keys() if len(incoming_edges[e]) == 0}

    path = list()
    ## Following Kahn's algorithm for topological sort of a directed acyclic graph
    while len(elems_with_no_dependencies) > 0:
        elem = min(elems_with_no_dependencies)  # min -> first alphabetically
        elems_with_no_dependencies.remove(elem)
        path.append(elem)

        for node in outgoing_edges[elem].copy():
            outgoing_edges[elem].remove(node)
            incoming_edges[node].remove(elem)
            if len(incoming_edges[node]) == 0:
                elems_with_no_dependencies.add(node)
    
    assert len([s for s in incoming_edges.values() if len(s) > 0]) == 0 ## Assert no inc edges left
    assert len([s for s in outgoing_edges.values() if len(s) > 0]) == 0 ## Assert no out edges left

    return path

def get_time_to_solve(dependencies, num_workers, cost_map):
    dep_map = build_full_dependency_map(dependencies)
    possible_jobs = {e for e, deps in dep_map.items() if len(deps) == 0}
    for job in possible_jobs:
        del dep_map[job]

    time = 0
    path = list()
    current_jobs = dict()
    free_workers = num_workers
    while True:

        # Check for new jobs
        while free_workers > 0 and len(possible_jobs) > 0:
            job = possible_jobs.pop()
            current_jobs[job] = cost_map[job]
            free_workers -= 1

        # Step all jobs
        for job in list(current_jobs.keys()):
            current_jobs[job] -= 1
            if current_jobs[job] == 0:  # Job finished
                free_workers += 1
                del current_jobs[job]
                path.append(job)

                for e in list(dep_map.keys()):
                    dep_map[e] -= {job}
                    if len(dep_map[e]) == 0:
                        possible_jobs.add(e)
                        del dep_map[e]

        time += 1
        if len(current_jobs) == 0 and len(possible_jobs) == 0:
            break

    return time

if __name__ == '__main__':
    lines = [l.rstrip() for l in sys.stdin.readlines()]
    matches = [re.match(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.', l) for l in lines]
    dependencies = [(m.group(2), m.group(1)) for m in matches]

    ## First part
    print(''.join(calc_path(dependencies)))

    ## Second part
    NUM_WORKERS = 5
    letter_to_int = {chr(i): 60 + i - 64 for i in range(65, 65+26)}
    print(get_time_to_solve(dependencies, NUM_WORKERS, letter_to_int))
