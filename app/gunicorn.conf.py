import multiprocessing

access_log_format = '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
access_logfile = "-"
error_logfile = "-"

bind = "0.0.0.0"
workers = multiprocessing.cpu_count()
worker_class = "gevent"