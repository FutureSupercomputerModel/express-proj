import main
import math
import cannon_gemm
import plot_graph


def get_b_1(n, a, p, m):
    '''
    If the overall matrix size of all the three matrices 
    fit in 8100 processors (8100 * 20MB), no blocking is needed, 
    otherwise, divide into 8100 blocks.
    '''
    if(n * n * a * 3 <= p * m):
        return 1
    else:
        return 8100
    
def get_b_2(n, mac):
    '''
    If the matrix held by each of the 8100 processor is 
    less than 200 * 200, then no blocking is needed. 
    Otherwise, need blocking.
    '''
    if(n * n <= mac * mac):
        return 1
    else:
        b = 1
        while(n * n > mac * mac):
            b = b * 4
            n = n / 2
        return b
    
matrix_sizes = [270, 1800, 4050, 16200, 64800, 121500, 259200, 1036800, 4147200] # n*n are multiples of 8100
# IMEC system p & m:
p_sizes = [[8100]] # level-4 = 9*9 * 10 *10
mem = [20971520] #20 MB
factors = [0.2]  #in pJ
factor_1 = 4.24 #in pJ
factor_comm_0 = 0.2 #in pJ
factor_comp_0 = 0.014 #in pJ
a = 8
mac = 200 # 200 * 200 MAC within each 9 * 9 processor

cannonGemmGraph = cannon_gemm.cannon_gemm()
baseline_energy = main.get_baseline_energy_calc(cannonGemmGraph, matrix_sizes, p_sizes, mem, a) #in pJ
transfer_energy = []
l4_energy = []
n_1 = []

for n in matrix_sizes:
    b_1 = get_b_1(n, a, p_sizes[0][0], mem[0])
    n_1_temp = n / math.sqrt(b_1)
    n_1.append(n_1_temp)
    n_on_each_proc = n_1_temp / 90
    b_0 = get_b_2(n_on_each_proc, p_sizes[0][0], mac)
    n_0 = n_on_each_proc / math.sqrt(b_0)
    # print(n, " ", b_1, " ", n_1_temp, " ", n_on_each_proc, " ", b_0, " ", n_0)
    transfer_energy_temp = main.get_transfer_energy(cannonGemmGraph, n_1_temp, b_1, factor_1)
    transfer_energy.append(transfer_energy_temp)
    l4_energy_temp = main.get_l4_energy(cannonGemmGraph, n_0, b_0, factor_comm_0, factor_comp_0)
    l4_energy.append(l4_energy_temp)


new_sys_energy, num_levels = main.get_new_sys_energy_calc(cannonGemmGraph, n_1, p_sizes, factors, mem, a=8)
# print(new_sys_energy)
# print(transfer_energy)
# print(l4_energy)

total_energy = main.get_total_energy_imec(transfer_energy, new_sys_energy, l4_energy)
# print(total_energy)
energy_saving_factor, max_energy_saving_factor = main.get_energy_saving_factor(baseline_energy, new_sys_energy, conversion_factor=1) #as both energies are in pJ, conversion_factor=1

for i in range(len(num_levels)):
    for j in range(len(num_levels[i])):
        for k in range(len(num_levels[i][j])):
            if(num_levels[i][j][k] >= 0):
                num_levels[i][j][k] = num_levels[i][j][k] + 1

#plot_p = [4096, 256, 128, 64, 32, 16, 8]
plot_p = [8100]
for y_axis in range(len(energy_saving_factor)):
    # title = f'm4 = {mem[y_axis]/1024} KB'
    title = f'm4 = {mem[y_axis]/(1024 * 1024)} MB'
    plot_graph.plot_heatmap_graph(matrix_sizes, plot_p, energy_saving_factor[y_axis], num_levels[y_axis], max_energy_saving_factor[y_axis], title)