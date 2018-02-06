from qiskit import QuantumProgram
from qiskit.extensions.revkit import phase_oracle

prog = QuantumProgram()

# allocate registers
qr = prog.create_quantum_register("qr", 4)
cr = prog.create_classical_register("cr", 4)
qc = prog.create_circuit("hws", [qr], [cr])

# step 1
qc.h(qr)

# step 2
qc.x(qr[0])
qc.phase_oracle(qr, 0x7888)
qc.x(qr[0])

# step 3
qc.h(qr)

# step 4
qc.phase_oracle(qr, 0x7888)

# step 5
qc.h(qr)

qc.measure(qr, cr)

result = prog.execute(["hws"])

print(result)
print(result.get_data("hws"))