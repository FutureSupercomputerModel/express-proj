import main
import math
import cannon_gemm
import plot_graph

#matrix_sizes = [8, 10, 12, 14] # sizes that fit into the 90 * 90 * 20 MB
#n = [2 ** i for i in matrix_sizes]
def get_b_1(n, a, p, m):
    if(n * n * a * 3 <= p * m):
        return 1
    else:
        return (n * n * a * 3) / 8100
    
def get_b_2(n, p, mac):
    if(n * n <= p * mac * mac):
        return 1
    else:
        return ((n * n) / (8100 * 200))
    
matrix_sizes = [180, 270, 900, 1800, 4050, 8100, 16200, 40500, 64800, 81000, 121500, 259200, 1036800, 4147200] # n*n are multiples of 8100
# n = [270, 900, 4050, 64800, 259200, 1036800, 4147200]
# p_sizes = [[4096 for i in range(4)],
#             [256 for i in range(4)],
#             [128 for i in range(4)],
#             [64 for i in range(4)],
#             [32 for i in range(4)],
#             [16 for i in range(4)],
#             [8 for i in range(4)]]
# mem = [2048, 16384, 65536]
# IMEC system p & m:
p_sizes = [[8100]] # level-4 = 9*9, level-3 = 10*10, level-2 = 2*2, level-1 = 2*2
mem = [20971520] #20 MB
# factors = [1, 100, 1000, 10000] 
factors = [0.2]  #in fJ
factor_1 = 4.24
factor_comm_0 = 0.2 #in pJ
factor_comp_0 = 0.014 #in pJ
a = 8
mac = 200

cannonGemmGraph = cannon_gemm.cannon_gemm()
baseline_energy = main.get_baseline_energy_calc(cannonGemmGraph, matrix_sizes, p_sizes, mem, a)
transfer_energy = []
l4_energy = []
n_1 = []

for n in matrix_sizes:
    b_1 = get_b_1(n, a, p_sizes[0][0], mem[0])
    n_1_temp = n / math.sqrt(b_1)
    n_1.append(n_1_temp)
    n_on_each_proc = n_1_temp / 90
    b_0 = get_b_2(n, p_sizes[0][0], mac)
    n_0 = n_on_each_proc / math.sqrt(b_0)
    transfer_energy_temp = main.get_transfer_energy(cannonGemmGraph, n_1_temp, b_1, factor_1)
    transfer_energy.append(transfer_energy_temp)
    l4_energy_temp = main.get_l4_energy(cannonGemmGraph, n_0, b_0, factor_comm_0, factor_comp_0)
    l4_energy.append(l4_energy_temp)


new_sys_energy, num_levels = main.get_new_sys_energy_calc(cannonGemmGraph, n_1, p_sizes, factors, mem, a=8)
print(new_sys_energy)
print(transfer_energy)
print(l4_energy)

total_energy = main.get_total_energy_imec(transfer_energy, new_sys_energy, l4_energy)
print(total_energy)
energy_saving_factor, max_energy_saving_factor = main.get_energy_saving_factor(baseline_energy, new_sys_energy)
# for i in range(len(num_levels)):
#     for j in range(len(num_levels[i])):
#         for k in range(len(num_levels[i][j])):
#             if(dram_energy[i][j][k] > baseline_energy[i][j][k]):
#                 print("Yes")
#             else:
#                 print("No")
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