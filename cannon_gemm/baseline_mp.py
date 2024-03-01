import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def heatmap(data, row_labels, col_labels, vmax, ax=None,
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

    ax.tick_params(axis="both", labelsize=14)
    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.set_ylabel("p", fontsize=15)
    ax.set_xlabel("m", fontsize=15)

    return im

def plot_graph(plot_n, p_sizes, energy, m, max_energy):
    '''
    m: int
    '''
    fig, ax = plt.subplots()
    ax.set_title(f'E = f(m,p) for n = {m}', fontsize=15)
    im = heatmap(energy, p_sizes, plot_n, max_energy, ax=ax,
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
            text1 = ax.text(j, i, text.rstrip('0').rstrip('.') if '.' in text else text,
                           ha="center", va="center", color="black",size=14)

    fig.tight_layout()
    plt.show()

def calc_energy(i, n, p, m, factors, J_s=0, J_w=1, a=4, addition_factor =0):
    block_memory = ((n * n) / p[i]) * a * 3
    # print(block_memory)
    # print("M: ", m[i])
    if(i < 0):
        return 0 # return 0 if the system can't calc the matrix
    if(i == 0):
        #print("In if I: ", i)
        return 2 * (J_s + J_w * factors[i] * a * ((n * n) / math.sqrt(p[i]))) + addition_factor
    else:
        #print("In else I: ", i)
        return 2 * (J_s + J_w * factors[i] * a * ((n * n) / math.sqrt(p[i]))) + calc_energy(i - 1, (n/p[i]), p, m, factors, addition_factor=addition_factor)   
    
def calc_baseline_energy_wrapper(matrix_sizes, p, factors, mem, num_levels, J_s=0, J_w=1, a=4, addition_factor=0):
    '''
    matrix_sizes: list
    plot_n: list
    p: list
    mem: list or list of list
    factors: list
    '''
    energy = []
    c = 0
    for size in matrix_sizes:
        n = 2 ** size
        addition_factor = 50 * n * n * n
        e = calc_energy(num_levels[c], n, p, mem, factors, addition_factor=addition_factor)
        energy.append(e)
        c = c + 1
    return energy
    
def calc_energy_wrapper(matrix_size, p, factors, mem, num_levels, J_s=0, J_w=1, a=4, addition_factor=0):
    '''
    matrix_sizes: list
    plot_n: list
    p: list
    mem: list or list of list
    factors: list
    '''
    energy = []
    c = 0
    for m in mem:
        e = calc_energy(num_levels[c], matrix_size, p, m, factors)
        energy.append(e)
        c = c + 1
    return energy
    
# def calc_energy_wrapper(matrix_sizes, plot_n, p, factors, mem, J_s=0, J_w=1, a=4, addition_factor=0):
#     '''
#     matrix_sizes: list
#     plot_n: list
#     p: list
#     mem: list
#     factors: list
#     '''
#     for m in mem:
#         energy = []
#         c = 0
#         for size in matrix_sizes:
#             n = 2 ** size
#             addition_factor = 2 * n * 3 * 2500
#             e = calc_energy(num_levels[c], n, p, m, factors, addition_factor=addition_factor)
#             energy.append(e)
#             c = c + 1
        # plot_graph(plot_n, energy, m[0])

def baseline_params_energy_calc():
    matrix_sizes = [20]
    #matrix_sizes = [8, 10, 12, 14, 16, 18, 20, 22]
    p = [4096, 4096]
    factors = [25000, 250000]
    #mem = [128000000, 32768000000]
    mem = [16777216, 68719476736]
    J_s = 0
    J_w = 1
    a = 4
    num_levels = [0 for _ in range(len(matrix_sizes))]
    i = 0
    for size in matrix_sizes:
        n = 2 ** size
        #print("N:", n)
        flag = False
        l = 0
        try:
            while(not flag):
                #print("L:", l)
                if(3 * a * n * n > mem[l] * p[l]):
                    l = l + 1
                    flag = False
                else:
                    num_levels[i] = l
                    flag = True
            #print("=============")
            i = i + 1
        except IndexError:
            num_levels[i] = -1
    # print("num_levels: ", num_levels)
    baseline_energy = calc_baseline_energy_wrapper(matrix_sizes, p, factors, mem, num_levels)
    assert len(baseline_energy) == len(matrix_sizes)
    return baseline_energy

def new_sys_params_energy_calc():
    #matrix_sizes = [8, 10, 12, 14, 16, 18, 20]
    matrix_sizes = [20]
    p_sizes = [[4096 for i in range(4)],
               [256 for i in range(4)],
               [128 for i in range(4)],
               [64 for i in range(4)],
               [32 for i in range(4)],
               [16 for i in range(4)],
               [8 for i in range(4)]]
    m_vals = [2000, 16000, 64000]
    factors = [1, 100, 10000, 100000]   
    m1 = [2048]
    m2 = [16384]
    m3 = [65536]

    for i in range(1, 4):
        m1.append(m1[i - 1] * 4096)
        m2.append(m2[i - 1] * 4096)
        m3.append(m3[i - 1] * 4096)
    mem = [m1, m2, m3]
    print(mem)
    J_s = 0
    J_w = 1
    a = 4
    num_levels = [0 for _ in range(len(m_vals))]
    # i = 0
    new_sys_energy = []
    for size in matrix_sizes:
        n = 2 ** size
        print("N:",n)
        #i = 0
        nm_energy = []
        for p in p_sizes:
            i = 0
            for m in mem:
                print("M:", m)
                flag = False
                l = 0
                try:
                    while(not flag):
                        print("L:", l)
                        if(3 * a * n * n > m[l] * p[l]):
                            l = l + 1
                            flag = False
                        else:
                            num_levels[i] = l
                            flag = True
                    print("=============")
                    i = i + 1
                except IndexError:
                    num_levels[i] = -1
                    i = i + 1
                    #continue
            print("num_levels: ", num_levels)
            energy = calc_energy_wrapper(n, p, factors, mem, num_levels)
            assert len(energy) == len(m_vals)
            nm_energy.append(energy)
        new_sys_energy.append(nm_energy)
    return new_sys_energy

baseline_energy = baseline_params_energy_calc() #list
new_sys_energy = new_sys_params_energy_calc() # list of list
energy_saving_factor = []
print(new_sys_energy)
# max_energy = 0
max_energy = []
for i in range(len(new_sys_energy)):
    temp = []
    m_energy = 0
    for j in range(len(new_sys_energy[i])):
        temp2 = []
        for k in range(len(new_sys_energy[i][j])):
            try:
                val = baseline_energy[0]/new_sys_energy[i][j][k]
                temp2.append(val)
                m_energy = max(m_energy, val)
            except ZeroDivisionError:
                temp2.append(0)
        temp.append(temp2)
    max_energy.append(m_energy)
    temp = np.asarray(temp, dtype=np.float32)
        #print(temp)
    energy_saving_factor.append(temp)

m_val = [2000, 16000, 64000]
plot_n = 2 ** 20
p_sizes = [4096, 256, 128, 64, 32, 16, 8]
print(max_energy)
for y_axis in range(len(energy_saving_factor)):
    print(energy_saving_factor[y_axis])
    plot_graph(m_val, p_sizes, energy_saving_factor[y_axis], plot_n, max_energy[y_axis])
