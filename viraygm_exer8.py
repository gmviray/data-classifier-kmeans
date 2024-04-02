import math
import random
import tkinter as tk
import tkinter.scrolledtext as st
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to read data from a CSV file
def read_csv_file(file):
    lines = file.read().split("\n")
    attributes = lines[0].split(",")
    data_points = [list(map(float, line.split(","))) for line in lines[1:] if line]
    return attributes, data_points

def reset_dropdowns():
    var_attr1.set(attributes[0])
    var_attr2.set(attributes[1])
    var_k_value.set(3)

def clear_text_area():
    text_area_output.delete('1.0', tk.END)

# Open CSV file and read data
file = open("Wine.csv")
attributes, data_points = read_csv_file(file)

# Create Tkinter window
root = tk.Tk()
root.title("K-MEANS CLUSTERING")
window_width, window_height = 900, 600
root.geometry(f"{window_width}x{window_height}")
root.config(bg="lightpink")
root.resizable(False, False)

# Frame for input controls
frame_input = tk.Frame(root, padx=20, pady=20, height=600, bg="lightpink")
frame_input.grid(column=0, row=0, sticky="nswe")

# Label and dropdown for selecting Attribute 1
label_attr1 = tk.Label(frame_input, text="SELECT ATTRIBUTE 1", anchor="w", justify="left", bg="lightpink", font=("Arial", 9, "bold"))
label_attr1.grid(column=0, row=0, sticky="w")

var_attr1 = tk.StringVar(frame_input)
var_attr1.set(attributes[0])

# a tkinter option menu (frame_input as its parent, var_attr1 as its variable, and the list of options)
menu_attr1 = tk.OptionMenu(frame_input, var_attr1, *attributes)
menu_attr1.config(width=15, background="lightpink", font=("Arial", 8, "bold"))
menu_attr1.grid_propagate(0)
menu_attr1.grid(column=1, row=0)

# Label and dropdown for selecting Attribute 2
label_attr2 = tk.Label(frame_input, text="SELECT ATTRIBUTE 2", anchor="w", justify="left", bg="lightpink", font=("Arial", 9, "bold"))
label_attr2.grid(column=0, row=1, sticky="w")

var_attr2 = tk.StringVar(frame_input)
var_attr2.set(attributes[1])

# a tkinter option menu (frame_input as its parent, var_attr2 as its variable, and the list of options)
menu_attr2 = tk.OptionMenu(frame_input, var_attr2, *attributes)
menu_attr2.config(width=15, background="lightpink", font=("Arial", 8, "bold"))
menu_attr2.grid_propagate(0)
menu_attr2.grid(column=1, row=1)

# Label and dropdown for selecting K Value
label_k_value = tk.Label(frame_input, text="SELECT K VALUE", anchor="w", justify="left", bg="lightpink", font=("Arial", 9, "bold"))
label_k_value.grid(column=0, row=2, sticky="w")

var_k_value = tk.StringVar(frame_input)
var_k_value.set(3)

# a tkinter option menu (frame_input as its parent, var_k_value as its variable, and the list of options)
menu_k_value = tk.OptionMenu(frame_input, var_k_value, *[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
menu_k_value.config(width=15, background="lightpink", font=("Arial", 8, "bold"))
menu_k_value.grid_propagate(0)
menu_k_value.grid(column=1, row=2)

# Frame for displaying output
frame_output = tk.Frame(root, height=600, bg="lightpink")
frame_output.grid(column=1, row=0, sticky="nswe")

# Function to perform k-means clustering and display results
def run_kmeans():
    # get attributes and chosen k from dropdowns
    attr1_index = attributes.index(var_attr1.get())
    attr2_index = attributes.index(var_attr2.get())
    k_value = int(var_k_value.get())

    # initialize lists
    centroids = []
    new_centroids = []
    clusters = []
    selected = []

    # Initialize centroids randomly, iterate through the number of clusters
    for i in range(k_value):
        centroid = []

        # generate random index until a centroid is found
        while True:
            random_index = random.randint(1, len(data_points) - 1)

            # checks if it is already chosen as a centroid
            if random_index not in selected:
                selected.append(random_index)
                break

        # append to centroid pair list
        centroid.append(data_points[random_index][attr1_index])
        centroid.append(data_points[random_index][attr2_index])

        # append centroid to the list of centroids
        centroids.append(centroid)
        new_centroids.append([])
        clusters.append([])

    # Perform k-means clustering
    while True:
        # iterate through each data point
        for point in data_points:

            # list of selected attributes
            data_point = [point[attr1_index], point[attr2_index]]

            # initialize variables to find the nearest centroid
            min_distance = float('inf')
            cluster_index = -1

            # iterate through each centroid
            for i in range(len(centroids)):

                # euclidean distance between the data point and the centroid
                distance = math.sqrt((data_point[0] - centroids[i][0])**2 + (data_point[1] - centroids[i][1])**2)

                # update distance if it is smaller than the current minimum distance
                if distance < min_distance:
                    min_distance = distance
                    cluster_index = i

            # append data point to the cluster
            clusters[cluster_index].append(data_point)

        # update the centroids based on the assigned data points
        for i in range(len(new_centroids)):
            new_centroids[i].append(sum([p[0] for p in clusters[i]]) / len(clusters[i]))
            new_centroids[i].append(sum([p[1] for p in clusters[i]]) / len(clusters[i]))

        # check for convergence
        if centroids != new_centroids:
            for i in range(k_value):
                centroids[i] = new_centroids[i].copy()
                new_centroids[i].clear()
                clusters[i].clear()
        else:
            break

    # set up matplotlib figure and scatter plot
    fig = Figure(figsize=(4.5, 4.5), dpi=100)
    scatter_plot = fig.add_subplot(111)

    # scatter plot for each cluster
    for cluster_points in clusters:
        scatter_plot.scatter([point[0] for point in cluster_points], [point[1] for point in cluster_points])
    scatter_plot.set_xlabel(attributes[attr1_index])
    scatter_plot.set_ylabel(attributes[attr2_index])

    # display matplotlib figure in tkinter window
    canvas = FigureCanvasTkAgg(fig, master=frame_output)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)

    # write output to a file
    output_file = open("output.csv", "w")
    output_text = ""
    output_file.write("ATTR 1: " + attributes[attr1_index] + "\n")
    output_file.write("ATTR 2: " + attributes[attr2_index] + "\n\n")

    output_file.write("n = " + str(k_value) + "\n\n")

    output_file.write("INITIAL CENTROIDS\n")

    for index in range(len(centroids)):
        if index == 0:
            output_file.writelines(f'Initial {centroids[index]}\n')
        elif index == 1:
            output_file.writelines(f'2nd centroids {centroids[index]}\n')
        elif index == 2:
            output_file.writelines(f'3rd centroids {centroids[index]}\n')
        else:
            output_file.writelines(f'{index}th centroids {centroids[index]}\n')
        
    output_file.write("\n")

    for i in range(len(centroids)):
        output_file.write(f"Centroid {i}: {centroids[i]}\n")
        output_text += f"Centroid {i}: {centroids[i]}\n"
        for j in range(len(clusters[i])):
            output_file.write(f"{clusters[i][j]}\n")
            output_text += f"{clusters[i][j]}\n"
        output_file.write("\n")
        output_text += "\n"

    # display output in scrolled text area
    text_area_output.delete('1.0', tk.END)
    text_area_output.insert(tk.INSERT, output_text)

# button to run
button_run = tk.Button(frame_input, text="RUN", command=run_kmeans, width=10, bg="#9E4244", font=("Arial", 10, "bold"), fg="White")
button_run.grid(column=0, row=3, sticky="w")

# button to reset
button_reset = tk.Button(frame_input, text="RESET", command=lambda: [clear_text_area(), reset_dropdowns()], width=10, bg="#9E4244", font=("Arial", 10, "bold"), fg="White")
button_reset.grid(column=0, row=4, sticky="w")

# displaying centroids and clusters
label_output = tk.Label(frame_input, text="CENTROIDS AND CLUSTERS", anchor="e", bg="lightpink", font=("Arial", 9, "bold"))
label_output.grid(column=1, row=4, sticky="e")

text_area_output = st.ScrolledText(frame_input, width=50, height=26, font=("Consolas", 10))
text_area_output.grid(column=0, pady=10, padx=10, columnspan=2)

# Start the Tkinter main loop
root.mainloop()
