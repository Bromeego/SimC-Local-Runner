import os


def env_int(name, default, minimum):
    try:
        value = int(os.environ.get(name, str(default)))
    except ValueError:
        return default
    return max(value, minimum)


bind = "0.0.0.0:8080"
workers = 1
threads = env_int("WEB_THREADS", 4, 2)
worker_class = "gthread"
timeout = env_int("SIMC_TIMEOUT_SECONDS", 1800, 30) + 60
graceful_timeout = 30
accesslog = "-"
errorlog = "-"
capture_output = True
