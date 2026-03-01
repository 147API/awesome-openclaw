# OpenClaw Agent Best Practices

> Lessons learned from running production AI agents

## 🎯 Core Principles

### 1. Keep Agents Focused
**DO:** One agent, one responsibility
```python
# ✅ Good: Focused monitoring agent
monitor_agent = Agent(
    task="Check service health every 10 minutes",
    tools=["exec", "message"]
)

# ❌ Bad: Kitchen sink agent
super_agent = Agent(
    task="Monitor, analyze, report, fix, deploy, and make coffee",
    tools=["everything"]
)
```

### 2. Handle Failures Gracefully
**DO:** Always have fallback strategies
```python
# ✅ Good: Graceful degradation
try:
    result = expensive_api_call()
except TimeoutError:
    result = cached_fallback()
    notify_admin("API timeout, using cache")

# ❌ Bad: Silent failures
try:
    result = expensive_api_call()
except:
    pass  # Hope for the best
```

### 3. Log Everything
**DO:** Make debugging easy
```python
# ✅ Good: Structured logging
log.info("Task started", task_id=123, user="wild1024")
log.error("API failed", error=str(e), retry_count=3)

# ❌ Bad: Print debugging
print("something happened")
```

## 🚫 Common Pitfalls

### 1. Infinite Loops
**Problem:** Agent keeps calling itself
```python
# ❌ Dangerous
def agent_task():
    if condition:
        sessions_send(message="Try again", target="self")
```

**Solution:** Add loop detection
```python
# ✅ Safe
MAX_RETRIES = 3
retry_count = 0

def agent_task():
    if condition and retry_count < MAX_RETRIES:
        retry_count += 1
        sessions_send(message=f"Retry {retry_count}/{MAX_RETRIES}")
```

### 2. Token Waste
**Problem:** Reading huge files unnecessarily
```python
# ❌ Wasteful
content = read_file("10GB_log.txt")  # Reads everything
```

**Solution:** Use limits and offsets
```python
# ✅ Efficient
content = read_file("10GB_log.txt", limit=100, offset=0)
```

### 3. Hardcoded Secrets
**Problem:** API keys in code
```python
# ❌ Security risk
API_KEY = "sk-1234567890abcdef"
```

**Solution:** Use environment variables
```python
# ✅ Secure
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set")
```

## ⚡ Performance Tips

### 1. Batch Operations
```python
# ❌ Slow: One at a time
for item in items:
    process(item)

# ✅ Fast: Batch processing
process_batch(items)
```

### 2. Cache Expensive Calls
```python
# ✅ Smart caching
@cache(ttl=3600)
def expensive_api_call():
    return requests.get("https://slow-api.com/data")
```

### 3. Parallel Execution
```python
# ✅ Concurrent tasks
with ThreadPoolExecutor() as executor:
    results = executor.map(process, items)
```

## 🔒 Security Guidelines

### 1. Validate All Inputs
```python
# ✅ Input validation
def process_url(url: str):
    if not url.startswith(("http://", "https://")):
        raise ValueError("Invalid URL")
    # Process safely
```

### 2. Limit Resource Usage
```python
# ✅ Resource limits
exec(command, timeout=30)  # Prevent hanging
read_file(path, limit=1000)  # Prevent memory issues
```

### 3. Sanitize Outputs
```python
# ✅ Remove sensitive data
def sanitize_log(text: str) -> str:
    text = re.sub(r'sk-[a-zA-Z0-9]+', 'sk-***', text)
    text = re.sub(r'\d{16}', '****', text)  # Credit cards
    return text
```

## 📊 Monitoring

### 1. Track Key Metrics
- Task completion rate
- Average execution time
- Error rate
- Token usage
- Cost per task

### 2. Set Up Alerts
```python
# ✅ Proactive monitoring
if error_rate > 0.1:  # 10% errors
    send_alert("High error rate detected")

if avg_latency > 30:  # 30 seconds
    send_alert("Performance degradation")
```

### 3. Regular Health Checks
```python
# ✅ Automated health checks
@cron("*/5 * * * *")  # Every 5 minutes
def health_check():
    if not service_is_healthy():
        restart_service()
        notify_admin()
```

## 🎓 Real-World Examples

### Example 1: Monitoring Agent
```python
# Production-ready monitoring agent
def monitor_service():
    try:
        response = requests.get(SERVICE_URL, timeout=10)
        if response.status_code != 200:
            send_alert(f"Service down: {response.status_code}")
            log.error("Health check failed", status=response.status_code)
        else:
            log.info("Health check passed")
    except Exception as e:
        send_alert(f"Service unreachable: {e}")
        log.error("Health check error", error=str(e))
```

### Example 2: Content Generation Agent
```python
# Efficient content generation
def generate_weekly_report():
    # Use cache to avoid regenerating
    cache_key = f"report_{datetime.now().strftime('%Y-W%W')}"
    
    if cached := get_cache(cache_key):
        return cached
    
    # Generate new report
    report = create_report()
    set_cache(cache_key, report, ttl=86400)  # 24 hours
    
    return report
```

---

## 📚 Further Reading

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Agent Design Patterns](./patterns.md)
- [Troubleshooting Guide](./troubleshooting.md)

---

**Questions?** [Open an issue](https://github.com/147API/foropenclaw/issues) or [join discussions](https://github.com/147API/foropenclaw/discussions)
