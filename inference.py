import os
from huggingface_hub import login

login(os.getenv("HF_TOKEN"))

from app import DrugEnv, grader
import random

random.seed(42)

env = DrugEnv()

def run():
    scores = []

    # 3 TASKS (Easy, Medium, Hard)
    for task in range(3):
        state = env.reset()

        for step in range(15):
            action = random.randint(0, 3)
            state, reward, done = env.step(action)

            if done:
                break

        score = grader(state)
        scores.append(score)

        print(f"Task {task+1} Score:", score)

    print("\nFinal Scores:", scores)
    print("Average Score:", round(sum(scores)/len(scores), 2))


if __name__ == "__main__":
    run()