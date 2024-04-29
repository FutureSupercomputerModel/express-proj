import math
import fft_graph
import cannon_gemm
import numpy as np
from operator import add

def baseline_calc_energy_wrapper(func, matrix_sizes, p=None, a=None, f1=None, f2=None):
    baseline_energy = []
    for size in matrix_sizes:
        energy = func.baseline_energy(size, p, a, f1, f2)
        baseline_energy.append(energy)
    return baseline_energy

def get_baseline_energy_calc(func, matrix_sizes, p_sizes, mem, a=None, f1=None, f2=None):
    baseline_energy = []
    for m_val in mem:
        bp_energy = []
        for p in p_sizes:
            energy = baseline_calc_energy_wrapper(func, matrix_sizes, p, a, f1, f2)
            bp_energy.append(energy)
        baseline_energy.append(bp_energy)
    return baseline_energy
    
def calc_energy_wrapper(func, matrix_sizes, p, factors, mem, num_levels, J_s=0, J_w=1, a=8, addition_factor=0):
    '''
    matrix_sizes: list
    plot_n: list
    p: list
    mem: list or list of list
    factors: list
    '''
    energy = []
    #c = 0
    for i in range(len(matrix_sizes)):
        e = func.new_sys_energy(num_levels[i], matrix_sizes[i], p, mem, factors, addition_factor=addition_factor)
        energy.append(e)
        #c = c + 1
    return energy

def get_new_sys_energy_calc(func, matrix_sizes, p_sizes, factors, mem, J_s=0, J_w=1, a=8, debug=False):
    new_sys_energy = []
    #baseline_energy = []
    all_num_levels = []
    for m_val in mem:
        if(debug):
            print("M:",m_val)
        np_level = []
        np_energy = []
        #bp_energy = []
        for p in p_sizes:
            num_levels = [0 for _ in range(len(matrix_sizes))]
            if(debug):
                print("P:",p)
            m = [m_val]
            for i in range(1, len(p)):
                m.append(m[i - 1] * p[i - 1])
            if(debug):
                print("M_VAL:",m)
            i = 0
            for n in matrix_sizes:
                # n = 2 ** size
                if(debug):
                    print("N:", n)
                flag = False
                l = 0
                try:
                    while(not flag):
                        if(func.level_condition(a, n, m, p, l)):
                        #if(3 * a * n > m[l] * p[l]):
                            l = l + 1
                            flag = False
                        else:
                            num_levels[i] = l
                            flag = True
                    i = i + 1
                except IndexError:
                    num_levels[i] = -1
                    i = i + 1
            if(debug):
                print("num_levels: ", num_levels)
            #b_energy = baseline_params_energy_calc(matrix_sizes, p, a)
            energy = calc_energy_wrapper(func, matrix_sizes, p, factors, m, num_levels)
            assert len(energy) == len(matrix_sizes)
            np_level.append(num_levels)
            np_energy.append(energy)
            #bp_energy.append(b_energy)
        new_sys_energy.append(np_energy)
        #baseline_energy.append(bp_energy)
        all_num_levels.append(np_level)
    return new_sys_energy, all_num_levels

def dram_calc_energy_wrapper(func, matrix_sizes, factors, p=None, a=None):
    dram_energy = []
    for size in matrix_sizes:
        energy = func.dram_energy(size, factors, a)
        dram_energy.append(energy)
    return dram_energy

def get_dram_energy_calc(func, matrix_sizes, p_sizes, factors, mem, a=8, debug=False):
    dram_energy = []
    for m_val in mem:
        dp_energy = []
        for p in p_sizes:
            energy = dram_calc_energy_wrapper(func, matrix_sizes, factors, p, a)
            dp_energy.append(energy)
        dram_energy.append(dp_energy)
    return dram_energy

def get_total_energy(comm_energy, energy_w_dram, num_levels):
    res = []
    #return list( map(add, comm_energy, energy_w_dram) )
    for i in range(len(energy_w_dram)):
        temp = []
        for j in range(len(energy_w_dram[i])):
            temp2 = []
            for k in range(len(energy_w_dram[i][j])):
                # print(i, j, k)
                if(num_levels[i][j][k] >= 0):
                    val = energy_w_dram[i][j][k] + comm_energy[i][j][k]
                else:
                    val = 0
                temp2.append(val)
            temp.append(temp2)
        res.append(temp)
    return res

def get_total_energy_imec(transfer_energy, cannon_energy, l4_energy):
    res = []
    #return list( map(add, comm_energy, energy_w_dram) )
    for i in range(len(cannon_energy)):
        temp = []
        for j in range(len(cannon_energy[i])):
            temp2 = []
            for k in range(len(cannon_energy[i][j])):
                # print(i, j, k)
                val = cannon_energy[i][j][k] + transfer_energy + l4_energy * 8100 # comm and comp cosr within MAC for each of 8100 processors
                temp2.append(val)
            temp.append(temp2)
        res.append(temp)
    return res

def get_energy_saving_factor(baseline_energy, new_sys_energy):
    energy_saving_factor = []
    max_energy_saving_factor = []
    print(len(new_sys_energy))
    for i in range(len(new_sys_energy)):
        temp = []
        m_energy = 0
        for j in range(len(new_sys_energy[i])):
            temp2 = []
            for k in range(len(new_sys_energy[i][j])):
                #print(i, j, k)
                try:
                    #print("In energy factor")
                    val = baseline_energy[i][j][k]/(new_sys_energy[i][j][k])
                    temp2.append(val)
                    m_energy = max(m_energy, val)
                except ZeroDivisionError:
                    temp2.append(0)
            temp.append(temp2)
        max_energy_saving_factor.append(m_energy)
        temp = np.asarray(temp, dtype=np.float64)
        #print(temp)
        energy_saving_factor.append(temp)
    return energy_saving_factor, max_energy_saving_factor

def get_transfer_energy(func, n, b, factor):
    return func.transfer_energy(n, b, factor)

def get_l4_energy(func, n, b, factor_comm, factor_comp):
    return func.l4_energy(n, b, factor_comm, factor_comp)