import dash


from components.split_pane import SplitPane
from model.distributions.conditional.conditional import Conditional
from renderer.selfcontained_distribution_renderer import SelfContainedDistributionRenderer as Renderer

dash.register_page(__name__)


renderer = Renderer(Conditional())
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