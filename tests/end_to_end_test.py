import dash
from app import app
import pytest

PAGES_WITH_PLOTLY_PLOTS = ['/conditional', '/gauss1d', '/gauss2d', '/sphere', '/torus']
PAGES_WITH_AT_LEAST_ONE_SLIDER = ['/conditional', '/gauss1d', '/gauss2d', '/sphere', '/torus']

# basic launch web-app test
def test_001_home_end_to_end(dash_duo):
	dash_duo.start_server(app)

	assert dash_duo.get_logs() == [], "browser console should contain no error"

	dash_duo.wait_for_text_to_equal("h1", "ISAS Interactive", timeout=10)

@pytest.mark.parametrize("path", PAGES_WITH_PLOTLY_PLOTS)
def test_002_page_loads_plots(dash_duo, path):
	dash_duo.start_server(app)

	# navbutton should appear
	link = dash_duo.wait_for_element(f'a.nav-link[href="{path}"]', timeout=10)
	link.click()

	# a plot should appear
	dash_duo.wait_for_element("div.js-plotly-plot", timeout=10)

	assert dash_duo.get_logs() == [], "browser console should contain no error"


@pytest.mark.parametrize("path", PAGES_WITH_PLOTLY_PLOTS)
def test_003_has_one_slider(dash_duo, path):
	dash_duo.start_server(app)

	# navbutton should appear
	link = dash_duo.wait_for_element(f'a.nav-link[href="{path}"]', timeout=10)
	link.click()

	# a slider should appear
	dash_duo.wait_for_element("div.rc-slider", timeout=10)

	assert dash_duo.get_logs() == [], "browser console should contain no error"