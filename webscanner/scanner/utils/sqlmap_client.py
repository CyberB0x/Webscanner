import requests
import time

API_URL = "http://127.0.0.1:8775"

def start_sqlmap_scan(target_url):
    try:
        # 1. Создание задания
        taskid = requests.get(f"{API_URL}/task/new").json().get("taskid")
        if not taskid:
            return {"error": "Не удалось создать задание"}

        # 2. Настройка опций
        options = {
            "level": 5,
            "risk": 3,
            "batch": True,
            "smart": True,
            "timeout": 15,
            "retries": 2,
            "user-agent": "Mozilla/5.0",
            "threads": 3,
        }
        requests.post(f"{API_URL}/option/{taskid}/set", json=options)

        # 3. Запуск сканирования
        start = requests.post(f"{API_URL}/scan/{taskid}/start", json={"url": target_url}).json()
        if not start.get("success"):
            return {"error": "Не удалось запустить сканирование"}

        # 4. Ожидание завершения
        while True:
            status = requests.get(f"{API_URL}/scan/{taskid}/status").json()
            if status.get("status") == "terminated":
                break
            time.sleep(3)

        data = requests.get(f"{API_URL}/scan/{taskid}/data").json()
        log = requests.get(f"{API_URL}/scan/{taskid}/log").json()

        # Только теперь удаляем
        requests.get(f"{API_URL}/task/{taskid}/delete")

        return {
            "data": data.get("data", []),
            "log": log.get("log", [])
        }

    except Exception as e:
        return {"error": str(e)}
