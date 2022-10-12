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

	sns.lineplot(meanx, meany, marker=MarkerStyle(mark, fillstyle=fill), color=color, label=line_name, markersize=10)#, edgecolor="black")


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

#input_lines = [
#	("Tâtonnement 10 assets", "sosp_tat_results", "o"),
#	("Convex Solver 10 assets", "cvxpy_results", "+")
#	]


	#plt.scatter(meanx, meany, mark=mark)

#plot_one_experiment_line("CVXPY, 10 Assets", "pricecomp_measurements/cvxpy_10", "D", "left", "tab:blue")
#plot_one_experiment_line("cvxpy 20", "pricecomp_measurements/cvxpy_20", "D", "right", "tab:blue")
#plot_one_experiment_line("cvxpy 50", "pricecomp_measurements/cvxpy_50", "D", "full", "tab:blue")
#plot_one_experiment_line("T\^atonnement, 10 Assets", "pricecomp_measurements/tatonnement_10", "o", "left", "tab:red")
#plot_one_experiment_line("T\^atonnement, 20 Assets", "pricecomp_measurements/tatonnement_20", "o", "right", "tab:red")
#plot_one_experiment_line("T\^atonnement, 50 Assets", "pricecomp_measurements/tatonnement_50", "o", "full", "tab:red")
#for (legend_name, filename, mark) in input_lines:
#	plot_one_experiment_line(legend_name, filename, mark)

plt.xscale('log')
plt.yscale('log')
plt.axis([100,50000,0.001, 300])
plt.xlabel("Number of Offers")
plt.ylabel("Time (s)")

plt.legend()


plt.savefig(output_filename)