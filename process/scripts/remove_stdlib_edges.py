"""
This script removes all standard library edges,
and adds those application edges which are in the transitive of the removed edges
"""

import csv
import sys
from collections import defaultdict, namedtuple
from pathlib import Path

import networkx as nx
from tqdm import tqdm

ROOT_METHOD = "<boot>"

# Edge and Node classes to model the graph
Edge = namedtuple("Edge", "bytecodeOffset dest")
Node = namedtuple(
    "Node", ["edges", "reachable_app_nodes", "reachableNodes", "isStdLibNode"]
)


def main():
    """The main method of the removestdlibedges.py script."""
    analysisfile = Path(sys.argv[1])
    methodsfile = Path(sys.argv[2])
    outputfile = Path(sys.argv[3])

    # Loop through all the file names
    nodes_with_closure = remove_stdlib_edges(analysisfile, methodsfile, True)
    nodes_without_closure = remove_stdlib_edges(analysisfile, methodsfile, False)

    # Compute without-closure edges
    without_closure_edges = set()
    for name, obj in nodes_without_closure.items():
        for edge in obj.edges:
            edge_id = (name, edge.bytecodeOffset, edge.dest)
            without_closure_edges.add(edge_id)

    # Write output
    printed = set()
    with open(outputfile, "w") as filep:
        print("Writing output ...")
        writer = csv.writer(filep)
        writer.writerow(["method", "offset", "target", "original", "direct"])
        for name, obj in nodes_with_closure.items():
            for edge in obj.edges:
                edge_id = (name, edge.bytecodeOffset, edge.dest)
                if edge_id in printed:
                    continue
                printed.add(edge_id)

                if edge_id in without_closure_edges:
                    writer.writerow((name, edge.bytecodeOffset, edge.dest, "1", "1"))
                else:
                    writer.writerow((name, edge.bytecodeOffset, edge.dest, "1", "0"))


def empty_node():
    """Create an empty node"""
    return Node([], set(), set(), False)


def remove_stdlib_nodes(nodes, stdlibnodes):
    """remove standard library nodes"""
    print("Removing stdlib nodes ...")
    for node in stdlibnodes:
        del nodes[node]
    print("Done removing stdlib nodes")
    return nodes


def get_std_lib_nodes_directly_called(static_analysis_nodes, std_lib_nodes):
    """Computes the set of stdLib nodes which get directly called
    from an application node
    (does not include stdlib nodes with no outgoing edges)"""
    directly_called_nodes = set()
    for node_object in static_analysis_nodes.values():
        for edge in node_object.edges:
            if edge.dest in std_lib_nodes:
                directly_called_nodes.add(edge.dest)
    return directly_called_nodes


def build_networkx_graph(std_lib_nodes):
    G = nx.DiGraph()
    for node_name, node in std_lib_nodes.items():
        for edge in node.edges:
            G.add_edge(node_name, edge.dest)
    return G


def compute_reachable_application_nodes(
    std_lib_nodes, application_method_list, static_analysis_nodes
):
    std_lib_nodes_called_directly_from_application = get_std_lib_nodes_directly_called(
        static_analysis_nodes, std_lib_nodes
    )

    print("Building graph ...")
    G = build_networkx_graph(std_lib_nodes)

    app_methods_set = set(application_method_list)

    print("Computing reachable application nodes (fast version) ...")
    for node_name in tqdm(std_lib_nodes_called_directly_from_application):
        # Get reachable nodes from node_name using built-in fast DFS
        reachable_nodes = nx.descendants(G, node_name)

        # Intersect with application methods
        reachable_apps = reachable_nodes & app_methods_set

        std_lib_nodes[node_name].reachable_app_nodes.update(reachable_apps)

    print("Done computing reachable application nodes")
    return std_lib_nodes


def get_std_lib_nodes(static_analysis_nodes, application_method_list):
    """Gets a list of standard library nodes"""
    std_lib_nodes = {}
    # if a node does not contain a class name from any of the classes
    # given by javaq, it is considered a standard library node
    for node_name, node_object in static_analysis_nodes.items():
        if node_name not in application_method_list:
            std_lib_nodes[node_name] = node_object
    return std_lib_nodes


def replace_std_lib_edges_with_app_edges(
    static_analysis_nodes, std_lib_nodes, application_method_list
):
    """Replaces edges ending in stdLib nodes with their reachable application
    nodes Assumes that wala nodes does not include stdLib nodes"""
    print("Replacing stdlib edges with application edges ...")
    for node_object in (loop := tqdm(static_analysis_nodes.values())):
        # Compute the standard libaray edges to remove, and the new application
        # nodes to replace them with
        new_edges_to_be_added = []
        edges_to_std_lib_to_be_removed = set()
        for edge in node_object.edges:
            # Remove standard library edges
            if edge.dest not in application_method_list:
                edges_to_std_lib_to_be_removed.add(edge)
            # If the destination is in std_lib_nodes, replace with the set of
            # reachable application nodes
            if edge.dest in std_lib_nodes:
                for node in std_lib_nodes[edge.dest].reachable_app_nodes:
                    new_edges_to_be_added.append(Edge(edge.bytecodeOffset, node))
        # Remove the standard library edges
        for edge_name in edges_to_std_lib_to_be_removed:
            node_object.edges.remove(edge_name)

        # Replace the standard library edges with ones to application nodes
        node_object.edges.extend(new_edges_to_be_added)
    print("Done replacing stdlib edges with application edges")


def remove_stdlib_edges(analysisfile, methodsfile, do_transitive_closure):
    """Remove edges to the std library, but keep the transitive closures."""
    # Intialize some variables
    nodes = defaultdict(empty_node)
    # Adjacency list representation. However this does not include nodes with no
    # outgoing edges
    appmethodlist = set()  # Needed to remove java standard library nodes
    appmethodlist.add(ROOT_METHOD)
    # Read the analysis reachable edges
    with open(analysisfile) as filep:
        # Loop through the edges
        for edge in csv.DictReader(filep):
            # Create new node if it doesn't exist
            _method = edge["method"]
            _offset = edge["offset"]
            _target = edge["target"]
            nodes[_method].edges.append(Edge(_offset, _target))

    # Read the nethod list from the methods.csv file
    with open(methodsfile) as filep:
        lines = [line.rstrip() for line in filep]
        for line in lines:
            appmethodlist.add(line)

    stdlibnodes = get_std_lib_nodes(nodes, appmethodlist)
    remove_stdlib_nodes(nodes, stdlibnodes)
    if do_transitive_closure:
        compute_reachable_application_nodes(stdlibnodes, appmethodlist, nodes)
        replace_std_lib_edges_with_app_edges(nodes, stdlibnodes, appmethodlist)

    return nodes


if __name__ == "__main__":
    main()
