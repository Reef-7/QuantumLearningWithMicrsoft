import sys
import random
import pygame
import qsharp

# Initialize the Q# environment linking to the current workspace
qsharp.init()

# Animation screen configuration
WIDTH, HEIGHT = 800, 400
FPS = 60

# Color palette definition (HEX inspired RGB)
BACKGROUND = (20, 24, 33)
WHITE = (240, 240, 245)
CYAN = (0, 255, 240)
MAGENTA = (255, 0, 128)
GRAY = (80, 85, 100)
GREEN = (50, 205, 50)
PURPLE = (147, 112, 219) # New color for CNOT gate visual links

class QuantumAnimation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Quantum Random Number Generator - Live Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.big_font = pygame.font.SysFont("Arial", 40)
        self.reset_simulation()

    def reset_simulation(self):
        """Fetches real results from Q# circuit and resets animation states."""
        try:
            res_a, res_b = qsharp.eval("QuantumRandomCircuit.RunRandomCircuit()")
            self.quantum_res_a = 1 if str(res_a) == "One" else 0
            self.quantum_res_b = 1 if str(res_b) == "One" else 0
        except Exception:
            self.quantum_res_a = random.choice([0, 1])
            self.quantum_res_b = random.choice([0, 1])

        # Hardware component positioning coordinates (Shifted M gate to make room for CNOT)
        self.gate_h_x = 200
        self.gate_cnot_x = 400  # NEW: CNOT gate position right in the middle
        self.gate_m_x = 600
        
        # Qubit visual properties (X_pos, Y_pos, current_display_state, animation_flag)
        self.qA = {"x": 50, "y": 150, "color": CYAN, "state": "0", "spinning": False}
        self.qB = {"x": 50, "y": 250, "color": MAGENTA, "state": "0", "spinning": False}
        
        # Simulation stages: MOVING_TO_H, IN_SUPERPOSITION, MOVING_TO_CNOT, IN_CNOT, MOVING_TO_M, COLLAPSED
        self.stage = "MOVING_TO_H" 
        self.superposition_timer = 0
        self.cnot_timer = 0  # NEW: Timer to hold qubits inside CNOT interaction phase

    def draw_circuit_lines(self):
        """Renders static quantum wire pathways, gates, and baseline text labels."""
        # Drawing horizontal quantum wire rails
        pygame.draw.line(self.screen, GRAY, (50, 150), (750, 150), 3)
        pygame.draw.line(self.screen, GRAY, (50, 250), (750, 250), 3)
        
        # Labeling input Qubits
        self.screen.blit(self.font.render("qA", True, WHITE), (15, 135))
        self.screen.blit(self.font.render("qB", True, WHITE), (15, 235))

        # Rendering Hadamard (H) Gate hardware boxes
        for y in [150, 250]:
            pygame.draw.rect(self.screen, CYAN, (self.gate_h_x - 25, y - 25, 50, 50), 0, 5)
            self.screen.blit(self.font.render("H", True, BACKGROUND), (self.gate_h_x - 8, y - 13))

        # NEW: Rendering static CNOT target blueprint (Control dot on wire A, Target cross on wire B)
        pygame.draw.circle(self.screen, PURPLE, (self.gate_cnot_x, 150), 6)
        pygame.draw.line(self.screen, PURPLE, (self.gate_cnot_x, 150), (self.gate_cnot_x, 250), 2)
        pygame.draw.circle(self.screen, PURPLE, (self.gate_cnot_x, 250), 15, 2)
        pygame.draw.line(self.screen, PURPLE, (self.gate_cnot_x - 10, 250), (self.gate_cnot_x + 10, 250), 2)
        pygame.draw.line(self.screen, PURPLE, (self.gate_cnot_x, 240), (self.gate_cnot_x, 260), 2)

        # Rendering Measurement (M) Gate hardware boxes
        for y in [150, 250]:
            pygame.draw.rect(self.screen, MAGENTA, (self.gate_m_x - 25, y - 25, 50, 50), 0, 5)
            self.screen.blit(self.font.render("M", True, WHITE), (self.gate_m_x - 8, y - 13))

    def update_qubits(self):
        """Handles physical translation vectors and timeline mechanics for both Qubits."""
        speed = 4
        
        # Stage 1: Continuous linear transition towards the Hadamard gates
        if self.stage == "MOVING_TO_H":
            self.qA["x"] += speed
            self.qB["x"] += speed
            if self.qA["x"] >= self.gate_h_x:
                self.stage = "IN_SUPERPOSITION"
                self.qA["spinning"] = True
                self.qB["spinning"] = True

        # Stage 2: Qubits locked in H gate, rendering rapid flickering to simulate |+⟩ state
        elif self.stage == "IN_SUPERPOSITION":
            self.superposition_timer += 1
            self.qA["state"] = str(random.choice([0, 1]))
            self.qB["state"] = str(random.choice([0, 1]))
            if self.superposition_timer > 60: # Decreased slightly for better pace
                self.stage = "MOVING_TO_CNOT" # NEW: Diverting trajectory to CNOT instead of M
                self.qA["spinning"] = False
                self.qB["spinning"] = False

        # NEW: Stage 2.5: Move towards CNOT gate
        elif self.stage == "MOVING_TO_CNOT":
            self.qA["x"] += speed
            self.qB["x"] += speed
            # Maintain the rapid spin look slightly while traveling since wave function is intact
            self.qA["state"] = str(random.choice([0, 1]))
            self.qB["state"] = str(random.choice([0, 1]))
            if self.qA["x"] >= self.gate_cnot_x:
                self.stage = "IN_CNOT"

        # NEW: Stage 2.6: CNOT Interaction (Mixing their superpositions together)
        elif self.stage == "IN_CNOT":
            self.cnot_timer += 1
            # Entanglement mixing behavior visualization (syncing states instantly or flipping)
            self.qA["state"] = str(random.choice([0, 1]))
            self.qB["state"] = self.qA["state"]  # Demonstrating joint dependency state visually
            if self.cnot_timer > 45: # Hold for about 0.75 seconds
                self.stage = "MOVING_TO_M"
                self.cnot_timer = 0

        # Stage 3: Traversing the wire towards Measurement Gates
        elif self.stage == "MOVING_TO_M":
            self.qA["x"] += speed
            self.qB["x"] += speed
            self.qA["state"] = str(random.choice([0, 1]))
            self.qB["state"] = str(random.choice([0, 1]))
            if self.qA["x"] >= self.gate_m_x:
                self.stage = "COLLAPSED"
                # Sudden wave-function collapse triggered by M gate evaluation
                self.qA["state"] = str(self.quantum_res_a)
                self.qB["state"] = str(self.quantum_res_b)

        # Stage 4: Exiting the circuit gates as classical binary data chunks
        elif self.stage == "COLLAPSED":
            if self.qA["x"] < 720:
                self.qA["x"] += speed
                self.qB["x"] += speed

    def draw_qubits(self):
        """Renders dynamic Qubit object payloads onto the active viewport."""
        for q in [self.qA, self.qB]:
            # Emitting a wave-function blur radius if currently superposition-locked
            if q["spinning"] or self.stage == "IN_CNOT":
                pygame.draw.circle(self.screen, WHITE, (q["x"], q["y"]), 25, 2)
            
            # Rendering core particle boundary
            pygame.draw.circle(self.screen, q["color"], (q["x"], q["y"]), 18)
            
            # Drawing the inner real-time state payload (0, 1, or flickering)
            state_text = self.font.render(q["state"], True, BACKGROUND)
            self.screen.blit(state_text, (q["x"] - 6, q["y"] - 13))

    def draw_ui(self):
        """Displays responsive HUD text alerts indicating current engine execution phase."""
        if self.stage == "COLLAPSED":
            res_text = f"Result: ({self.quantum_res_a}, {self.quantum_res_b})"
            text_surf = self.big_font.render(res_text, True, GREEN)
            self.screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, 40))
            
            hint = self.font.render("Press SPACE to run again", True, WHITE)
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 330))
        else:
            status_map = {
                "MOVING_TO_H": "Allocating Qubits: Entering Circuit...",
                "IN_SUPERPOSITION": "Hadamard Gate: Entering Individual Superposition (0 AND 1)!",
                "MOVING_TO_CNOT": "Moving towards CNOT interaction zone...",
                "IN_CNOT": "CNOT Gate: Mixing superpositions into a joint combined state!",
                "MOVING_TO_M": "Moving to measurement gates with joint wave function...",
            }
            curr_text = status_map.get(self.stage, "")
            text_surf = self.font.render(curr_text, True, WHITE)
            self.screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, 40))

    def run(self):
        """Core application lifecycle execution loop."""
        running = True
        while running:
            self.screen.fill(BACKGROUND)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    # Allow iterative workflow looping via Spacebar on completion
                    if event.key == pygame.K_SPACE and self.stage == "COLLAPSED":
                        self.reset_simulation()

            self.draw_circuit_lines()
            self.update_qubits()
            self.draw_qubits()
            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = QuantumAnimation()
    app.run()
