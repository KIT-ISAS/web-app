'''
Run this file directly from project root with:

sudo "$(poetry run which python)" -m pyperf system tune
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

def bench_single_kappa(kappa, sample_count, id):
	results = {}
	for method_name, method in methods.items():
		bench_name = f"Watson Fibonacci Sampling: {method_name} (kappa={kappa}) [{id}]"
		benchmark = runner.bench_func(bench_name, benchmark_kappa, method, kappa, sample_count, 5)
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


def plot_benches(results, title, x_label):
	import plotly.express as px
	try:
		if x_label == "sample_count":
			rows = [dict(name=n, sample_count=k, time=t.mean()) for n, pts in results.items() for k, t in pts]
		else:
			rows = [dict(name=n, kappa=k, time=t.mean()) for n, pts in results.items() for k, t in pts]
		fig = px.line(rows, x=x_label, y="time", color="name", markers=True, title=title)
		fig.write_image(f"{title.replace(' ', '_').replace(':', '')}.svg")
	except Exception as e:
		print("Generating plot failed, dumping data:", e)
		print(results.items())
		print("Trying to save html as fallback")
		fig.write_html(f"{title.replace(' ', '_').replace(':', '')}.html", include_plotlyjs="cdn", full_html=True)



if __name__ == "__main__":
	runner = pyperf.Runner()
	mult_kappa = bench_multiple_kappa()
	mult_samples_neg_10 = bench_multiple_sample_counts(-10)
	mult_samples_10 = bench_multiple_sample_counts(10)

	if not runner.args.worker:
		plot_benches(mult_kappa, "Watson Fibonacci Sampling Benchmark: time taken for various kappa values (10000 samples)", "kappa")
		plot_benches(mult_samples_neg_10, "Watson Fibonacci Sampling Benchmark: time taken for various sample counts (kappa=-10)", "sample_count")
		plot_benches(mult_samples_10, "Watson Fibonacci Sampling Benchmark: time taken for various sample counts (kappa=10)", "sample_count")
		
	