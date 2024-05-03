import math


class fft_graph:
    def init(self):
        pass

    def baseline_energy(self, n, p, a, f1, f2, f3=0.2):
        comm_factor = f1 * 2 * a * n * math.sqrt(p[0]) # f1 -> pJ/bit
        comp_factor = f2 * 5 * n * math.log((n / p[0]), 2) # f2 -> pJ/flop
        dram_factor = f3 * 2 * a * n # f3 -> pJ/bit
        energy = comm_factor + comp_factor + dram_factor
        #print(f'p: {p}, n:{n}, tech factpr:{dram_factorr}, comm_factor:{comm_factor}, energy: {energy}')
        return energy

    def new_sys_energy(self, i, n, p, m, factors, J_s=0, J_w=1, a=8, addition_factor =0):
        if(i < 0):
            return 0 # return 0 if the system can't calc the matrix
        if(i == 0):
            #print("In if I: ", i)
            #print(f'n :{n}, p: {p[i]}, levels: {i}, factors: {factors[i]}, J_s: {J_s}, J_w: {J_w}, a: {a}, addition_factor: {addition_factor}')
            return (J_s + J_w * factors[i] * a * (n) * math.sqrt(p[i])) + addition_factor
        else:
            #print("In else I: ", i)
            return (J_s + J_w * factors[i] * a * (n) * math.sqrt(p[i])) + self.new_sys_energy(i - 1, (n/p[i]), p, m, factors, addition_factor=addition_factor) * p[i] 
    
    def level_condition(self, a, n, m, p, l):
        return 2 * a * n > m[l] * p[l] # Does array fit in the memory of all the processors
    
    def dram_energy(self, n, factors, a):
        dram_energy = 0
        for i in range(3):
            dram_energy += 2 * 2 * a * n * factors[i] # 2 -> pJ (accessing RAM is 2x more expensive), 2 -> num of read and write
        return dram_energy
