
import requests
from .config import SILICONFLOW_API_KEY, SILICONFLOW_URL, MODEL_ID

chat_history = [{"role": "system", "content": ""}]

def ask_model(prompt):
    chat_history.append({"role": "user", "content": prompt})
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}"
    }
    data = {
        "model": MODEL_ID,
        "messages": chat_history,
        "temperature": 0.7,
        "max_tokens": 512
    }
    response = requests.post(SILICONFLOW_URL, headers=headers, json=data)
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": reply})
        return reply.strip()
    else:
        print("模型调用失败：", response.status_code)
        print(response.text)
        return "出错了"
