from app import DrugEnv

env = DrugEnv()

def inference(request: dict):
    task = "drug-task"
    env_name = "drug_env"
    model = "custom-model"

    rewards = []
    steps = 0
    success = False

    print(f"[START] task={task} env={env_name} model={model}", flush=True)

    try:
        action = request.get("action", "Increase Dose")

        result = env.step(action)

        reward = float(result["reward"])
        done = True

        rewards.append(reward)
        steps = 1
        success = True

        print(
            f"[STEP] step=1 action={action} reward={reward:.2f} done=true error=null",
            flush=True
        )

    except Exception as e:
        print(
            f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}",
            flush=True
        )
        rewards = [0.0]
        steps = 1
        success = False

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True
    )

    return {"result": result}