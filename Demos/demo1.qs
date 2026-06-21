namespace QuantumDemo1 {

    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Math;

    operation ApplyInverseQFT(register : Qubit[]) : Unit is Adj + Ctl {
        // This operation applies the inverse Quantum Fourier Transform(QFT) to the given register of qubits.
        //The inverse QFT is a key component in many quantum algorithms,

        let n = Length(register); // Get the number of qubits in the register
        let half = n / 2;
        for i in 0..half - 1 {
            SWAP(register[i], register[n - 1 - i]); // Swap the qubits to reverse their order
        }
        for i in (n - 1).. -1..0 {
            for j in (n - 1).. -1..(i + 1) {
                let angle = -2.0 * PI() / IntAsDouble(1 <<< (j - i + 1)); // Calculate the angle for the controlled rotation
                Controlled R1([register[j]], (angle, register[i])); // Apply the controlled rotation to the qubit at index i, controlled by the qubit at index j
            }
            H(register[i]); // Apply the Hadamard gate to the qubit at index i
        }
    }

    function CalculatePhaseWithPower(baseAngle : Double, power : Int) : Double {
        // This function calculates the phase by raising the base angle to the power of the given integer.

        if power < 0 { return 0.0; }
        return baseAngle^IntAsDouble(power);
    }

    operation PrepareSuperpositionWithPhase(q : Qubit, baseAngle : Double, power : Int) : Unit is Adj + Ctl {
        // This operation prepares a qubit in a superposition state with a specific phase determined by the base angle and power.

        let phase = CalculatePhaseWithPower(baseAngle, power); // Calculate the phase based on the base angle and power
        H(q); // Apply Hadamard gate to put the qubit in superposition
        Rz(phase, q); // Apply a rotation around the Z-axis by the calculated phase

    }

    @EntryPoint()
    operation RunDemo1() : Result[] {


        let baseAngle = 3.14159 / 2.0;
        mutable iterations = 3; // Number of iterations for phase calculation
        Message($"Running demo with base angle {baseAngle} and {iterations} iterations.");

        let calculatedPhase = CalculatePhaseWithPower(baseAngle, iterations);
        Message($"Calculated phase for base angle {baseAngle} and power {iterations}: {calculatedPhase}");

        use qubits = Qubit[5]; // Allocate 5 qubits for the demo
        let qcontrol = qubits[0]; // Control qubit for the controlled operations
        H(qcontrol); // Put control qubit in superposition
        let qtarget1 = qubits[1]; // Target qubit for the first controlled operation
        let qtarget2 = qubits[2]; // Target qubit for the second controlled operation
        let qtarget3 = qubits[3]; // Target qubit for the third controlled operation
        let qtarget4 = qubits[4]; // Target qubit for the fourth controlled operation
        Message("Preparing superposition with phase on target qubits...");
        PrepareSuperpositionWithPhase(qtarget1, baseAngle, iterations); // Prepare the first target qubit with the calculated phase
        PrepareSuperpositionWithPhase(qtarget2, baseAngle, iterations + 1); // Prepare the second target qubit with the calculated phase for the next power
        PrepareSuperpositionWithPhase(qtarget3, baseAngle, iterations + 2); // Prepare the third target qubit with the calculated phase for the next power
        PrepareSuperpositionWithPhase(qtarget4, baseAngle, iterations + 3); // Prepare the fourth target qubit with the calculated phase for the next power
        Message("Applying controlled operations...");
        Controlled Rz([qcontrol], (baseAngle, qtarget1)); // Apply controlled Rz rotation to the first target qubit
        Controlled Rz([qcontrol], (baseAngle * 2.0, qtarget2)); // Apply controlled Rz rotation to the second target qubit
        Controlled Rz([qcontrol], (baseAngle * 3.0, qtarget3)); // Apply controlled Rz rotation to the third target qubit
        Controlled Rz([qcontrol], (baseAngle * 4.0, qtarget4)); // Apply controlled Rz rotation to the fourth target qubit

        Message("Applying Inverse QFT on target qubits to decode phases...");
        let targetsRegister = [qtarget1, qtarget2, qtarget3, qtarget4]; // Create a register of target qubits for the Inverse QFT
        ApplyInverseQFT(targetsRegister); // Apply the Inverse Quantum Fourier Transform to decode the phases on the target qubits


        DumpMachine(); // Dump the state of the quantum machine for debugging and analysis
        Message("Measuring qubits...");
        let results = [M(qcontrol), M(qtarget1), M(qtarget2), M(qtarget3), M(qtarget4)]; // Measure the control and target qubits to obtain the results of the quantum operations
        Message($"Measurement results: {results}");
        ResetAll(qubits); // Reset all qubits to the |0⟩ state to clean up after the demo
        return results; // Return the measurement results for further analysis or verification

    }

}