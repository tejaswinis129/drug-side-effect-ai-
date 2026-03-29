import random

random.seed(42)

class DrugEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.health = random.randint(40, 60)
        self.side_effect = random.randint(10, 30)
        self.drug = random.randint(1, 3)
        return self.get_state()

    def get_state(self):
        return {
            "health": self.health,
            "side_effect": self.side_effect,
            "drug": self.drug
        }

    def step(self, action):
        """
        Actions:
        0 = decrease dose
        1 = increase dose
        2 = switch drug
        3 = maintain
        """

        if action == 1:
            self.health += random.randint(5, 10)
            self.side_effect += random.randint(6, 10)

        elif action == 0:
            self.health -= random.randint(2, 6)
            self.side_effect -= random.randint(3, 7)

        elif action == 2:
            self.drug = random.randint(1, 3)
            self.health += random.randint(3, 8)
            self.side_effect += random.randint(2, 6)

        elif action == 3:
            self.health += random.randint(0, 3)
            self.side_effect += random.randint(0, 3)

        # Clamp values
        self.health = max(0, min(100, self.health))
        self.side_effect = max(0, min(100, self.side_effect))

        reward = (self.health * 1.2) - self.side_effect

        done = self.health > 90 and self.side_effect < 20

        return self.get_state(), reward, done


def grader(state):
    """
    Score between 0 and 1
    """
    score = (state["health"] / 100) - (state["side_effect"] / 100)
    return max(0, min(1, round(score, 2)))