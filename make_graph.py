import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib.markers import MarkerStyle

output_filename = "cvxpy_graph.png"

import seaborn as sns

import csv

def plot_one_experiment_line(results, line_name, mark, fill, color):
	print(results)

	meanx = []
	meany = []

	for m in results.keys():
		time = results[m]

		meanx.append(m)
		meany.append(time)

	sns.lineplot(x=meanx, y=meany, marker=MarkerStyle(mark, fillstyle=fill), color=color, label=line_name, markersize=10)#, edgecolor="black")


with open("cvxpy_results.csv", 'r') as f:
	reader = csv.reader(f)
	res = {}
	for row in reader:
		n = int(row[0])
		m = int(row[1])
		time = float(row[3])

		if n not in res.keys():
			res[n] = {}
		res[n][m] = time

	print (res)

	plot_one_experiment_line(res[10], "10 assets", "D", "full", "tab:blue")
	plot_one_experiment_line(res[20], "20 assets", "D", "full", "tab:red")
	plot_one_experiment_line(res[50], "50 assets", "D", "full", "tab:green")

plt.xscale('log')
plt.yscale('log')
plt.axis([100,50000,0.001, 300])
plt.xlabel("Number of Offers")
plt.ylabel("Time (s)")

plt.legend()


plt.savefig(output_filename)
