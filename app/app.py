from flask import Flask, render_template, jsonify
from prometheus_flask_exporter import PrometheusMetrics  # <--- Monitoring library
import redis
import psutil
import os

app = Flask(__name__)

# Prometheus Metrics ko initialize kar rahe hain
# Ye apne aap '/metrics' endpoint bana dega
metrics = PrometheusMetrics(app)

# static information metrics ke liye (Optional)
metrics.info('app_info', 'Application info', version='1.0.0')

# Redis setup
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
    # Port 5000 par run ho raha hai
    app.run(host='0.0.0.0', port=5000)
