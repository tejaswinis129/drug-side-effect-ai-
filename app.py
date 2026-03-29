import random
import gradio as gr

random.seed(42)

class DrugEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.health = random.randint(40, 60)
        self.side_effect = random.randint(10, 30)
        self.drug = random.randint(1, 3)

    def step(self, action):
        if action == "Increase Dose":
            self.health += random.randint(5, 10)
            self.side_effect += random.randint(6, 10)
        elif action == "Decrease Dose":
            self.health -= random.randint(2, 6)
            self.side_effect -= random.randint(3, 7)
        elif action == "Switch Drug":
            self.drug = random.randint(1, 3)
            self.health += random.randint(3, 8)
            self.side_effect += random.randint(2, 6)
        else:
            self.health += random.randint(0, 3)
            self.side_effect += random.randint(0, 3)

        self.health = max(0, min(100, self.health))
        self.side_effect = max(0, min(100, self.side_effect))

        reward = (self.health * 1.2) - self.side_effect

        return f"Health: {self.health}\nSide Effect: {self.side_effect}\nDrug: {self.drug}\nReward: {round(reward,2)}"

env = DrugEnv()

def simulate(action):
    return env.step(action)

demo = gr.Interface(
    fn=simulate,
    inputs=gr.Dropdown(["Increase Dose", "Decrease Dose", "Switch Drug", "Maintain"]),
    outputs="text",
    title="💊 Drug Side Effect AI"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)