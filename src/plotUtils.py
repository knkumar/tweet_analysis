import matplotlib as mplot
mplot.use('PDF')
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class plotFigParams:
    def __init__(self, xlabel, ylabel, title, xscale=None, yscale=None, legend=None, xticks=None, 
                 axhline=None, cumulative=0, rotation=None, color='b', marker='o'):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.xscale = xscale
        self.yscale = yscale
        self.legend = legend
        self.xticks = xticks
        self.axhline = axhline
        self.cumulative = cumulative
        self.rotation = rotation
        self.color = color
        self.marker = marker

class plotFigFunc:
    
    def __init__(self):
        self.fig = plt.figure()

    def plot_scatter(self, params, xvalues,yvalues, ax=None):
        if not ax:
            subplot = self.fig.add_subplot(111)
        else:
            subplot = ax
            params.color = 'r'
            params.marker = 'x'
        subplot.scatter(xvalues, yvalues, c=params.color,marker=params.marker)
        if params.axhline:
            subplot.axhline(y=params.axhline, color='r')
        if params.xscale:
            subplot.set_xscale(params.xscale)
        if params.yscale:
            subplot.set_yscale(params.yscale)
        if params.legend:
            subplot.legend(params.legend) #("flickr","twitter")
        if params.xticks:
            ax.set_xticklabels(xticks, rotation='vertical')
        subplot.set_xlabel(params.xlabel)
        subplot.set_ylabel(params.ylabel)
        subplot.set_title(params.title)
        return subplot

    def plot_hist(self, params, xvalues, yvalues,ax=None):
        if not ax:
            subplot = self.fig.add_subplot(111)
        else:
            subpolot = ax
        subplot.hist(xvalues,yvalues,color=params.color, cumulative=params.cumulative)
        if params.xscale:
            subplot.set_xscale(params.xscale)
        if params.yscale:
            subplot.set_yscale(params.yscale)
        subplot.set_xlabel(params.xlabel)
        subplot.set_ylabel(params.ylabel)
        subplot.set_title(params.title)
        return subplot

    def save_fig(self, name):
        self.fig.savefig("%s.pdf"%name)
