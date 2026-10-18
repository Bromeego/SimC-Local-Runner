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


def _stop_orphan_simulations():
    # Import lazily so configuration loading does not start the web app twice.
    import app as simc_app

    simc_app.stop_active_run_containers()


def worker_abort(_worker):
    _stop_orphan_simulations()


def post_worker_init(_worker):
    """Stop child simulations if this worker is asked to shut down."""
    import signal

    previous_handlers = {
        signal.SIGTERM: signal.getsignal(signal.SIGTERM),
        signal.SIGINT: signal.getsignal(signal.SIGINT),
    }

    def handle_shutdown(signum, frame):
        _stop_orphan_simulations()
        previous = previous_handlers.get(signum)
        if callable(previous):
            previous(signum, frame)
        # A simulation can start while the worker is marking itself stopped.
        _stop_orphan_simulations()

    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)
