import random
import gradio as gr
import matplotlib.pyplot as plt

random.seed(42)

class DrugEnv:
    def __init__(self):
        self.drugs = ["Paracetamol", "Ibuprofen", "Amoxicillin"]
        self.reset()

    def reset(self):
        self.health = random.randint(40, 60)
        self.side_effect = random.randint(10, 30)
        self.drug = random.choice(self.drugs)

    def step(self, action):

        # 🔹 ACTION EFFECT
        if action == "Increase Dose":
            self.health += random.randint(5, 10)
            self.side_effect += random.randint(6, 10)

        elif action == "Decrease Dose":
            self.health -= random.randint(2, 6)
            self.side_effect -= random.randint(3, 7)

        elif action == "Switch Drug":
            self.drug = random.choice(self.drugs)
            self.health += random.randint(3, 8)
            self.side_effect += random.randint(2, 6)

        elif action == "Maintain":
            self.health += random.randint(0, 3)
            self.side_effect += random.randint(0, 3)

        # 🔹 MEDICINE EFFECT
        if self.drug == "Paracetamol":
            self.health += 5
            self.side_effect += 2

        elif self.drug == "Ibuprofen":
            self.health += 7
            self.side_effect += 5

        elif self.drug == "Amoxicillin":
            self.health += 6
            self.side_effect += 3

        # 🔹 Clamp values
        self.health = max(0, min(100, self.health))
        self.side_effect = max(0, min(100, self.side_effect))

        reward = (self.health * 1.2) - self.side_effect

        return {
            "health": self.health,
            "side_effect": self.side_effect,
            "drug": self.drug,
            "reward": round(reward, 2)
        }


# ✅ Grader
def grader(state):
    score = (state["health"]/100) - (state["side_effect"]/100)
    return max(0, min(1, round(score, 2)))


# 🌐 UI + GRAPH
env = DrugEnv()
history_health = []
history_side = []

def simulate(action):
    result = env.step(action)

    history_health.append(result["health"])
    history_side.append(result["side_effect"])

    plt.figure()
    plt.plot(history_health, marker='o', label="Health")
    plt.plot(history_side, marker='o', label="Side Effect")
    plt.legend()
    plt.xlabel("Steps")
    plt.ylabel("Values")
    plt.title("Health vs Side Effects")

    return (
        f"""Health: {result['health']}
Side Effect: {result['side_effect']}
Drug: {result['drug']}
Reward: {result['reward']}""",
        plt.gcf()
    )


demo = gr.Interface(
    fn=simulate,
    inputs=gr.Dropdown(
        ["Increase Dose", "Decrease Dose", "Switch Drug", "Maintain"],
        label="Choose Action"
    ),
    outputs=[gr.Textbox(), gr.Plot()],
    title="💊 Drug Side Effect AI with Visualization"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)