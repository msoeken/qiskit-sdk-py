from qiskit import QuantumCircuit

from ._utils import _get_temporary_name, _exec_from_file

def phase_oracle(qc, qr, function, **kwargs):
    """
    Synthesizes phase circuit from an arbitrary Boolean function.

    This creates a phase circuit from a Boolean function.  It inverts the phase
    of all amplitudes for which the function evaluates to 1.  The Boolean
    function is provided as integer representation of the function's truth table
    in binary notation.  For example, for the majority-of-three function, which
    truth table 11101000, the value for function can be, e.g., ``0b11101000,
    ``0xe8``, or ``232``.
    """

    try:
        import revkit
    except ModuleNotFoundError:
        raise RuntimeError(
            "The RevKit Python library needs to be installed and in the "
            "PYTHONPATH in order to call this function")

    if not isinstance(function, int):
        import dormouse
        function = dormouse.to_truth_table(function)

    # function truth table must be non-negative and cannot be larger than number of control qubits allow
    if function < 0 or 2**(2**len(qr)) <= function:
        raise AttributeError(
            "Function truth table exceeds number of control qubits")

    # create truth table from function integer
    revkit.tt(load="0d{}:{}".format(len(qr), function))

    # translate truth table into AIG
    revkit.convert(tt_to_aig = True)

    # create phase circuit from AIG
    kwargs.get("synth", lambda: revkit.esopps())()    

    # check whether circuit has correct signature
    if revkit.ps(circuit = True, silent = True)['lines'] != len(qr):
        raise RuntimeError("Generated circuit lines does not match provided qubits")

    # write phase circuit to QISKit code
    filename = _get_temporary_name()
    revkit.write_qiskit(filename=filename)

    # evaluate QISKit code in place
    _exec_from_file(filename, qc, qr)

QuantumCircuit.phase_oracle = phase_oracle