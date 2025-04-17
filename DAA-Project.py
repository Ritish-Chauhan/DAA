# [cite: 68] Python
import tkinter as tk
from tkinter import ttk, messagebox # [cite: 125, 126, 127, 128, 129, 175] Import messagebox for error/info display
import networkx as nx
import matplotlib
matplotlib.use('TkAgg') # [cite: 68, 81] Set backend BEFORE importing pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # [cite: 68, 82] Add NavigationToolbar2Tk if needed

class GraphVisualizerApp:
    # [cite: 68] def __init__(self, master):
    def __init__(self, master): # [cite: 159] Initializes the main window/frame...
        self.master = master
        master.title("DAA Graph Algorithm Visualizer") # [cite: 68]
        master.geometry("900x700") # [cite: 68] Initial size (adjusted for better layout)

        # -- Main Frames --- # [cite: 68]
        # Frame for controls (top) # [cite: 68]
        self.control_frame = ttk.Frame(master, padding="10") # [cite: 68]
        self.control_frame.pack(side=tk.TOP, fill=tk.X) # [cite: 68]

        # Frame for visualization (bottom) # [cite: 68]
        self.vis_frame = ttk.Frame(master, padding="10") # [cite: 68]
        self.vis_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) # [cite: 68]

        # --- Initialize Graph and Plot --- # [cite: 68]
        self.graph = nx.Graph() # [cite: 68, 85] Or nx.DiGraph() if directed needed initially
        self.pos = None # [cite: 68, 157] To store node positions
        self.edge_labels = {} # To store edge weights for drawing

        # --- Setup GUI elements --- # [cite: 68]
        self.setup_gui() # [cite: 68, 159]

        # --- Initialize Matplotlib Embedding --- # [cite: 161]
        self.setup_matplotlib_canvas() # [cite: 80]

    # [cite: 160] Creates and places all the Tkinter widgets...
    def setup_gui(self): # [cite: 68, 72]
        # Use grid layout manager for more control within control_frame [cite: 70]
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=0) # For potential scrollbar
        self.control_frame.columnconfigure(2, weight=1)
        self.control_frame.columnconfigure(3, weight=1)

        # --- Graph Input --- # [cite: 72]
        ttk.Label(self.control_frame, text="Graph Data (Edges: u v [weight], one per line):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2) # [cite: 73]
        self.graph_input_text = tk.Text(self.control_frame, height=8, width=40) # [cite: 73] Increased height
        self.graph_input_text.grid(row=1, column=0, padx=5, pady=2, rowspan=4, sticky="nsew") # [cite: 73] Use rowspan and sticky
        # Add a scrollbar for the Text widget [cite: 73]
        text_scrollbar = ttk.Scrollbar(self.control_frame, orient=tk.VERTICAL, command=self.graph_input_text.yview) # [cite: 73]
        self.graph_input_text['yscrollcommand'] = text_scrollbar.set # [cite: 73]
        text_scrollbar.grid(row=1, column=1, sticky='ns', rowspan=4) # [cite: 73]

        # --- Algorithm Selection --- # [cite: 74]
        ttk.Label(self.control_frame, text="Select Algorithm:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2) # [cite: 75]
        self.algorithm_var = tk.StringVar()
        # [cite: 5] Algorithm list
        algo_list = ["BFS", "DFS", "Dijkstra", "Kruskal", "Prim"]
        self.algorithm_combobox = ttk.Combobox(self.control_frame, # [cite: 74]
                                               textvariable=self.algorithm_var,
                                               values=algo_list, # [cite: 76]
                                               state='readonly') # Prevent user typing random text
        self.algorithm_combobox.grid(row=1, column=2, columnspan=2, padx=5, pady=2, sticky="ew") # [cite: 76] Use columnspan and sticky
        if algo_list:
             self.algorithm_combobox.current(0) # [cite: 76] Set default selection

        # --- Additional Inputs (Source/Target Nodes) --- # [cite: 77]
        ttk.Label(self.control_frame, text="Source Node:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2) # [cite: 78]
        self.source_entry = ttk.Entry(self.control_frame, width=15) # [cite: 78] Adjusted width
        self.source_entry.grid(row=2, column=3, padx=5, pady=2, sticky="ew") # [cite: 78]

        ttk.Label(self.control_frame, text="Target Node:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=2) # [cite: 78]
        self.target_entry = ttk.Entry(self.control_frame, width=15) # [cite: 78] Adjusted width
        self.target_entry.grid(row=3, column=3, padx=5, pady=2, sticky="ew") # [cite: 78]

        # --- Execution Button --- # [cite: 79]
        self.run_button = ttk.Button(self.control_frame, text="Run Algorithm",
                                     command=self.run_algorithm) # [cite: 79, 123] Links button to run_algorithm
        self.run_button.grid(row=4, column=2, columnspan=2, pady=10, padx=5, sticky="ew") # [cite: 79]

    # [cite: 80] Setup method for Matplotlib canvas
    def setup_matplotlib_canvas(self):
        self.fig = Figure(figsize=(7, 6), dpi=100) # [cite: 80] Create Matplotlib Figure
        self.ax = self.fig.add_subplot(111) # [cite: 80, 81] Add Axes
        self.ax.set_title("Graph Visualization") # [cite: 80]
        self.ax.axis('off') # [cite: 80] Hide axes ticks/spines initially

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.vis_frame) # [cite: 80, 82] Create Tkinter Canvas
        self.canvas_widget = self.canvas.get_tk_widget() # [cite: 82] Get the Tkinter-compatible widget
        # [cite: 82] Pack or grid this widget into the vis_frame
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # [cite: 80] Optional: Add Matplotlib Navigation Toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.vis_frame) # [cite: 80, 83]
        toolbar.update() # [cite: 80]
        # self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True) # [cite: 80] Canvas packed before toolbar for typical layout

        self.canvas.draw() # [cite: 80, 82] Initial draw (often blank)

    # [cite: 91] Parsing method called by run_algorithm.
    def parse_graph_input(self): # [cite: 92]
        self.graph.clear() # [cite: 92, 161] Clear previous graph data
        self.edge_labels.clear() # Clear previous edge labels
        graph_data_string = self.graph_input_text.get("1.0", tk.END) # [cite: 92]
        lines = graph_data_string.strip().split('\n') # [cite: 92]
        edges_to_add = [] # [cite: 92]
        has_weights = False # [cite: 92] Flag to track if any weights are provided

        for line_num, line in enumerate(lines): # [cite: 92]
            parts = line.strip().split() # [cite: 92]
            if not parts:
                continue # Skip empty lines [cite: 92]

            try: # [cite: 96] Use a try-except block
                if len(parts) == 2: # [cite: 95] Parse unweighted edges
                    u, v = parts
                    edges_to_add.append((u, v)) # [cite: 92]
                elif len(parts) == 3: # [cite: 95] Parse weighted edges
                    u, v, weight_str = parts # [cite: 93]
                    weight = float(weight_str) # [cite: 93, 97] Convert weight to float
                    edges_to_add.append((u, v, {'weight': weight})) # [cite: 93] Add edge with weight attribute
                    self.edge_labels[(u,v)] = weight # Store for drawing
                    has_weights = True # [cite: 93]
                else:
                    # Handle incorrect format for this line [cite: 93]
                    print(f"Warning: Skipping malformed line {line_num+1}: '{line}'") # [cite: 93]
                    # Optionally show error to user via messagebox [cite: 93]
                    messagebox.showwarning("Parsing Warning", f"Skipping malformed line {line_num+1}: '{line}'.\nExpected format: u v [weight]")
                    continue
            except ValueError: # [cite: 97] Handle non-numeric weight
                 print(f"Warning: Skipping line {line_num+1} due to non-numeric weight: '{line}'") # [cite: 93]
                 messagebox.showwarning("Parsing Warning", f"Skipping line {line_num+1} due to non-numeric weight: '{line}'.")
                 continue
            except Exception as e: # [cite: 93]
                 print(f"Error parsing line {line_num+1}: {e}") # [cite: 93]
                 messagebox.showerror("Parsing Error", f"Error parsing line {line_num+1}: {e}")
                 return False # [cite: 93] Indicate parsing failure

        # Add edges to the graph
        try:
            # add_edges_from handles the attribute dict correctly [cite: 94]
            self.graph.add_edges_from(edges_to_add) # [cite: 94, 98]
            # Nodes are added automatically when edges are added [cite: 94, 99]
            print(f"Graph parsed: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges.") # [cite: 94]
            return True # [cite: 94, 100] Indicate parsing success
        except Exception as e:
            print(f"Error adding edges to graph: {e}") # [cite: 94]
            messagebox.showerror("Graph Error", f"Error adding edges to graph: {e}") # [cite: 94]
            return False # [cite: 94, 100] Indicate parsing failure

    # [cite: 123] Central coordinator method linked to the button
    # [cite: 162] Orchestrates getting user input, calling parse_graph_input, executing algorithm...
    def run_algorithm(self): # [cite: 124]
        # 1. Get user selections # [cite: 124]
        selected_algo = self.algorithm_var.get() # [cite: 124]
        source_node = self.source_entry.get().strip() # [cite: 124]
        target_node = self.target_entry.get().strip() # [cite: 124]

        # 2. Parse graph data # [cite: 124]
        if not self.parse_graph_input(): # [cite: 124]
            # Parsing failed, error message already shown in parse_graph_input
            # tk.messagebox.showerror("Error", "Failed to parse graph input. Please check format.") # [cite: 124] Handled in parser
            self.update_visualization() # Update viz to show potentially cleared graph
            return # [cite: 124]

        # Check if graph is empty # [cite: 124]
        if not self.graph: # [cite: 124]
            tk.messagebox.showwarning("Warning", "Graph is empty. Please enter graph data.") # [cite: 124]
            self.update_visualization() # Update viz to show empty state
            return # [cite: 124]

        # 3. Validate inputs (basic example) # [cite: 125]
        if selected_algo in ["BFS", "DFS", "Dijkstra", "Prim"] and not source_node: # [cite: 125] (Prim also often needs a source)
             tk.messagebox.showerror("Input Error", f"Source node required for {selected_algo}.") # [cite: 125]
             return # [cite: 126]

        if selected_algo == "Dijkstra" and not target_node: # [cite: 126]
             tk.messagebox.showerror("Input Error", f"Target node required for {selected_algo}.") # [cite: 126]
             return # [cite: 126]

        # Validate if nodes exist in the graph [cite: 129]
        if source_node and source_node not in self.graph: # [cite: 126]
             tk.messagebox.showerror("Input Error", f"Source node '{source_node}' not found in graph.") # [cite: 126]
             return # [cite: 126]

        if target_node and target_node not in self.graph: # [cite: 126]
             tk.messagebox.showerror("Input Error", f"Target node '{target_node}' not found in graph.") # [cite: 126]
             return # [cite: 126]

        # Check if graph is connected for algorithms that need it (optional, can be complex)

        # 4. Execute selected algorithm # [cite: 126]
        results = None
        try: # [cite: 129] Use try-except for algorithm execution
            if selected_algo == "BFS": # [cite: 126]
                # [cite: 112] To get the edges traversed: edges = list(nx.bfs_edges(self.graph, source=start_node))
                results = list(nx.bfs_edges(self.graph, source=source_node)) # [cite: 126]
            elif selected_algo == "DFS": # [cite: 126]
                # [cite: 114] To get the edges traversed: edges = list(nx.dfs_edges(self.graph, source=start_node))
                results = list(nx.dfs_edges(self.graph, source=source_node)) # [cite: 126]
            elif selected_algo == "Dijkstra": # [cite: 126]
                # Ensure graph has weights or handle appropriately # [cite: 126] Check if 'weight' attribute exists needed
                results = nx.dijkstra_path(self.graph, source=source_node, target=target_node, weight='weight') # [cite: 116, 126]
            elif selected_algo == "Kruskal": # [cite: 126]
                # Ensure graph is undirected and has weights # [cite: 126] nx.Graph handles undirected
                # [cite: 118] Get MST edges directly: mst_edges = list(nx.minimum_spanning_edges(...))
                results = list(nx.minimum_spanning_edges(self.graph, algorithm='kruskal', weight='weight', data=False)) # [cite: 118, 126]
            elif selected_algo == "Prim": # [cite: 126]
                # Ensure graph is undirected and has weights # [cite: 126]
                # Prim needs a starting node if graph is not connected, but minimum_spanning_edges handles this. [cite: 127]
                # We pass the user source_node to the algorithm, which might be used as starting point internally if graph disconnected
                results = list(nx.minimum_spanning_edges(self.graph, algorithm='prim', weight='weight', data=False, ignore_nan=True)) # Added ignore_nan, specify source if needed for disconnected behavior
                # Note: NetworkX's Prim implementation (via minimum_spanning_edges) doesn't directly take a start node parameter in the same way as some textbook algorithms.
                # It typically finds the MST for the component containing an arbitrary node if the graph is disconnected.
                # For visualizing Prim's *process* from a specific node, a step-by-step implementation would be needed. [cite: 177]
            else:
                tk.messagebox.showwarning("Warning", f"Algorithm '{selected_algo}' selection not recognized or not yet implemented.") # [cite: 127]
                return

        except nx.NetworkXNoPath: # [cite: 127, 129] Handle no path error
            tk.messagebox.showinfo("Info", f"No path found between {source_node} and {target_node}.") # [cite: 127]
            # Still update visualization to show the base graph
            self.update_visualization(algorithm_results=None, algorithm_name=selected_algo) # [cite: 128] Show graph without path
            return # [cite: 128]
        except nx.NodeNotFound as e: # [cite: 128, 129] Handle missing node error during algorithm run
            tk.messagebox.showerror("Algorithm Error", f"Node not found during algorithm execution: {e}") # [cite: 128]
            return # [cite: 128]
        except nx.NetworkXError as e: # Catch other NetworkX specific errors (e.g., weight missing)
            tk.messagebox.showerror("Algorithm Error", f"NetworkX algorithm error: {e}\nCheck if weights are provided for weighted algorithms.")
            print(f"Algorithm Error: {e}")
            return
        except Exception as e: # [cite: 128] Catch generic errors
            tk.messagebox.showerror("Error", f"Algorithm execution failed: {e}") # [cite: 128]
            print(f"Algorithm Error: {e}") # [cite: 128]
            return # [cite: 128]

        # 5. Update visualization # [cite: 129]
        self.update_visualization(algorithm_results=results, algorithm_name=selected_algo) # [cite: 129, 162] Trigger visualization update


    # [cite: 130] Responsible for redrawing the graph
    # [cite: 163] Responsible for the redraw cycle: clearing the axes... drawing... highlighting... refreshing...
    def update_visualization(self, algorithm_results=None, algorithm_name=None): # [cite: 131]
        # 1. Clear previous drawing # [cite: 131]
        self.ax.cla() # [cite: 131, 137, 163] Clear the axes

        if not self.graph or self.graph.number_of_nodes() == 0: # [cite: 131] If graph is empty after clearing/parsing failure
            self.ax.set_title("Graph Visualization (No Data)") # [cite: 131]
            self.ax.axis('off') # [cite: 131]
            self.canvas.draw() # [cite: 131, 136, 163] Refresh canvas
            return # [cite: 132]

        # 2. Calculate layout (or reuse if desired) # [cite: 132]
        # Recalculate each time unless self.pos is explicitly managed
        try: # [cite: 132]
            # Use a seed for reproducibility [cite: 132, 139]
            if self.pos is None or len(self.pos) != len(self.graph.nodes()): # Recalculate if graph changed significantly
                 self.pos = nx.spring_layout(self.graph, seed=42) # [cite: 132, 138]
        except Exception as e: # [cite: 132] Handle layout errors
            print(f"Layout Error (Spring): {e}. Trying Kamada-Kawai.")
            try: # [cite: 132] Fallback layout
                self.pos = nx.kamada_kawai_layout(self.graph) # [cite: 132]
            except Exception as e2: # [cite: 132] Final fallback
                print(f"Fallback Layout Error (Kamada-Kawai): {e2}. Using random layout.") # [cite: 132]
                self.pos = nx.random_layout(self.graph, seed=42) # [cite: 132]

        # 3. Draw base graph # [cite: 132, 140, 144]
        node_colors = ['lightblue'] * len(self.graph.nodes())
        # Optionally color source/target nodes differently in the base draw
        source_node = self.source_entry.get().strip()
        target_node = self.target_entry.get().strip()
        node_list = list(self.graph.nodes())
        if source_node in self.graph:
             node_colors[node_list.index(source_node)] = 'lightgreen'
        if target_node in self.graph:
             node_colors[node_list.index(target_node)] = 'salmon'


        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax, node_size=500, node_color=node_colors, alpha=0.9) # [cite: 132, 140]
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax, font_size=10) # [cite: 132, 140]
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, edge_color='gray', alpha=0.6, width=1.0) # [cite: 132, 140]
        # Draw edge labels (weights) if they exist
        if self.edge_labels:
             nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=self.edge_labels, ax=self.ax, font_size=8)


        # 4. Apply Highlighting based on results # [cite: 132, 141, 143]
        highlight_edge_color = 'blue'
        highlight_node_color = 'orange'
        highlight_width = 2.5 # [cite: 134, 146]

        if algorithm_results is not None: # [cite: 132] Check if results exist
            if algorithm_name in ["BFS", "DFS"]: # [cite: 132, 148]
                # Highlight traversed edges [cite: 132]
                highlight_edge_color = 'blue'
                nx.draw_networkx_edges(self.graph, self.pos, edgelist=algorithm_results, ax=self.ax,
                                       edge_color=highlight_edge_color, width=highlight_width, alpha=0.8) # [cite: 132, 148]
            elif algorithm_name == "Dijkstra": # [cite: 133, 148]
                # Highlight path nodes and edges [cite: 133]
                # algorithm_results is list of nodes [cite: 133, 149]
                path_nodes = algorithm_results # [cite: 133]
                # [cite: 133, 149] Derive the edges in the path: path_edges = list(zip(path_nodes, path_nodes[1:]))
                path_edges = list(zip(path_nodes, path_nodes[1:])) # [cite: 133, 149]
                highlight_edge_color = 'red' # [cite: 134, 150]
                highlight_node_color = 'orange' # [cite: 133, 150]
                # Highlight path nodes [cite: 133, 150]
                nx.draw_networkx_nodes(self.graph, self.pos, nodelist=path_nodes, ax=self.ax,
                                       node_color=highlight_node_color, node_size=600) # [cite: 133]
                # Highlight path edges [cite: 134, 150]
                nx.draw_networkx_edges(self.graph, self.pos, edgelist=path_edges, ax=self.ax,
                                       edge_color=highlight_edge_color, width=highlight_width, alpha=0.8) # [cite: 134]
            elif algorithm_name in ["Kruskal", "Prim"]: # [cite: 134, 152]
                # Highlight MST edges [cite: 134]
                # algorithm_results is list of edges [cite: 134, 152]
                mst_edges = algorithm_results # [cite: 134]
                highlight_edge_color = 'green' # [cite: 134, 152]
                nx.draw_networkx_edges(self.graph, self.pos, edgelist=mst_edges, ax=self.ax,
                                       edge_color=highlight_edge_color, width=highlight_width, style='solid', alpha=0.8) # [cite: 134, 152]

        # 5. Finalize plot appearance # [cite: 135]
        title = "Graph Visualization"
        if algorithm_name:
            title += f": {algorithm_name} Result" # [cite: 135]
            if algorithm_results is not None:
                 if algorithm_name == "Dijkstra":
                      # Add path length if available (NetworkX doesn't return it with path easily)
                      try:
                           length = nx.dijkstra_path_length(self.graph, source=self.source_entry.get().strip(), target=self.target_entry.get().strip(), weight='weight') # [cite: 117]
                           title += f" (Length: {length:.2f})"
                      except: # Handle cases where length calculation might fail separately
                           pass
                 elif algorithm_name in ["Kruskal", "Prim"]:
                      # Add total weight of MST
                      try:
                           mst_weight = sum(self.graph[u][v].get('weight', 1) for u, v in mst_edges)
                           title += f" (Total Weight: {mst_weight:.2f})"
                      except:
                           pass

        self.ax.set_title(title) # [cite: 135]
        self.ax.axis('off') # [cite: 135] Ensure axes are off

        # 6. Refresh canvas # [cite: 136]
        self.canvas.draw() # [cite: 136, 142, 163, 172] IMPORTANT: Update the embedded plot

# --- Main execution --- # [cite: 69]
if __name__ == "__main__": # [cite: 69]
    root = tk.Tk() # [cite: 69]
    app = GraphVisualizerApp(root) # [cite: 69]
    root.mainloop() # [cite: 69]