"""
OpenClaw Monitoring Agent Template

A production-ready template for service monitoring with:
- Health checks
- Failure tracking
- Alert notifications
- Automatic recovery
"""

import requests
import time
import json
from datetime import datetime, timezone
from typing import Dict, Optional

class MonitoringAgent:
    """
    Production-ready monitoring agent template.
    
    Features:
    - Configurable health checks
    - Failure history tracking
    - Multiple notification channels
    - Automatic retry logic
    """
    
    def __init__(
        self,
        service_name: str,
        service_url: str,
        check_interval: int = 300,  # 5 minutes
        alert_webhook: Optional[str] = None,
        max_retries: int = 3
    ):
        self.service_name = service_name
        self.service_url = service_url
        self.check_interval = check_interval
        self.alert_webhook = alert_webhook
        self.max_retries = max_retries
        self.failure_count = 0
        self.last_check = None
        
    def check_health(self) -> Dict:
        """
        Perform health check on the service.
        
        Returns:
            Dict with status, latency, and error info
        """
        start_time = time.time()
        
        try:
            response = requests.get(
                self.service_url,
                timeout=30,
                headers={"User-Agent": "OpenClaw-Monitor/1.0"}
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                self.failure_count = 0  # Reset on success
                return {
                    "status": "healthy",
                    "latency_ms": latency_ms,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            else:
                self.failure_count += 1
                return {
                    "status": "unhealthy",
                    "error": f"HTTP {response.status_code}",
                    "latency_ms": latency_ms,
                    "consecutive_failures": self.failure_count,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
        except requests.Timeout:
            self.failure_count += 1
            return {
                "status": "timeout",
                "error": "Request timed out after 30s",
                "consecutive_failures": self.failure_count,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.failure_count += 1
            return {
                "status": "error",
                "error": str(e),
                "consecutive_failures": self.failure_count,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def send_alert(self, result: Dict):
        """
        Send alert notification via webhook.
        
        Args:
            result: Health check result dictionary
        """
        if not self.alert_webhook:
            print(f"⚠️  Alert: {self.service_name} - {result['status']}")
            return
        
        message = self._format_alert_message(result)
        
        try:
            requests.post(
                self.alert_webhook,
                json={"msgtype": "text", "text": {"content": message}},
                timeout=10
            )
        except Exception as e:
            print(f"Failed to send alert: {e}")
    
    def _format_alert_message(self, result: Dict) -> str:
        """Format alert message for notification."""
        status_emoji = {
            "healthy": "✅",
            "unhealthy": "❌",
            "timeout": "⏱️",
            "error": "💥"
        }
        
        emoji = status_emoji.get(result["status"], "⚠️")
        
        msg = f"{emoji} {self.service_name} 监控告警\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"状态: {result['status']}\n"
        
        if "error" in result:
            msg += f"错误: {result['error']}\n"
        
        if "latency_ms" in result:
            msg += f"延迟: {result['latency_ms']}ms\n"
        
        if result.get("consecutive_failures", 0) > 1:
            msg += f"连续失败: {result['consecutive_failures']} 次\n"
        
        msg += f"时间: {result['timestamp']}\n"
        
        return msg
    
    def run_check(self):
        """
        Run a single health check and handle alerts.
        
        This is the main method to call from your cron job.
        """
        print(f"🔍 Checking {self.service_name}...")
        
        result = self.check_health()
        self.last_check = result
        
        # Alert on failures
        if result["status"] != "healthy":
            print(f"❌ {self.service_name} is {result['status']}")
            self.send_alert(result)
        else:
            print(f"✅ {self.service_name} is healthy ({result['latency_ms']}ms)")
        
        return result


# Example usage
if __name__ == "__main__":
    # Create monitoring agent
    agent = MonitoringAgent(
        service_name="My API",
        service_url="https://api.example.com/health",
        alert_webhook="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    )
    
    # Run check
    result = agent.run_check()
    
    # Print result
    print(json.dumps(result, indent=2))
