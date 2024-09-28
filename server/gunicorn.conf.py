bind = "127.0.0.1:3000"
workers = 2
threads = 2
worker_class = "gthread"
max_requests = 1000
max_requests_jitter = 50

# Добавим следующие строки для улучшения логирования
loglevel = "debug"
accesslog = "/root/ranoberead/logs/gunicorn-access.log"
errorlog = "/root/ranoberead/logs/gunicorn-error.log"
capture_output = True
enable_stdio_inheritance = True

# Добавим проверку загрузки приложения
def on_starting(server):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("gunicorn.error")
    logger.debug("Gunicorn is starting up")

def on_reload(server):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("gunicorn.error")
    logger.debug("Gunicorn is reloading")

def when_ready(server):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("gunicorn.error")
    logger.debug("Gunicorn is ready")
