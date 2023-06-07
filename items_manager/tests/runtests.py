import subprocess
import redis
import coverage


result = subprocess.run(['coverage','run', '-m', 'pytest', 'test_items.py'])
subprocess.run(['coverage', 'html'])
redis.Redis().flushdb()