import customtkinter
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import queue
import time

customtkinter.set_appearance_mode("light")

# Whole GUI window
window = customtkinter.CTk()
window.geometry("1000x700")
window.title("Laboratory 5")

######################################################

# For creating the left-side bar menu

menu_frame = customtkinter.CTkFrame(
    window, fg_color="#AAAAAA", width=300)
menu_frame.pack(pady=10, padx=10, side="left", fill="y")

######################################################

# Label for search algorithm options

search_type = customtkinter.CTkLabel(
    menu_frame, text="Searching Algorithm Type", text_color="white", font=("Circular", 13, "bold"))
search_type.pack(pady=10, padx=5)

search_algorithms = customtkinter.CTkComboBox(menu_frame, values=[
                                              "Depth-first Search", "Breadth-first Search", "Hill Climbing", "Beam Search", "Branch and Bound", "A*"])
search_algorithms.set("Depth-first Search")  # Set the default selection
search_algorithms.pack(pady=5, padx=10)

########################################################

# Buttons for searching, stopping, pausing, and resuming of the simulation

search_button = customtkinter.CTkButton(
    menu_frame, text="Search", fg_color="#E8E6E6", text_color="black")
search_button.pack(pady=10, padx=5)
stop_button = customtkinter.CTkButton(
    menu_frame, text="Stop", fg_color="#E8E6E6", text_color="black")
stop_button.pack(padx=10)
pause_button = customtkinter.CTkButton(
    menu_frame, text="Pause", fg_color="#E8E6E6", text_color="black")
pause_button.pack(pady=10, padx=10)
resume_button = customtkinter.CTkButton(
    menu_frame, text="Resume", fg_color="#E8E6E6", text_color="black")
resume_button.pack(padx=10)

#########################################################

# For setting up the random graph

set_label = customtkinter.CTkLabel(
    menu_frame, text="Create Random Graph", text_color="white", font=("Circular", 13, "bold"))
set_label.pack(pady=15)

node_l = customtkinter.CTkLabel(
    menu_frame, text="Nodes", text_color="white", font=("Circular", 12))
node_l.pack(padx=5)

node_inpt = customtkinter.CTkEntry(menu_frame)
node_inpt.pack()

edge_l = customtkinter.CTkLabel(
    menu_frame, text="Edges", text_color="white", font=("Circular", 12))
edge_l.pack(padx=5)

edge_inpt = customtkinter.CTkEntry(menu_frame)
edge_inpt.pack()

# For the Start and End nodes

start_node_label = customtkinter.CTkLabel(
    menu_frame, text="Start Node", text_color="white", font=("Circular", 12))
start_node_label.pack()

start_node_input = customtkinter.CTkEntry(menu_frame)
start_node_input.pack()

goal_node_label = customtkinter.CTkLabel(
    menu_frame, text="Goal Node", text_color="white", font=("Circular", 12))
goal_node_label.pack()

goal_node_input = customtkinter.CTkEntry(menu_frame)
goal_node_input.pack()

reset_button = customtkinter.CTkButton(
    menu_frame, text="Reset Graph", fg_color="#E8E6E6", text_color="black")
reset_button.pack(pady=10)

#####################################################

# Frame for the display window of the graph

frame = customtkinter.CTkFrame(window)
frame.pack(pady=20, padx=20, fill="both", expand=True)

#####################################################

# Functions for the searching algorithms


def bfs_search(graph, start_node, goal_node):  # Breadth-first search
    visited = set()
    q = queue.Queue()
    q.put(start_node)
    order = []

    while not q.empty():
        vertex = q.get()
        if vertex not in visited:
            order.append(vertex)
            visited.add(vertex)
            print(f"Visiting Node: {vertex}")  # Display visiting node
            if vertex == goal_node:
                # Display goal node found
                print(f"Goal Node {goal_node} found!")
                break
            for node in graph[vertex]:
                if node not in visited:
                    q.put(node)

    return order


def dfs_search(graph, start_node, goal_node):  # Depth-first search
    visited = set()
    stack = [start_node]
    order = []

    while stack:
        current_node = stack.pop()
        if current_node not in visited:
            visited.add(current_node)
            order.append(current_node)
            print(f"Visited Node: {current_node}")  # Display visiting node
            if current_node == goal_node:
                print(f"Goal Node {goal_node} found!")
                break
            stack.extend(
                neigh for neigh in graph[current_node] if neigh not in visited)

    return order

#######################################################

# Functions for generating random graph for searching


def generate_random_graph(node, edge):
    while True:
        G = nx.gnm_random_graph(node, edge)
        if nx.is_connected(G):
            return G


canvas = None


def visualize_search(order, G, pos, goal_node):
    global canvas
    if canvas is not None:
        plt.clf()  # Clear the current figure
    fig, ax = plt.subplots(figsize=(5, 4))
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill='both', expand=True)

    for i, node in enumerate(order, start=1):
        colors = ['g' if n == goal_node else 'r' if n in order[:i]
                  else '#86C7F3' for n in G.nodes]
        nx.draw(G, pos, ax=ax, with_labels=True,
                node_size=700, node_color=colors)
        canvas.draw()
        plt.pause(1.8)


def reset_graph():
    global canvas
    # Clear the canvas
    if canvas:
        plt.clf()  # Clear the current figure
        canvas.get_tk_widget().destroy()
        canvas = None


#####################################################

# For getting the input value for nodes, edges, start, and end node


def get_node():
    input_value = node_inpt.get()
    if input_value.isdigit():
        return int(input_value)


def get_edge():
    input_value = edge_inpt.get()
    if input_value.isdigit():
        return int(input_value)


def get_start_node():
    input_value = start_node_input.get()
    if input_value.isdigit():
        return int(input_value)


def get_goal_node():
    input_value = goal_node_input.get()
    if input_value.isdigit():
        return int(input_value)


# Function for button click on search

def on_search_button_click():
    selected_algorithm = search_algorithms.get()
    num_of_node = get_node()
    num_of_edge = get_edge()
    start_node = get_start_node()
    goal_node = get_goal_node()

    if selected_algorithm == "Breadth-first Search":
        if start_node is not None and goal_node is not None:
            if num_of_node is not None and num_of_edge is not None:
                G = generate_random_graph(num_of_node, num_of_edge)
                if G is not None:
                    pos = nx.spring_layout(G)
                    visualize_search(bfs_search(
                        G, start_node, goal_node), G, pos, goal_node)
    elif selected_algorithm == "Depth-first Search":
        if start_node is not None and goal_node is not None:
            if num_of_node is not None and num_of_edge is not None:
                G = generate_random_graph(num_of_node, num_of_edge)
                if G is not None:
                    pos = nx.spring_layout(G)
                    visualize_search(dfs_search(
                        G, start_node, goal_node), G, pos, goal_node)


####################################################


#####################################################
label = customtkinter.CTkLabel(
    master=window, text="Searching Algorithms Simulator", font=("Circular", 20, "bold"))
label.pack(pady=10)

# Bind the on_search_button_click function to the search button
search_button.configure(command=on_search_button_click)
reset_button.configure(command=reset_graph)

# Start the GUI main loop
window.mainloop()
