import math

class cannon_gemm:
    def init(self):
        pass

    def baseline_energy(self, n, p, a, f1, f2):
        energy = 40 * n * n * n
        return energy

    def new_sys_energy(self, i, n, p, m, factors, J_s=0, J_w=1, a=8, addition_factor =0):
        if(i < 0):
            return 0 # return 0 if the system can't calc the matrix
        if(i == 0):
            #print("In if I: ", i)
            #print(f'n :{n}, p: {p[i]}, levels: {i}, factors: {factors[i]}, J_s: {J_s}, J_w: {J_w}, a: {a}, addition_factor: {addition_factor}')
            return 2 * (J_s + J_w * factors[i] * a * (n * n) * math.sqrt(p[i])) + addition_factor
        else:
            #print("In else I: ", i)
            return 2 * (J_s + J_w * factors[i] * a * (n * n) * math.sqrt(p[i])) + self.new_sys_energy(i - 1, (n/math.sqrt(p[i])), p, m, factors, addition_factor=addition_factor) * p[i] 
    
    def dram_energy(self, n, factors, a):
        dram_energy = 0
        for i in range(len(factors)):
            dram_energy += 2 * 4 * a * n * n * factors[i] # 2 -> pJ (accessing RAM is 2x more expensive), 4 -> num of read and write
        return dram_energy * 0
    
    def level_condition(self, a, n, m, p, l):
        return 3 * a * n * n > m[l] * p[l] # Does matrix fit in the memory of all the processors
    
    def transfer_energy(self, n, b, factor):
        return (n * n * b * (2 * math.sqrt(b) + 1) * factor) / 4 # For IMEC, the tranfer energy from HBM to 8100
    
    def l4_energy(self, n, b, factor_comm, factor_comp):
        comm_energy = (((n * n * b * (2 * math.sqrt(b) + 1)) * factor_comm) / 4) # Tranfer energy from 8100 to 200 MAC, 4 in denominator is for BFlop
        comp_energy = 2 * n * n * n * factor_comp # Flops energy
        return comm_energy + comp_energy