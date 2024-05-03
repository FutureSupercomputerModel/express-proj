import main
import cannon_gemm
import plot_graph

matrix_sizes = [8, 10, 12, 14, 16, 18, 20, 22]
n = [2 ** i for i in matrix_sizes]
p_sizes = [[4096 for i in range(4)],
            [256 for i in range(4)],
            [128 for i in range(4)],
            [64 for i in range(4)],
            [32 for i in range(4)],
            [16 for i in range(4)],
            [8 for i in range(4)]]
mem = [2048, 16384, 65536]
# factors = [1, 100, 1000, 10000] 
factors = [0.01, 1, 100, 1000]  # energy factors in fJ in new architecture

a = 8

cannonGemmGraph = cannon_gemm.cannon_gemm()
baseline_energy = main.get_baseline_energy_calc(cannonGemmGraph, n, p_sizes, mem, a)
new_sys_energy, num_levels = main.get_new_sys_energy_calc(cannonGemmGraph, n, p_sizes, factors, mem, a=8)
dram_energy = main.get_dram_energy_calc(cannonGemmGraph, n, p_sizes, factors, mem, a=8)
new_sys_energy_w_dram = main.get_total_energy(new_sys_energy, dram_energy, num_levels)
energy_saving_factor, max_energy_saving_factor = main.get_energy_saving_factor(baseline_energy, new_sys_energy_w_dram)

for i in range(len(num_levels)):
    for j in range(len(num_levels[i])):
        for k in range(len(num_levels[i][j])):
            if(num_levels[i][j][k] >= 0):
                num_levels[i][j][k] = num_levels[i][j][k] + 1 # to shift 0-indexing to start from 1

plot_p = [4096, 256, 128, 64, 32, 16, 8]
for y_axis in range(len(energy_saving_factor)):
    title = f'm4 = {mem[y_axis]/1024} KB'
    plot_graph.plot_heatmap_graph(n, plot_p, energy_saving_factor[y_axis], num_levels[y_axis], max_energy_saving_factor[y_axis], title)