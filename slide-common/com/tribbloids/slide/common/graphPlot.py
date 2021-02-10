import inspect

import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
import networkx as nx


def setCanvas():
    plt.rcParams['figure.figsize'] = [14, 9]
    plt.rcParams['figure.dpi'] = 80
    plt.rcParams['savefig.dpi'] = 80





def filterDict(dictToFilter: dict, function):
    sig = inspect.signature(function)
    argKeys: list = [
        param.name
        for param in sig.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD
    ]

    dictKeys = dictToFilter.keys()

    mutualKeys = set(dictKeys).intersection(set(argKeys))

    filtered_dict = {argKey: dictToFilter[argKey] for argKey in mutualKeys}
    return filtered_dict


def drawEdgesAndLabels(options,
                       g,
                       edgeFactory=lambda g: nx.get_edge_attributes(g, 'text')):
    _edgeOptions = filterDict({**options}, nx.drawing.draw_networkx_edges)

    _labelOptions = filterDict(
        {
            **_edgeOptions, 'font': 'dejavu sans',
            'edge_labels': edgeFactory(g),
            'bbox': dict(alpha=0.05, color='w')
        }, nx.drawing.draw_networkx_edge_labels)
    nx.drawing.draw_networkx_edges(g, arrows=True, **_edgeOptions)
    nx.drawing.draw_networkx_edge_labels(g, **_labelOptions)


def drawGraph(g, layoutG=None, **kwargs):
    if not layoutG:
        layoutG = g

    edges = g.edges.data()
    tails = [e[0:2] for e in edges if ('wedge' in e[2])]
    tailGraph = g.edge_subgraph(tails)

    heads = [e[0:2] for e in edges if ('wedge' not in e[2])]
    headGraph = g.edge_subgraph(heads)

    defaultOpt = {
        'node_size': 2000,
        'pos': nx.drawing.nx_agraph.graphviz_layout(layoutG, prog='dot')
        # 'pos': nx.drawing.spring_layout(layoutG)
    }
    sharedOpt = {**defaultOpt, **kwargs}

    nodeOpt = {
        **sharedOpt,
        'node_color': 'white',
        'node_shape': "o",
        # 'font_family': 'dejavu sans',
        # 'node_shape': "s",
    }

    arrowOpt = {
        **sharedOpt,
        'width': 2,
        'edge_color': '#AAAAAA',
        'arrowsize': 30
    }

    arrowHeadOpt = {**arrowOpt, 'arrowstyle': '->'}

    arrowTailOpt = {**arrowOpt, 'arrowstyle': 'wedge'}

    with plt.xkcd():
        fig, ax = plt.subplots(1)
        fig.patch.set_alpha(0)

        ax.axis('off')

        ax = SubplotZero(fig, 111)
        fig.add_subplot(ax)
        plt.xticks([])
        plt.yticks([])

        ax.set_ylabel('go up')
        ax.set_xlabel('go right')

        for s in ['right', 'top']:
            ax.axis[s].set_visible(False)

        for s in ['bottom', 'left']:
            axis = ax.axis[s]
            axis.set_axisline_style("->")
            # axis.set_lim([1.1*y for y in axis.get_lim()])# TODO: how to do this?

        ax.patch.set_alpha(0)

        _nodeOpt = filterDict({**nodeOpt}, nx.drawing.draw_networkx_nodes)
        nx.drawing.draw_networkx_nodes(g, **_nodeOpt)

        _labelOpt = filterDict({**nodeOpt}, nx.drawing.draw_networkx_labels)
        nx.drawing.draw_networkx_labels(g, **_labelOpt)

        drawEdgesAndLabels(arrowHeadOpt, headGraph)
        drawEdgesAndLabels(arrowTailOpt, tailGraph)
