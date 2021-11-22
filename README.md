# SortCluster
# Language: Python
# Input: TXT
# Output: CSV
# Tested with: PluMA 1.1, Python 3.6
# Dependency: 

PluMA plugin that takes as input a network and a set of clusters,
and sorts the network nodes based on their cluster membership.

The plugin takes as input a parameter file of keyword, value pairs:
network: CSV file for network
clusters: CSV file for clusters


The network is input as an adjacency matrix
(CSV file), with the value at entry (i, j) corresponding to the weight
of the edge between nodes i and j.

The network is output as an adjacency matrix
but with nodes reordered, with nodes in the same cluster grouped together.
