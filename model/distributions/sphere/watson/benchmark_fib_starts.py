'''
Run this file directly from project root with:
PYTHONPATH=$PWD poetry run python model/distributions/sphere/watson/benchmark_fib_starts.py
'''

from model.distributions.sphere.watson.fibonachi import WatsonFibonachiSampling
from util.selectors.slider_float import FloatSlider
import pyperf
import statistics


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

def bench_single_kappa(kappa, sample_count):
	results = {}
	for method_name, method in methods.items():
		bench_name = f"Watson Fibonacci Sampling: {method_name} (kappa={kappa})"
		benchmark = runner.bench_func(bench_name, benchmark_kappa, method, kappa, sample_count, 1) # TODO: make this higher
		results[method_name] = benchmark

	return results

def bench_multiple_kappa():
	sample_count = 1000
	all_results = {}
	for kappa in range(-30, 31, 10): # TODO: set step lower 
		res = bench_single_kappa(kappa, sample_count)
		for name, bench in res.items():
			if name not in all_results:
				all_results[name] = []
			all_results[name].append((kappa, bench))
	return all_results

def bench_multiple_sample_counts(kappa):
	all_results = {}
	for sample_count in range(100, 1001, 100): # TODO: set step lower 
		res = bench_single_kappa(kappa, sample_count)
		for name, bench in res.items():
			if name not in all_results:
				all_results[name] = []
			all_results[name].append((sample_count, bench))
	return all_results


def plot_benches(results):
	import plotly.express as px
	
	rows = [dict(name=n, kappa=k, time=t.mean()) for n, pts in results.items() for k, t in pts]
	px.line(rows, x="kappa", y="time", color="name", markers=True).show()
		

			


if __name__ == "__main__":
	runner = pyperf.Runner()
	mult_kappa = bench_multiple_kappa()
	if not runner.args.worker:
		plot_benches(mult_kappa)
		
	