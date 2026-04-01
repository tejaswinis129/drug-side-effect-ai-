from app import DrugEnv

def inference():
    env = DrugEnv()
    result = env.step("Increase Dose")

    return {
        "result": {
            "health": result["health"],
            "side_effect": result["side_effect"],
            "drug": result["drug"],
            "reward": result["reward"]
        }
    }