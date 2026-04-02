import os
from openai import OpenAI
from app import DrugEnv

# ✅ ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN")

# ✅ CLIENT
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# ✅ ENV
env = DrugEnv()

# ✅ LOG FUNCTIONS
def log_start(task, env_name, model):
    print(f"[START] task={task} env={env_name} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True
    )

def log_end(success, steps, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True
    )

# ✅ MAIN FUNCTION
def inference():
    TASK = "drug-optimization"
    ENV_NAME = "drug_env"

    rewards = []
    steps_taken = 0
    success = False

    log_start(TASK, ENV_NAME, MODEL_NAME)

    try:
        state = env.reset()

        for step in range(1, 4):   # small loop (safe for runtime)
            prompt = f"""
            Patient state:
            Health: {state['health']}
            Side effects: {state['side_effect']}
            Drug: {state['drug']}

            Choose one action:
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
            done = True  # single-step logic

            rewards.append(reward)
            steps_taken = step

            log_step(step, action, reward, done, None)

            if done:
                break

        success = True

    except Exception as e:
        log_step(1, "error", 0.0, True, str(e))
        rewards = [0.0]
        steps_taken = 1
        success = False

    log_end(success, steps_taken, rewards)

    return {"result": result}