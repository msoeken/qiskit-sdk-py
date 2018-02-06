from qiskit import QuantumCircuit

from ._utils import _get_temporary_name, _exec_from_file

def permutation_oracle(qc, qr, permutation, **kwargs):
    """
    Synthesizes a permutation using RevKit.

    Given a permutation over `2**q` elements (starting from 0), this class helps
    to automatically find a reversible circuit over `q` qubits that realizes
    that permutation.
    """

    try:
        import revkit
    except ModuleNotFoundError:
        raise RuntimeError(
            "The RevKit Python library needs to be installed and in the "
            "PYTHONPATH in order to call this function")

    # permutation must start from 0, has no duplicates and all elements are consecutive
    if sorted(list(set(permutation))) != list(range(len(permutation))):
        raise AttributeError("Invalid permutation (does it start from 0?)")

    # permutation must have 2*q elements, where q is the number of qubits
    if 2**(len(qr)) != len(permutation):
        raise AttributeError(
            "Number of qubits does not fit to the size of the permutation")

    # create reversible truth table from permutation
    revkit.read_spec(permutation=" ".join(map(str, permutation)))

    # create reversible circuit from reversible truth table
    kwargs.get("synth", lambda: revkit.tbs())()    

    # write reversible circuit to QISKit code
    filename = _get_temporary_name()
    revkit.write_qiskit(filename=filename)

    # evaluate QISKit code in place
    _exec_from_file(filename, qc, qr)

QuantumCircuit.permutation_oracle = permutation_oracle