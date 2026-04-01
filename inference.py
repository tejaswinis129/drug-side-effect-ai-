from app import DrugEnv

def inference(request: dict):
    # ✅ handle missing input safely
    action = request.get("action") if request else None

    if not action:
        action = "Increase Dose"   # default fallback

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