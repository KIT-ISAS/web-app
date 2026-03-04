'''
Run this file directly from project root with:

sudo "$(poetry run which python)" -m pyperf system tune
PYTHONPATH=$PWD poetry run python model/distributions/sphere/watson/benchmark_fib_starts.py


you can also plot from existing JSON files by setting the environment variable:
PLOT_FROM_JSON=1 PYTHONPATH=$PWD poetry run python model/distributions/sphere/watson/benchmark_fib_starts.py
'''

import json
import os
from pathlib import Path
import plotly.express as px
from model.distributions.sphere.watson.fibonachi import WatsonFibonachiSampling
from util.selectors.slider_float import FloatSlider
import pyperf
import statistics
import numpy as np

sampler = WatsonFibonachiSampling()
methods = {
	"Closed-Form" : sampler.sample_closed,
	"Inverse Interpolation" : sampler.sample_inverse_interpolation,
	"Inverse ODE" : sampler.sample_inverse_ode,
	"ODE Event Locations" : sampler.sample_events,
}


def benchmark_kappa(method, kappa, sample_count, times=50):
	distribution_options = [FloatSlider("", 0, kappa, 100)]
	sampling_options = [FloatSlider("", 0, sample_count, sample_count)]
	for time in range(times):
		method(sampling_options, distribution_options)

def bench_single_kappa(kappa, sample_count, id):
	results = {}
	for method_name, method in methods.items():
		bench_name = f"Watson Fibonacci Sampling: {method_name} (kappa={kappa}) [{id}]"
		benchmark = runner.bench_func(bench_name, benchmark_kappa, method, kappa, sample_count, 1)
		results[method_name] = benchmark

	return results

def bench_multiple_kappa():
	sample_count = 10000
	all_results = {}
	for kappa in range(-30, 31, 2):
		res = bench_single_kappa(kappa, sample_count, "Multiple Kappa")
		for name, bench in res.items():
			if name not in all_results:
				all_results[name] = []
			all_results[name].append((kappa, bench))
	return all_results

def bench_multiple_sample_counts(kappa):
	all_results = {}
	for sample_count in range(100, 1001, 10):
		res = bench_single_kappa(kappa, sample_count, f"Multiple Sample Counts (kappa={kappa}, sample_count={sample_count})")
		for name, bench in res.items():
			if name not in all_results:
				all_results[name] = []
			all_results[name].append((sample_count, bench))
	return all_results

def bench_multiple_sample_counts_log(kappa):
	all_results = {}
	sample_counts = np.unique(np.logspace(2, 5, num=90, dtype=int))
	for sample_count in sample_counts:
		res = bench_single_kappa(kappa, sample_count, f"Multiple Sample Counts Log (kappa={kappa}, sample_count={sample_count})")
		for name, bench in res.items():
			if name not in all_results:
				all_results[name] = []
			all_results[name].append((sample_count, bench))
	return all_results


def _sanitize_filename(name):
	return name.replace(" ", "_").replace(":", "")

def _rows_from_results(results, x_label):
	def _to_builtin(value):
		if isinstance(value, np.integer):
			return int(value)
		if isinstance(value, np.floating):
			return float(value)
		return value

	if x_label == "sample_count":
		return [
			dict(name=n, sample_count=_to_builtin(k), time=_to_builtin(t.mean()))
			for n, pts in results.items()
			for k, t in pts
		]
	if x_label == "kappa":
		return [
			dict(name=n, kappa=_to_builtin(k), time=_to_builtin(t.mean()))
			for n, pts in results.items()
			for k, t in pts
		]
	raise ValueError(f"Unsupported x_label: {x_label}")

def _plot_rows(rows, title, filename, x_label, log_x=False, log_y=False):
	fig = px.line(
		rows,
		x=x_label,
		y="time",
		color="name",
		markers=True,
		log_x=log_x,
		log_y=log_y,
		labels={"time": "time in s", "sample_count": "sample count"}, 
	)
	fig.update_layout(
		legend=dict(
			orientation="h",
			yanchor="bottom",
			y=1.02,
			xanchor="left",
			x=0,
		),
		font=dict(size=26),
	)
	if log_x:
		fig.update_xaxes(dtick=1)
	if log_y:
		fig.update_yaxes(dtick=1)
	fig.update_layout(legend_title_text="")

	try:
		fig.write_image(f"{_sanitize_filename(filename)}.svg")
	except Exception as e:
		print("Generating plot failed, dumping data:", e)
		print(rows)
		print("Trying to save html as fallback")
		fig.write_html(f"{_sanitize_filename(title)}.html", include_plotlyjs="cdn", full_html=True)

def plot_benches(results, title=None, filename=None, x_label=None, log_x=None, log_y=None, json_filename=None):

	if isinstance(results, (str, Path)):
		json_path = Path(results)
		with json_path.open("r", encoding="utf-8") as handle:
			payload = json.load(handle)
		rows = payload["rows"]
		if title is None:
			title = payload.get("title", json_path.stem)
		if filename is None:
			filename = payload.get("filename", json_path.stem)
		if x_label is None:
			x_label = payload.get("x_label")
		if log_x is None:
			log_x = payload.get("log_x", False)
		if log_y is None:
			log_y = payload.get("log_y", False)
		if x_label is None:
			raise ValueError("x_label is required when replotting from JSON")
		_plot_rows(rows, title, filename, x_label, log_x=log_x, log_y=log_y)
		return

	if title is None or filename is None or x_label is None:
		raise ValueError("title, filename, and x_label are required for raw benchmark data")
	if log_x is None:
		log_x = False
	if log_y is None:
		log_y = False

	rows = _rows_from_results(results, x_label)
	payload = {
		"title": title,
		"filename": filename,
		"x_label": x_label,
		"log_x": log_x,
		"log_y": log_y,
		"rows": rows,
	}
	if json_filename is None:
		json_filename = f"{_sanitize_filename(filename)}.json"
	with open(json_filename, "w", encoding="utf-8") as handle:
		json.dump(payload, handle, indent=2, sort_keys=True)
	_plot_rows(rows, title, filename, x_label, log_x=log_x, log_y=log_y)



if __name__ == "__main__":
	plot_from_json = os.getenv("PLOT_FROM_JSON")
	if plot_from_json:
		if plot_from_json != "1":
			json_paths = [p.strip() for p in plot_from_json.split(",") if p.strip()]
		else:
			json_paths = [
				f"{_sanitize_filename('time taken for various kappa values (10000 samples)')}.json",
				f"{_sanitize_filename('time taken for various kappa values log scale (10000 samples)')}.json",
				f"{_sanitize_filename('time taken for various sample counts log scale (kappa=10)')}.json",
				f"{_sanitize_filename('time taken for various sample counts log scale (kappa=-10)')}.json",
			]
		for json_path in json_paths:
			plot_benches(json_path)
		raise SystemExit(0)

	runner = pyperf.Runner()
	

	mult_kappa = bench_multiple_kappa()
	#mult_samples_neg_10 = bench_multiple_sample_counts(-10)
	#mult_samples_10 = bench_multiple_sample_counts(10)
	log_mult_samples_10 = bench_multiple_sample_counts_log(10)
	log_mult_samples_neg_10 = bench_multiple_sample_counts_log(-10)
	

	if not runner.args.worker:
		plot_benches(mult_kappa, "time taken for various kappa values (10000 samples)", "time taken for various kappa values (10000 samples)", "kappa")
		plot_benches(mult_kappa, "time taken for various kappa values log scale (10000 samples)", "time taken for various kappa values log scale (10000 samples)", "kappa", log_y=True)
		
		#plot_benches(mult_samples_10, "time taken for various sample counts (kappa=10)", "time taken for various sample counts (kappa=10)", "sample_count")
		plot_benches(log_mult_samples_10, "time taken for various sample counts (kappa=10)", "time taken for various sample counts log scale (kappa=10)", "sample_count", log_x=True, log_y=True)

		#plot_benches(mult_samples_neg_10, "time taken for various sample counts (kappa=-10)", "time taken for various sample counts (kappa=-10)", "sample_count")
		plot_benches(log_mult_samples_neg_10, "time taken for various sample counts (kappa=-10)", "time taken for various sample counts log scale (kappa=-10)", "sample_count", log_x=True, log_y=True)
