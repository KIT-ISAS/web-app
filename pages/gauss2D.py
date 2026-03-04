import dash

from components.split_pane import SplitPane
from model.distributions.gaus2d.gaus2d import Gaus2D
from renderer.selfcontained_distribution_renderer import SelfContainedDistributionRenderer as Renderer

dash.register_page(__name__)

renderer = Renderer(Gaus2D())
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