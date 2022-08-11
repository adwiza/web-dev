import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)


print("set login user")
print(r.set('login', 'user'))
print("get login")
print(r.get('login').decode('utf-8'))
