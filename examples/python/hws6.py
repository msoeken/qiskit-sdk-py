from qiskit import QuantumProgram
from qiskit.extensions.revkit import phase_oracle, permutation_oracle

import revkit

prog = QuantumProgram()

# allocate registers
qr = prog.create_quantum_register("qr", 6)
cr = prog.create_classical_register("cr", 6)
qc = prog.create_circuit("hws", [qr], [cr])

x = [qr[0], qr[2], qr[4]]
y = [qr[1], qr[3], qr[5]]

pi = [0,2,3,5,7,1,4,6]

def f(a, b, c, d, e, f):
    return (a and b) ^ (c and d) ^ (e and f)

# step 1
qc.h(qr)

# step 2
qc.x(x[0])
qc.x(x[1])
qc.permutation_oracle(y, pi)
qc.phase_oracle(qr, f)
qc.permutation_oracle(y, pi, synth = lambda: [revkit.tbs(), revkit.reverse()])
qc.x(x[1])
qc.x(x[0])

# step 3
qc.h(qr)

# step 4
qc.permutation_oracle(x, pi, synth = lambda: [revkit.dbs(), revkit.pos(), revkit.reverse()])
qc.phase_oracle(qr, f)
qc.permutation_oracle(x, pi, synth = lambda: [revkit.dbs(), revkit.pos()])

# step 5
qc.h(qr)

qc.measure(qr, cr)

result = prog.execute(["hws"], shots=1)

print(result)
print(result.get_data("hws"))