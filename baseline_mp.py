import math
import plot_graph
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def calc_energy(i, n, p, m, factors, J_s=0, J_w=1, a=8, addition_factor =0):
    block_memory = ((n * n) / p[i]) * a * 3
    # print(block_memory)
    # print("M: ", m[i])
    if(i < 0):
        return 0 # return 0 if the system can't calc the matrix
    if(i == 0):
        print("In if I: ", i)
        print(f'n :{n}, p: {p[i]}, levels: {i}, factors: {factors[i]}, J_s: {J_s}, J_w: {J_w}, a: {a}, addition_factor: {addition_factor}')
        return 2 * (J_s + J_w * factors[i] * a * (n * n) * math.sqrt(p[i])) + addition_factor
    else:
        print("In else I: ", i)
        return 2 * (J_s + J_w * factors[i] * a * (n * n) * math.sqrt(p[i])) + calc_energy(i - 1, (n/math.sqrt(p[i])), p, m, factors, addition_factor=addition_factor) * p[i]  
    
def calc_energy_wrapper(matrix_size, p, factors, mem, num_levels, J_s=0, J_w=1, a=8, addition_factor=0):
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

def baseline_params_energy_calc():
    matrix_sizes = [20]
    baseline_energy = []
    for size in matrix_sizes:
        n = 2 ** size
        baseline_energy.append(40 * n * n *n)
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
    factors = [1, 100, 1000, 10000]   
    m1 = [2048]
    m2 = [16384]
    m3 = [65536]

    # for i in range(1, 4):
    #     m1.append(m1[i - 1] * 4096)
    #     m2.append(m2[i - 1] * 4096)
    #     m3.append(m3[i - 1] * 4096)
    # mem = [m1, m2, m3]
    mem = [2048, 16384, 65536]
    print(mem)
    J_s = 0
    J_w = 1
    a = 8
    
    # i = 0
    all_num_levels = []
    new_sys_energy = []
    for size in matrix_sizes:
        n = 2 ** size
        print("N:",n)
        #i = 0
        nm_energy = []
        nm_level = []
        for p in p_sizes:
            i = 0
            num_levels = [0 for _ in range(len(m_vals))]

            for m_val in mem:
                m = [m_val]
                for j in range(1, 4):
                    m.append(m[j - 1] * p[j - 1])
                print("M_VAL: ", m)  
                
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
            nm_level.append(num_levels)
            energy = calc_energy_wrapper(n, p, factors, mem, num_levels)
            assert len(energy) == len(m_vals)
            nm_energy.append(energy)
        new_sys_energy.append(nm_energy)
        all_num_levels.append(nm_level)
    return new_sys_energy, all_num_levels

baseline_energy = baseline_params_energy_calc() #list
new_sys_energy, num_levels = new_sys_params_energy_calc() # list of list
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
                val = baseline_energy[0]/(0.064 * new_sys_energy[i][j][k])
                temp2.append(val)
                m_energy = max(m_energy, val)
            except ZeroDivisionError:
                temp2.append(0)
        temp.append(temp2)
    max_energy.append(m_energy)
    temp = np.asarray(temp, dtype=np.float32)
        #print(temp)
    energy_saving_factor.append(temp)

m_val = [2048, 16384, 65536]
plot_n = [2 ** 20]
p_sizes = [4096, 256, 128, 64, 32, 16, 8]

for i in range(len(num_levels)):
    for j in range(len(num_levels[i])):
        for k in range(len(num_levels[i][j])):
            if(num_levels[i][j][k] >= 0):
                num_levels[i][j][k] = num_levels[i][j][k] + 1

for y_axis in range(len(energy_saving_factor)):
    title = f'n = {plot_n[y_axis]}'
    plot_graph.plot_heatmap_graph(m_val, p_sizes, energy_saving_factor[y_axis], num_levels[y_axis], max_energy[y_axis], title, 'm', 'p')
