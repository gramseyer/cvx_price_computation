import numpy as np
import cvxpy as cp
import os

import random

endow_min=1000
endow_max=1000000

size_dist = [100, 80, 50, 30, 10, 5]

min_price = 1
max_price = 1000

bad_frac = 0.1

def gen_endow():
	return random.randint(endow_min, endow_max)

def gen_cycle_size():
	v = random.random()

	base = sum(size_dist)

	i = 2
	acc = 0
	for sz in size_dist:
		acc += sz
		if (v < (acc / base)):
			return i
		i += 1

def gen_asset_cycle(n_assets):
	sz = min(n_assets, gen_cycle_size())
	return random.sample(range(n_assets), k = sz)

def gen_asset_pair(n_assets):
	return random.sample(range(n_assets), k = 2)

def gen_tolerance():
	return random.uniform(0, 0.02)

def gen_good_price(price):
	return price * (1.0 - gen_tolerance())

def gen_bad_price(price):
	return price * (1.0 + gen_tolerance())

def gen_offer_cycle(n_assets, prices):
	assets = gen_asset_cycle(n_assets)

	endow = gen_endow()

	out = []

	for i in range(0, len(assets)):
		sell = assets[i]
		buy = assets[(i + 1) % len(assets)]

		sell_price = prices[sell]

		sell_amount = endow / sell_price

		min_price = gen_good_price (sell_price / prices[buy])

		out.append( (sell, buy, sell_amount, min_price) )
	return out

def gen_bad_offer(n_assets, prices):
	assets = gen_asset_pair(n_assets)

	endow = gen_endow()

	sell = assets[0]
	buy = assets[1]

	min_price = gen_bad_price(prices[sell] / prices[buy])

	return (sell, buy, endow / prices[sell], min_price)

def gen_price():
	return random.uniform(min_price, max_price)

def gen_prices(n_assets):
	out = []
	for i in range(n_assets):
		out.append(gen_price())
	return out

def gen_offers(n_assets, m_offers):

	prices = gen_prices(n_assets)

	out = []

	bad_frac = 0.0

	while (len(out) < m_offers):
		if (bad_frac > 1.0):
			out.append(gen_bad_offer(n_assets, prices))
			bad_frac -= 1
		else:
			good_offers = gen_offer_cycle(n_assets, prices)
			bad_frac += (len(good_offers) * bad_frac)
			out += good_offers

	return out[0:m_offers]

def run_experiment(n, m):
	print("running trial (assets, offers)", n, m)

	sell_asset = np.zeros(m, dtype=np.uint)
	buy_asset = np.zeros(m, dtype=np.uint)
	ratios = np.zeros((m, 1))
	endowments = np.zeros((m, 1))

	offers = gen_offers(n, m)

	for i in range(0, m):
		(sell, buy, endow, price) = offers[i]
		sell_asset[i] = sell
		buy_asset[i] = buy
		ratios[i] = price
		endowments[i] = endow


	sell_expanded = np.zeros((m, n))
	for i in range(0, m):
		sell_expanded[i,sell_asset[i]] = 1

	buy_expanded = np.zeros((m, n))
	for i in range(0, m):
		buy_expanded[i, buy_asset[i]] = 1

	sell_endow_expanded = np.zeros((m,n))
	for i in range(0,m):
		sell_endow_expanded[i, sell_asset[i]] = endowments[i]


	ones = np.ones((m, 1))

	y = cp.Variable((m, 1), name="y")

	beta = cp.Variable((m, 1), name = "beta")
	p = cp.Variable((n, 1), name = "price")

	constraints = [
		y >= 0,
		beta >= 0,
		y <= sell_endow_expanded @ p,
		cp.multiply(ratios, beta) <= buy_expanded @ p,
		beta <= sell_expanded @ p, 
		y.T @ buy_expanded == y.T @ sell_expanded,
		p >= 1,
	]

	def get_x_lg_x_over_y(x, y):
		return cp.kl_div(x,y) + x - y

	objective = cp.Minimize(cp.sum(cp.multiply(endowments, get_x_lg_x_over_y(sell_expanded @ p, beta))) - cp.sum(cp.multiply(y, cp.log(ratios))))

	problem = cp.Problem(objective, constraints)
	error = 0.001
	max_iters = 100
	success = False
	while not success:
		try:
			problem.solve(verbose=False, abstol = error, reltol=error, abstol_inacc=error, reltol_inacc=error, max_iters=max_iters)#, feastol = error, feastol_inacc = error)
			success=True
		except:
			max_iters += 20
			if max_iters > 300:
				print ("hit max iter count")
				return -1
	duration = problem.solver_stats.solve_time

	return duration

	

def run_unified_exp(n_assets):
	num_offer_list = [100, 500, 1000, 2000, 5000, 10000, 50000]
	trials = 5
	results = {}

	for n in num_offer_list:
		acc = 0
		succ = 0
		results[n] = {}
		for i in range(0, trials):
			res = run_experiment(n_assets, n)
			if (res > 0):
				succ += 1
				acc += res

		if (succ != trials):
			print("warning: found timeouts in offer count ", n)
		results[n]["avg"] = (acc / succ)
		results[n]["succ"] = succ

	return results


overall_res = {}
overall_res[10] = run_unified_exp(10)
overall_res[20] = run_unified_exp(20)
overall_res[50] = run_unified_exp(50)

import csv

with open("cvxpy_results.csv", 'w') as f:
	writer = csv.writer(f)
	for n in overall_res.keys():
		results = overall_res[n]
		for k in results.keys():
			v = results[k]
			writer.writerow([n, k, v["succ"], v["avg"]])


