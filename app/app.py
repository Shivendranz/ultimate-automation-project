from flask import Flask, render_template, jsonify
import redis
import psutil
import os

app = Flask(__name__)

r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    try:
        hits = r.incr('visitor_count')
    except:
        hits = "Redis Offline"
    return jsonify({
        "cpu": f"{cpu}%",
        "ram": f"{ram}%",
        "visitors": hits,
        "status": "Healthy"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
