import os
import redis
from dotenv import load_dotenv
Redis_Host=os.getenv("UPSTASH_REDIS_HOST")
Redis_Port=os.getenv("UPSTASH_REDIS_PORT")
Redis_Password=os.getenv("UPSTASH_REDIS_PASSWORD")
try:
    redis_client=redis.Redis(
        host=Redis_Host,
        port=int(Redis_Port),
        password=Redis_Password,
        ssl=True,
        decode_responses=True
    )
except Exception as e:
    print(f"redis connection error:{e}")    
    redis_client=None   
download_folder=os.path.join(os.path.expanduser("~"),"Downloads")
os.makedirs(download_folder,exist_ok=True)
def rate_limit(ip,limit=15,duration=60):
    if redis_client:
        if redis_client:
            key = f"ratelimit:{ip}"
            try:
                current = redis_client.incr(key)
                if current == 1:
                    redis_client.expire(key, duration)
                return current > limit
            except Exception as e:
                print(f"Redis error: {e}")
    return False  