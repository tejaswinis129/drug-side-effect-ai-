from app import DrugEnv
import os
from openai import OpenAI

env = DrugEnv()

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

def inference():
    task = "drug-llm"
    env_name = "drug_env"
    model = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

    rewards = []
    steps = 0
    success = False

    print(f"[START] task={task} env={env_name} model={model}", flush=True)

    try:
        state = env.state()

        prompt = f"""
        Patient state:
        Health: {state['health']}
        Side effect: {state['side_effect']}
        Drug: {state['drug']}

        Choose best action:
        Increase Dose / Decrease Dose / Switch Drug / Maintain
        """

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20
        )

        action = response.choices[0].message.content.strip()

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