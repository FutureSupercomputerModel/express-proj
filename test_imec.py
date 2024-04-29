import main
import math
import cannon_gemm
import plot_graph

#matrix_sizes = [8, 10, 12, 14] # sizes that fit into the 90 * 90 * 20 MB
#n = [2 ** i for i in matrix_sizes]
n = [180, 270, 900, 1800, 4050, 8100, 16200] # n*n are multiples of 8100
# p_sizes = [[4096 for i in range(4)],
#             [256 for i in range(4)],
#             [128 for i in range(4)],
#             [64 for i in range(4)],
#             [32 for i in range(4)],
#             [16 for i in range(4)],
#             [8 for i in range(4)]]
# mem = [2048, 16384, 65536]
# IMEC system p & m:
p_sizes = [[8100, 1]] # level-4 = 9*9, level-3 = 10*10, level-2 = 2*2, level-1 = 2*2
mem = [20971520] #20 MB
# factors = [1, 100, 1000, 10000] 
factors = [0.2]  #in fJ

a = 8

cannonGemmGraph = cannon_gemm.cannon_gemm()
baseline_energy = main.get_baseline_energy_calc(cannonGemmGraph, n, p_sizes, mem, a)
new_sys_energy, num_levels = main.get_new_sys_energy_calc(cannonGemmGraph, n, p_sizes, factors, mem, a=8)
print(new_sys_energy)
factor_1 = 4.24 #in pJ
b_1 = 8100
n_1 = int(math.sqrt((n[0] * n[0]) / b_1))
transfer_energy = main.get_transfer_energy(cannonGemmGraph, n_1, b_1, factor_1)
#transfer_energy = 0
factor_comm_0 = 0.2 #in pJ
factor_comp_0 = 0.014 #in pJ
b_0 = n_1/200 
l4_energy = main.get_l4_energy(cannonGemmGraph, n_1, b_0, factor_comm_0, factor_comp_0)
print(transfer_energy)
print(l4_energy)
# dram_energy = main.get_dram_energy_calc(cannonGemmGraph, n, p_sizes, factors, mem, a=8)
# new_sys_energy_w_dram = main.get_total_energy(new_sys_energy, dram_energy, num_levels)
# print(new_sys_energy_w_dram)
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
    plot_graph.plot_heatmap_graph(n, plot_p, energy_saving_factor[y_axis], num_levels[y_axis], max_energy_saving_factor[y_axis], title)