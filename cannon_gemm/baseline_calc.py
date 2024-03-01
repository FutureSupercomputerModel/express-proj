import math
import matplotlib.pyplot as plt


def plot_graph(plot_n, energy, m):
    '''
    m: int
    '''
    plt.plot(plot_n, energy, marker='o', color='b')
    plt.xticks(plot_n)
    plt.yticks(energy)
    #print(energy)

    plt.xscale("log", base=2)
    plt.yscale("log")
    plt.xlabel('n', fontsize=20)
    plt.ylabel('Energy saving factor',fontsize=20)
    plt.title(f'E = f(n) for m4 = {m/1000} KB', fontsize=21)
    plt.tick_params(axis="both", labelsize=20)

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
    for i in range(len(matrix_sizes)):
        n = 2 ** matrix_sizes[i]
        # addition_factor = 50 * n * n * n
        add_factor = addition_factor[i] if addition_factor != 0 else 0
        e = calc_energy(num_levels[c], n, p, mem, factors, addition_factor=add_factor)
        energy.append(e)
        c = c + 1
    return energy
    # for size in matrix_sizes:
    #     n = 2 ** size
    #     addition_factor = 50 * n * n * n
    #     e = calc_energy(num_levels[c], n, p, mem, factors, addition_factor=addition_factor)
    #     energy.append(e)
    #     c = c + 1
    # return energy
    
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
    matrix_sizes = [8, 10, 12, 14, 16, 18, 20, 22]
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
    addition_factor = []
    for size in matrix_sizes:
        n = 2 ** size
        addition_factor.append(50 * n * n * n)
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
            
    baseline_energy = calc_baseline_energy_wrapper(matrix_sizes, p, factors, mem, num_levels, addition_factor=addition_factor)
    assert len(baseline_energy) == len(matrix_sizes)
    return baseline_energy

def new_sys_params_energy_calc():
    #matrix_sizes = [8, 10, 12, 14, 16, 18, 20]
    matrix_sizes = [8, 10, 12, 14, 16, 18, 20, 22]
    p = [4096, 4096, 4096]
    # p = [64, 64, 64, 64]
    factors = [1, 100, 10000, 100000]   
    m1 = [2048]
    m2 = [16384]
    m3 = [65536]

    for i in range(1, 4):
        m1.append(m1[i - 1] * p[i - 1])
        m2.append(m2[i - 1] * p[i - 1])
        m3.append(m3[i - 1] * p[i - 1])
    mem = [m1, m2, m3]
    print(mem)
    J_s = 0
    J_w = 1
    a = 4
    num_levels = [0 for _ in range(len(matrix_sizes))]
    # i = 0
    new_sys_energy = []
    for m in mem:
        print("M:",m)
        i = 0
        for size in matrix_sizes:
            n = 2 ** size
            print("N:", n)
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
        energy = calc_baseline_energy_wrapper(matrix_sizes, p, factors, m, num_levels)
        assert len(energy) == len(matrix_sizes)
        new_sys_energy.append(energy)
    return new_sys_energy

baseline_energy = baseline_params_energy_calc() #list
new_sys_energy = new_sys_params_energy_calc() # list of list
energy_saving_factor = []
print(new_sys_energy)

for i in range(len(new_sys_energy)):
    temp = []
    for j in range(len(new_sys_energy[i])):
        try:
            temp.append(baseline_energy[j]/new_sys_energy[i][j])
        except ZeroDivisionError:
            temp.append(0)
    print(temp)
    energy_saving_factor.append(temp)

m_val = [2000, 16000, 64000]
matrix_sizes = [8, 10, 12, 14, 16, 18, 20, 22]
plot_n = []
for n in matrix_sizes:
    plot_n.append(2 ** n)
for y_axis in range(len(energy_saving_factor)):
    plot_graph(plot_n, energy_saving_factor[y_axis], m_val[y_axis])




