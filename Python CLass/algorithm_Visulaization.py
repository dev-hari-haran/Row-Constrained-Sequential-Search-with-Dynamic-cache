import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class PathVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Pathfinding Visualizer")
        self.root.geometry("1100x750")

        # Config Variables
        self.grid_size = tk.IntVar(value=10)
        self.obs_count = tk.IntVar(value=15)
        self.start_node = None
        self.goal_node = None
        self.obstacles = set()
        
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        sidebar = tk.Frame(self.root, width=280, bg="#2c3e50", padx=20, pady=20)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Base style without font to avoid the "multiple values" error
        base_style = {"bg": "#2c3e50", "fg": "white"}
        
        tk.Label(sidebar, text="GRID CONTROLS", font=("Segoe UI", 14, "bold"), **base_style).pack(pady=(0, 20))

        tk.Label(sidebar, text="Grid Dimension (N):", font=("Segoe UI", 10), **base_style).pack(anchor=tk.W)
        tk.Entry(sidebar, textvariable=self.grid_size, width=15).pack(pady=5)

        tk.Label(sidebar, text="Random Obstacle Count:", font=("Segoe UI", 10), **base_style).pack(anchor=tk.W)
        tk.Entry(sidebar, textvariable=self.obs_count, width=15).pack(pady=5)

        tk.Button(sidebar, text="Reset / New Grid", command=self.reset_graph, bg="#e67e22", fg="white", relief="flat").pack(fill=tk.X, pady=10)

        ttk.Separator(sidebar, orient='horizontal').pack(fill=tk.X, pady=15)

        tk.Label(sidebar, text="INTERACTION MODE", font=("Segoe UI", 10, "bold"), **base_style).pack(anchor=tk.W)
        self.mode_var = tk.StringVar(value="start")
        
        modes = [("Set Start Point", "start"), ("Set Goal Point", "goal"), ("Manual Obstacle", "obstacle")]
        for text, m in modes:
            tk.Radiobutton(sidebar, text=text, variable=self.mode_var, value=m, 
                           bg="#2c3e50", fg="white", selectcolor="#34495e", 
                           activebackground="#2c3e50", activeforeground="white").pack(anchor=tk.W, pady=2)

        tk.Button(sidebar, text="Generate Random Walls", command=self.add_random_obstacles, bg="#95a5a6").pack(fill=tk.X, pady=10)

        ttk.Separator(sidebar, orient='horizontal').pack(fill=tk.X, pady=15)

        tk.Label(sidebar, text="ALGORITHM", font=("Segoe UI", 10, "bold"), **base_style).pack(anchor=tk.W)
        self.algo_var = tk.StringVar(value="A*")
        self.algo_menu = ttk.Combobox(sidebar, textvariable=self.algo_var, 
                                     values=["BFS", "DFS", "Dijkstra", "A*", "Modified A*", "Greedy"])
        self.algo_menu.pack(fill=tk.X, pady=5)

        tk.Button(sidebar, text="START VISUALIZATION", command=self.visualize, 
                  bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"), height=2).pack(fill=tk.X, pady=25)

        # Plotting Area
        self.fig, self.ax = plt.subplots(figsize=(7, 7), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        
        self.reset_graph()

    def reset_graph(self):
        self.start_node = None
        self.goal_node = None
        self.obstacles = set()
        self.update_plot()

    def on_click(self, event):
        if event.xdata is None or event.ydata is None: return
        x, y = int(round(event.xdata)), int(round(event.ydata))
        N = self.grid_size.get()

        if 0 <= x < N and 0 <= y < N:
            node = (x, y)
            mode = self.mode_var.get()
            if mode == "start":
                self.start_node = node
                if node in self.obstacles: self.obstacles.remove(node)
            elif mode == "goal":
                self.goal_node = node
                if node in self.obstacles: self.obstacles.remove(node)
            elif mode == "obstacle":
                if node != self.start_node and node != self.goal_node:
                    if node in self.obstacles: self.obstacles.remove(node)
                    else: self.obstacles.add(node)
            self.update_plot()

    def add_random_obstacles(self):
        N = self.grid_size.get()
        self.obstacles = set()
        all_nodes = [(x, y) for x in range(N) for y in range(N)]
        all_nodes = [n for n in all_nodes if n != self.start_node and n != self.goal_node]
        num_obs = min(self.obs_count.get(), len(all_nodes))
        self.obstacles.update(random.sample(all_nodes, num_obs))
        self.update_plot()

    def update_plot(self, path=None):
        self.ax.clear()
        N = self.grid_size.get()
        pos = {(x, y): (x, y) for x in range(N) for y in range(N)}
        G_full = nx.grid_2d_graph(N, N)

        # Background Grid
        nx.draw_networkx_nodes(G_full, pos, ax=self.ax, node_size=10, node_color='#ecf0f1')
        nx.draw_networkx_edges(G_full, pos, ax=self.ax, edge_color='#ecf0f1', alpha=0.3)

        # Obstacles
        if self.obstacles:
            nx.draw_networkx_nodes(G_full, pos, nodelist=list(self.obstacles), 
                                   ax=self.ax, node_size=120, node_color='#2c3e50', node_shape='s')
        # Path
        if path:
            edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G_full, pos, edgelist=edges, ax=self.ax, width=3, edge_color='#3498db')
            nx.draw_networkx_nodes(G_full, pos, nodelist=path, ax=self.ax, node_size=50, node_color='#3498db')

        # Start/Goal
        if self.start_node:
            nx.draw_networkx_nodes(G_full, pos, nodelist=[self.start_node], ax=self.ax, node_size=200, node_color='#2ecc71')
        if self.goal_node:
            nx.draw_networkx_nodes(G_full, pos, nodelist=[self.goal_node], ax=self.ax, node_size=200, node_color='#e74c3c')

        self.ax.set_xlim(-0.5, N - 0.5)
        self.ax.set_ylim(-0.5, N - 0.5)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.canvas.draw()

    def visualize(self):
        if not self.start_node or not self.goal_node:
            messagebox.showwarning("Incomplete", "Set Start and Goal nodes first.")
            return

        N = self.grid_size.get()
        G = nx.grid_2d_graph(N, N)
        G.remove_nodes_from(self.obstacles)

        algo = self.algo_var.get()
        try:
            if algo == "BFS":
                path = nx.shortest_path(G, self.start_node, self.goal_node)
            elif algo == "Dijkstra":
                path = nx.dijkstra_path(G, self.start_node, self.goal_node)
            elif algo == "A*":
                path = nx.astar_path(G, self.start_node, self.goal_node, 
                                     heuristic=lambda a, b: abs(a[0]-b[0]) + abs(a[1]-b[1]))
            elif algo == "Modified A*":
                path = nx.astar_path(G, self.start_node, self.goal_node, 
                                     heuristic=lambda a, b: 3.0 * (abs(a[0]-b[0]) + abs(a[1]-b[1])))
            elif algo == "Greedy":
                path = self.run_greedy(G)
            else: # DFS or fallback
                path = nx.shortest_path(G, self.start_node, self.goal_node)
            
            self.update_plot(path)
        except nx.NetworkXNoPath:
            messagebox.showinfo("No Path", "Goal is unreachable!")

    def run_greedy(self, G):
        path, current, visited = [self.start_node], self.start_node, {self.start_node}
        while current != self.goal_node:
            neighbors = [n for n in G.neighbors(current) if n not in visited]
            if not neighbors: raise nx.NetworkXNoPath
            current = min(neighbors, key=lambda n: abs(n[0]-self.goal_node[0]) + abs(n[1]-self.goal_node[1]))
            path.append(current)
            visited.add(current)
        return path

if __name__ == "__main__":
    root = tk.Tk()
    app = PathVisualizer(root)
    root.mainloop()
