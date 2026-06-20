namespace QuantumRandomCircuit {

    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;

    @EntryPoint()
    operation RunRandomCircuit() : (Result, Result) {
        // Two Random Qubits Allocation
        use (qA, qB) = (Qubit(), Qubit());

        // 1. First Qubit Preparation - Hadamard Gate (Superposition)
        H(qA);

        // 2. Second Qubit Preparation
        H(qB);

        // 3. New Element: Creating a joint superposition between them
        // This entangles/mixes their individual superpositions into a combined state
        CNOT(qA, qB);


        // 4. Measurement Function - Triggers Wave Function Collapse
        // The two qubits collapse simultaneously to classical states
        let resultA = M(qA);
        let resultB = M(qB);

        // Mandatory Reset before releasing the qubits
        Reset(qA);
        Reset(qB);

        // Return the results after the collapse
        return (resultA, resultB);
    }
}
