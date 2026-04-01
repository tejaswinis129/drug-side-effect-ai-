from app import DrugEnv

def inference(request=None):   # ✅ allow None

    # ✅ handle all cases safely
    action = "Increase Dose"

    if isinstance(request, dict):
        action = request.get("action", "Increase Dose")

    env = DrugEnv()
    result = env.step(action)

    return {
        "result": {
            "health": result["health"],
            "side_effect": result["side_effect"],
            "drug": result["drug"],
            "reward": result["reward"]
        }
    }