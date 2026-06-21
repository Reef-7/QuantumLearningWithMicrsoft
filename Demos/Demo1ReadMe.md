# Quantum Phase & Inverse QFT Demo in Q#

This Demo contains a beginner-friendly yet robust **Q# (Quantum)** project demonstrating quantum state preparation, controlled phase rotations, and phase decoding using the **Inverse Quantum Fourier Transform**.

This project is a great showcase of fundamental quantum computing algorithms implemented from scratch in Microsoft's Q# language.

## 🚀 What This Code Does

The program executes a complete quantum routine across 5 qubits:
1. **State Preparation:** It allocates 5 qubits. One acts as a control qubit, and the other 4 are target qubits.
2. **Superposition & Phase Encoding:** It puts the target qubits into a superposition state and applies unique, power-scaled phase shifts to each of them using custom logic.
3. **Controlled Operations:** Applies conditional `Rz` rotations controlled by the first qubit.
4. **Phase Decoding (Inverse QFT):** It runs a custom implementation of the **Inverse Quantum Fourier Transform** to translate the phases encoded in the target qubits back into basis states (\(\vert{}0\rangle\) or \(\vert{}1\rangle\)) that can be measured.
5. **State Inspection & Measurement:** It utilizes `DumpMachine()` to output the full quantum state for debugging, measures the qubits, and resets them.

## 🛠️ Project Structure & Key Components

* **`ApplyInverseQFT`**: A manual, step-by-step implementation of the Inverse QFT algorithm. It uses `SWAP` gates to reverse qubit order, followed by controlled-phase rotations (`Controlled R1`) and Hadamard (`H`) gates.
* **`PrepareSuperpositionWithPhase`**: Prepares a clean superposition with calculated phase angles.
* **`RunDemo1`**: The `@EntryPoint()` that coordinates the entire execution flow from allocation to measurement.

## 💻 How to Run This Project

### Prerequisites
Make sure you have the modern Azure Quantum Development Kit (QDK) extension installed in **VS Code**, or the modern Q# compiler tools.

### Execution Steps
1. Open the project folder in VS Code.
2. Simply click the **"Run"** or **"Debug"** button above the `@EntryPoint()` macro in your Q# file, or use your terminal environment to run the simulation.

## 📊 Sample Output Reference
When executed, the program will output logs similar to this in your debug console:
```text
Running demo with base angle 1.570795 and 3 iterations.
Calculated phase for base angle 1.570795 and power 3: 3.87578
Preparing superposition with phase on target qubits...
Applying controlled operations...
Applying Inverse QFT on target qubits to decode phases...
[DumpMachine Output Showcasing Quantum Amplitudes]
Measuring qubits...
Measurement results: [Zero, One, Zero, One, Zero]
```

## 📊 Actual Simulation Output
When executed, the program outputs the following state distribution before measurement, successfully demonstrating constructive interference around the encoded phases:

```text
Running demo with base angle 1.570795 and 3 iterations.
Calculated phase for base angle 1.570795 and power 3: 3.8757747638402096
Preparing superposition with phase on target qubits...
Applying controlled operations...
Applying Inverse QFT on target qubits to decode phases...

 Basis   | Amplitude      | Probability | Phase
 -------------------------------------------------

 |00000⟩ |  0.0059+0.0000𝑖 |     0.0034% |  -0.0000
 ...

 |10010⟩ |  0.3978+0.1648𝑖 |    18.5428% |   0.3927  <-- High Probability Peak
 ...

 |11010⟩ |  0.1820−0.4393𝑖 |    22.6131% |  -1.1781  <-- Maximum Probability Peak
 ...

Measuring qubits...
Measurement results: [Zero, Zero, Zero, One, One]
```
## ⚠️ Important Note on Phase Leakage (The "Power" Experiment)

You might notice in the output that in the given example, the maximum probability peak is around **22.6%** and the final measurement collapsed into a lower-probability state (`|00011⟩`). 

**This is expected and is a core feature of this experiment:**
* **Non-Linear Phases:** Standard Inverse QFT relies on a strict binary geometric progression ($\theta, 2\theta, 4\theta$). In this demo, the phases are calculated using exponents ($\theta^1, \theta^2, \theta^3$) via `CalculatePhaseWithPower`.
* **Probability Leakage:** Because exponent-based phases do not align cleanly with the binary basis of the QFT circuit, it breaks the perfect constructive interference. 
* **The Result:** Instead of converging 100% onto a single computational state, the probability "leaks" across multiple states, demonstrating the chaotic and probabilistic nature of misaligned quantum phases.


## What I Learned From This Project
* How to manipulate quantum phases using `Rz` and `R1` gates.
* Manual implementation of the **Inverse QFT** circuit layout.
* Managing qubit lifecycles cleanly using `use` blocks and `ResetAll`.
* Using `DumpMachine()` for testing and debugging quantum states.

