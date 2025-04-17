# DAA Graph Algorithm Visualizer

![Python](https://img.shields.io/badge/python-3.x-blue.svg) ![Libraries](https://img.shields.io/badge/libraries-Tkinter%2C%20NetworkX%2C%20Matplotlib-orange.svg)

A simple Python desktop application using Tkinter, NetworkX, and Matplotlib to visualize common graph algorithms studied in Design and Analysis of Algorithms (DAA).

## Purpose

This tool aims to provide an interactive way for students and learners to understand how various graph algorithms work by visualizing their execution step-by-step (currently shows final result) on user-defined graphs. It transforms abstract algorithmic concepts into tangible visual representations.

## Features

* **Graphical User Interface (GUI):** Built with Tkinter for easy interaction.
* **Graph Input:** Define graph nodes and edges (weighted or unweighted) via a simple text input format.
* **Algorithm Selection:** Choose from a list of common DAA graph algorithms:
    * Breadth-First Search (BFS)
    * Depth-First Search (DFS)
    * Dijkstra's Shortest Path Algorithm
    * Kruskal's Minimum Spanning Tree (MST) Algorithm
    * Prim's Minimum Spanning Tree (MST) Algorithm
* **Parameter Input:** Specify necessary parameters like source and target nodes for relevant algorithms.
* **Graph Visualization:** Displays the input graph using Matplotlib embedded within the Tkinter window.
* **Result Highlighting:** Visually highlights the output of the selected algorithm (e.g., traversed edges, shortest path nodes/edges, MST edges) on the graph display.

## Technology Stack

* **Python:** Core programming language.
* **Tkinter:** Standard Python library for creating the GUI.
* **NetworkX:** Library for creating, manipulating, and studying graph structures and implementing graph algorithms.
* **Matplotlib:** Library for plotting and embedding the graph visualization within the GUI.

## Prerequisites

* Python 3.x installed on your system.
* `pip` (Python package installer)

## Installation

1.  **Clone the repository (or download the script):**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```
    Alternatively, download the `graph_visualizer.py` script directly.

2.  **Install required libraries:**
    ```bash
    pip install networkx matplotlib
    ```
    (Tkinter is usually included with Python)

## How to Run

Navigate to the directory containing the script and run:

```bash
python graph_visualizer.py

How to Use
Launch the application.

Enter Graph Data: In the "Graph Data" text area, input the edges of your graph, one per line.

Format for unweighted edges: node1 node2

Format for weighted edges: node1 node2 weight

Example:

A B 4
A C 2
B C 5
B D 10
C E 3
E D 4
D F 11

Select Algorithm: Choose the algorithm you want to visualize from the dropdown menu.

Enter Parameters:

If using BFS, DFS, Dijkstra, or Prim, enter the starting node in the "Source Node" field.

If using Dijkstra, enter the destination node in the "Target Node" field.

Run: Click the "Run Algorithm" button.

View Results: The graph will be displayed in the lower panel.

The base graph nodes are light blue, edges are gray. Source node is light green, target node is salmon.

Algorithm results are highlighted:

BFS/DFS edges: Blue

Dijkstra path nodes: Orange, path edges: Red

Kruskal/Prim MST edges: Green

Edge weights (if provided) are shown on the edges.

The plot title indicates the algorithm run and may show results like path length or MST weight.

Use the Matplotlib toolbar below the graph to zoom, pan, or save the image.

Example Usage (Dijkstra)
Graph Data:

A B 4
A C 2
B C 5
B D 10
C E 3
E D 4
D F 11

Algorithm: Dijkstra

Source Node: A

Target Node: D

Result: The graph will show the path A -> C -> E -> D highlighted in orange (nodes) and red (edges), with a total path length of 9 displayed in the title.

Potential Enhancements
Improved error handling and user feedback.

Step-by-step algorithm animation instead of just showing the final result.

Addition of more DAA algorithms (e.g., Bellman-Ford, Topological Sort, Connected Components).

Option to choose different graph layout algorithms (e.g., circular, kamada-kawai).

Interactive features (e.g., clicking nodes/edges for info, dragging nodes).

UI improvements (e.g., using themes or alternative GUI frameworks like PySide).
