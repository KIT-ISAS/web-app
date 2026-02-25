import dash

from components.split_pane import SplitPane
from model.distributions.gaus1d.gaus1d import Gaus1D
from renderer.selfcontained_distribution_renderer import SelfContainedDistributionRenderer as Renderer

dash.register_page(__name__)

renderer = Renderer(Gaus1D())
options, graph = renderer.get_layout_components()

layout = SplitPane(
	[
		*options
	],
	[
		*graph
	],
	30
)