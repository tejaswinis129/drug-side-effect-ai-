import os
from openai import OpenAI
from app import DrugEnv

# env variables
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

env = DrugEnv()

def inference():
    print(f"[START] task=drug env=drug_env model={MODEL_NAME}", flush=True)

    rewards = []
    steps = 0
    success = False

    try:
        state = env.reset()

        prompt = f"""
        Health: {state['health']}
        Side effect: {state['side_effect']}
        Drug: {state['drug']}

        Choose one:
        Increase Dose / Decrease Dose / Switch Drug / Maintain
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20
        )

        action = response.choices[0].message.content.strip()

        result = env.step(action)

        reward = float(result["reward"])
        rewards.append(reward)
        steps = 1
        success = True

        print(f"[STEP] step=1 action={action} reward={reward:.2f} done=true error=null", flush=True)

    except Exception as e:
        print(f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}", flush=True)
        rewards = [0.0]
        steps = 1
        success = False

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)

    return {"result": result}