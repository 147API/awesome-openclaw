"""
OpenClaw Cron Job Agent Example

Real-world example: Automated service monitoring with cron scheduling.

This example shows how to:
1. Set up a monitoring agent with OpenClaw cron
2. Handle failures gracefully
3. Send notifications to multiple channels
4. Track failure history
"""

# Step 1: Define your monitoring task
MONITORING_TASK = """
Run service health check for MyAPI:

1. Check https://api.example.com/health
2. If status != 200, send alert to enterprise WeChat
3. Track consecutive failures
4. If failures > 3, escalate to Telegram

Log all results to /var/log/myapi-monitor.log
"""

# Step 2: Create the cron job using OpenClaw API
# This would be done via the cron tool in your agent

CRON_JOB_CONFIG = {
    "name": "MyAPI Health Monitor",
    "schedule": {
        "kind": "cron",
        "expr": "*/5 * * * *",  # Every 5 minutes
        "tz": "UTC"
    },
    "sessionTarget": "isolated",
    "payload": {
        "kind": "agentTurn",
        "message": MONITORING_TASK,
        "timeoutSeconds": 60
    },
    "delivery": {
        "mode": "none"  # Silent unless there's a failure
    }
}

# Step 3: The agent execution script
import requests
import json
from datetime import datetime

def monitor_service():
    """
    Service monitoring logic.
    This runs in an isolated session every 5 minutes.
    """
    SERVICE_URL = "https://api.example.com/health"
    ALERT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    
    try:
        # Perform health check
        response = requests.get(SERVICE_URL, timeout=30)
        
        if response.status_code == 200:
            # Service is healthy
            log_result("healthy", response.elapsed.total_seconds())
            return 0  # Success
        else:
            # Service is unhealthy
            error_msg = f"HTTP {response.status_code}"
            log_result("unhealthy", response.elapsed.total_seconds(), error_msg)
            send_alert(error_msg)
            return 1  # Failure
            
    except requests.Timeout:
        error_msg = "Request timeout (>30s)"
        log_result("timeout", 30, error_msg)
        send_alert(error_msg)
        return 1
        
    except Exception as e:
        error_msg = str(e)
        log_result("error", 0, error_msg)
        send_alert(error_msg)
        return 1

def log_result(status: str, latency: float, error: str = None):
    """Log monitoring result."""
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "status": status,
        "latency_seconds": latency,
        "error": error
    }
    
    with open("/var/log/myapi-monitor.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def send_alert(error: str):
    """Send alert to enterprise WeChat."""
    ALERT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    
    message = f"⚠️ MyAPI 监控告警\n\n错误: {error}\n时间: {datetime.utcnow().isoformat()}"
    
    try:
        requests.post(
            ALERT_WEBHOOK,
            json={"msgtype": "text", "text": {"content": message}},
            timeout=10
        )
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Step 4: Usage in OpenClaw
"""
To use this in OpenClaw:

1. Create the cron job:
   cron(action="add", job=CRON_JOB_CONFIG)

2. The agent will automatically run every 5 minutes

3. Check job status:
   cron(action="list")

4. View run history:
   cron(action="runs", jobId="your-job-id")

5. Manually trigger:
   cron(action="run", jobId="your-job-id")
"""

# Step 5: Advanced features

# A. Failure escalation
FAILURE_HISTORY_FILE = "/tmp/myapi-failures.json"

def track_failures():
    """Track consecutive failures for escalation."""
    try:
        with open(FAILURE_HISTORY_FILE, "r") as f:
            history = json.load(f)
    except:
        history = {"count": 0, "last_failure": None}
    
    history["count"] += 1
    history["last_failure"] = datetime.utcnow().isoformat()
    
    with open(FAILURE_HISTORY_FILE, "w") as f:
        json.dump(history, f)
    
    # Escalate if too many failures
    if history["count"] > 3:
        escalate_alert()
    
    return history["count"]

def escalate_alert():
    """Escalate to Telegram after multiple failures."""
    # Use OpenClaw message tool to send to Telegram
    pass

# B. Recovery detection
def reset_failures():
    """Reset failure count when service recovers."""
    with open(FAILURE_HISTORY_FILE, "w") as f:
        json.dump({"count": 0, "last_failure": None}, f)

# C. Performance tracking
def track_performance(latency: float):
    """Track service performance over time."""
    # Store in time-series database or log file
    pass

if __name__ == "__main__":
    exit(monitor_service())
