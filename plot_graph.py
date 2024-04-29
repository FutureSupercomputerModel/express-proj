import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_line_graph(plot_n, energy, xlabel, ylabel, title, fontsize_axis, fontsize_title):
    '''
    m: int
    '''
    plt.plot(plot_n, energy, marker='o', color='b')
    plt.xticks(plot_n)
    plt.yticks(energy)
    #print(energy)

    plt.xscale("log", base=2)
    plt.yscale("log")
    plt.xlabel(xlabel, fontsize=fontsize_axis)
    plt.ylabel(ylabel,fontsize=fontsize_axis)
    plt.title(title, fontsize=fontsize_title) # f'm4 = {m/1000} KB'
    plt.tick_params(axis="both", labelsize=20)

    plt.show()

def heatmap(data, row_labels, col_labels, vmax, xlabel="n", ylabel="p", ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, vmin = 0, vmax = data[-1,-1], **kwargs)

    # Create colorbar
    # cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    # cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    im.set_clim(0, vmax)
    # cbar.set_ticks(ticks=[0, 10000000, 1000000000000000])

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)
    ax.tick_params(axis="both", labelsize=12)
    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.set_xlabel(xlabel, fontsize=15)

    return im

def plot_heatmap_graph(plot_n, p_sizes, energy, level, max_energy, title, xlabel="n", ylabel="p"):
    '''
    m: int
    '''
    fig, ax = plt.subplots()
    ax.set_title(title, fontsize=15)
    # ax.set_title(f'm4 = {m/1000} KB', fontsize=15)
    im = heatmap(energy, p_sizes, plot_n, max_energy, xlabel, ylabel, ax=ax,
                       cmap="Wistia", cbarlabel="Energy [pJ]")
    # texts = annotate_heatmap(im, valfmt="{x:.2e}")
    valfmt = matplotlib.ticker.StrMethodFormatter("{x}")

    for i in range(len(p_sizes)):
        for j in range(len(plot_n)):
            if(energy[i,j] > 1000):
                valfmt = matplotlib.ticker.StrMethodFormatter("{x:.2e}")
            elif(energy[i,j]% 1 != 0):
                valfmt = matplotlib.ticker.StrMethodFormatter("{x:.4f}")
            else:
                valfmt = matplotlib.ticker.StrMethodFormatter("{x}")
            text = valfmt(energy[i, j], None)
            text = text.rstrip('0').rstrip('.') if '.' in text else text
            text += '\n'
            text += str(int(level[i][j]))
            text1 = ax.text(j, i, text,
                           ha="center", va="center", color="black",size=14)

    fig.tight_layout()
    plt.show()
