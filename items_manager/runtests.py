import subprocess
import redis

result = subprocess.run(['pytest', 'test_items.py'])
redis.Redis().flushdb()