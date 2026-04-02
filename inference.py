from app import DrugEnv

env = DrugEnv()

def inference(request: dict = {}):
    task = "drug-task"
    env_name = "drug_env"
    model = "custom-model"

    rewards = []
    steps = 0
    success = False

    # ✅ START (exact format)
    print(f"[START] task={task} env={env_name} model={model}", flush=True)

    try:
        action = request.get("action", "Increase Dose")

        result = env.step(action)

        reward = float(result["reward"])
        done = True  # single-step environment

        rewards.append(reward)
        steps += 1
        success = True

        # ✅ STEP (exact format)
        print(
            f"[STEP] step={steps} action={action} reward={reward:.2f} done={str(done).lower()} error=null",
            flush=True
        )

    except Exception as e:
        # error handling
        print(
            f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}",
            flush=True
        )
        rewards = [0.0]
        steps = 1
        success = False

    # ✅ END (exact format)
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True
    )

    return {
        "result": {
            "health": result["health"],
            "side_effect": result["side_effect"],
            "drug": result["drug"],
            "reward": result["reward"]
        }
    }