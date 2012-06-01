import matplotlib as mplot
mplot.use('PDF')
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class plotFigParams:
    def __init__(self, xlabel, ylabel, title, xscale=None, yscale=None, legend=None, xticks=None, 
                 rotation=None,axhline=None, cumulative=None, rotation=None, color='b', marker='o'):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.xscale = xscale
        self.yscale = yscale
        self.legend = legend
        self.xticks = xticks
        self.rotation = rotation
        self.axhline = axhline
        self.cumulative = cumulative
        self.rotation = rotation
        self.color = color
        self.marker = marker

class plotFigFunc:

    self.fig = plt.figure()

    def plot_scatter(self, params, xvalues,yvalues, ax=None):
        if not ax:
            subplot = self.fig.add_subplot(111)
        else:
            subplot = ax
            params.color = 'r'
            params.marker = 'x'
        subplot.scatter(xvalues, yvalues, c=params.color,marker=params.marker)
        subplot.set_xscale(params.xscale)
        subplot.set_yscale(params.yscale)
        subplot.legend(params.legend) #("flickr","twitter")                                                            
        subplot.set_xlabel(params.xlabel)
        subplot.set_ylabel(params.ylabel)
        subplot.set_title(params.title)
        return subplot

    def plot_hist(self, params, xvalues, yvalues,ax=None):
        if not ax:
            subplot = fig.add_subplot(111)
        else:
            subpolot = ax
        subplot.hist(xvalues,yvalue,color=params.color, cumulative=params.cumulative)
        subplot.set_yscale(params.yscale)
        subplot.set_xlabel(params.xlabel)
        subplot.set_ylabel(params.ylabel)
        subplot.set_title(params.title)
        return subplot

    def save_fig(self, name):
        fig.savefig("%s.pdf",name)
