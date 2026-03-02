# OpenClaw Agent Troubleshooting Guide

> Common issues and how to fix them

## 🔍 Debugging Basics

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Session Status
```python
# List all sessions
sessions_list()

# Check specific session
sessions_history(sessionKey="your-session-key", limit=50)
```

### Monitor Token Usage
```python
# Check current session usage
session_status()
```

---

## 🐛 Common Issues

### Issue 1: Agent Not Responding

**Symptoms:**
- Cron job doesn't run
- No output from agent
- Silent failures

**Diagnosis:**
```python
# Check if job is enabled
cron(action="list")

# Check run history
cron(action="runs", jobId="your-job-id")

# Check for errors in logs
exec(command="tail -100 /var/log/openclaw.log")
```

**Solutions:**
1. **Job disabled?** Enable it:
   ```python
   cron(action="update", jobId="xxx", patch={"enabled": True})
   ```

2. **Wrong schedule?** Check cron expression:
   ```python
   # Test at https://crontab.guru
   "*/5 * * * *"  # Every 5 minutes
   ```

3. **Timeout?** Increase timeout:
   ```python
   payload = {
       "kind": "agentTurn",
       "message": "...",
       "timeoutSeconds": 600  # 10 minutes
   }
   ```

---

### Issue 2: High Token Usage

**Symptoms:**
- Unexpected costs
- Slow responses
- Token limit errors

**Diagnosis:**
```python
# Check token usage
session_status()

# Find expensive operations
sessions_history(sessionKey="xxx", limit=100)
```

**Solutions:**
1. **Reading large files?** Use limits:
   ```python
   # ❌ Bad
   content = read("huge_file.txt")
   
   # ✅ Good
   content = read("huge_file.txt", limit=100)
   ```

2. **Repeated API calls?** Add caching:
   ```python
   import functools
   
   @functools.lru_cache(maxsize=128)
   def expensive_call():
       return api.fetch_data()
   ```

3. **Verbose outputs?** Summarize:
   ```python
   # ❌ Bad: Return entire log
   return log_content
   
   # ✅ Good: Return summary
   return f"Found {error_count} errors in last 100 lines"
   ```

---

### Issue 3: Tool Execution Fails

**Symptoms:**
- `exec` command hangs
- Permission denied errors
- Timeout errors

**Diagnosis:**
```python
# Test command manually
exec(command="your-command", timeout=10)

# Check permissions
exec(command="ls -la /path/to/file")

# Check if process is running
exec(command="ps aux | grep your-process")
```

**Solutions:**
1. **Command hangs?** Add timeout:
   ```python
   exec(command="long-running-cmd", timeout=30)
   ```

2. **Permission denied?** Check file permissions:
   ```python
   exec(command="chmod +x /path/to/script.sh")
   ```

3. **Interactive command?** Use non-interactive mode:
   ```python
   # ❌ Bad: Interactive
   exec(command="vim file.txt")
   
   # ✅ Good: Non-interactive
   exec(command="sed -i 's/old/new/g' file.txt")
   ```

---

### Issue 4: Memory Issues

**Symptoms:**
- Agent crashes
- Out of memory errors
- Slow performance

**Diagnosis:**
```python
# Check memory usage
exec(command="free -h")

# Check process memory
exec(command="ps aux --sort=-%mem | head -10")
```

**Solutions:**
1. **Processing large data?** Stream it:
   ```python
   # ❌ Bad: Load everything
   with open("huge.txt") as f:
       data = f.read()
   
   # ✅ Good: Process line by line
   with open("huge.txt") as f:
       for line in f:
           process(line)
   ```

2. **Accumulating data?** Clear periodically:
   ```python
   results = []
   for item in items:
       results.append(process(item))
       if len(results) > 1000:
           save_batch(results)
           results = []  # Clear
   ```

---

### Issue 5: Rate Limiting

**Symptoms:**
- 429 Too Many Requests
- API throttling errors
- Slow responses

**Diagnosis:**
```python
# Check API rate limits
# Look for 429 errors in logs
```

**Solutions:**
1. **Add delays between requests:**
   ```python
   import time
   
   for item in items:
       process(item)
       time.sleep(1)  # 1 second delay
   ```

2. **Implement exponential backoff:**
   ```python
   import time
   
   def retry_with_backoff(func, max_retries=3):
       for i in range(max_retries):
           try:
               return func()
           except RateLimitError:
               wait = 2 ** i  # 1s, 2s, 4s
               time.sleep(wait)
       raise Exception("Max retries exceeded")
   ```

3. **Batch requests:**
   ```python
   # ❌ Bad: One by one
   for item in items:
       api.process(item)
   
   # ✅ Good: Batch
   api.process_batch(items)
   ```

---

### Issue 6: Notification Failures

**Symptoms:**
- Alerts not received
- Webhook errors
- Silent failures

**Diagnosis:**
```python
# Test webhook manually
import requests

response = requests.post(
    "https://your-webhook-url",
    json={"msgtype": "text", "text": {"content": "test"}},
    timeout=10
)
print(response.status_code, response.text)
```

**Solutions:**
1. **Webhook URL wrong?** Verify:
   ```python
   # Check webhook configuration
   print(WEBHOOK_URL)
   ```

2. **Network issues?** Add retry:
   ```python
   def send_with_retry(webhook, message, retries=3):
       for i in range(retries):
           try:
               response = requests.post(webhook, json=message, timeout=10)
               if response.status_code == 200:
                   return True
           except:
               time.sleep(2 ** i)
       return False
   ```

3. **Message format wrong?** Check docs:
   ```python
   # Enterprise WeChat format
   {
       "msgtype": "text",
       "text": {"content": "your message"}
   }
   
   # Telegram format
   {
       "chat_id": "your-chat-id",
       "text": "your message"
   }
   ```

---

## 🔧 Debugging Tools

### 1. Interactive Testing
```python
# Test your agent logic in Python REPL
python3
>>> from your_agent import monitor_service
>>> result = monitor_service()
>>> print(result)
```

### 2. Dry Run Mode
```python
# Add dry-run flag to test without side effects
def monitor_service(dry_run=False):
    result = check_health()
    
    if result["status"] != "healthy":
        if dry_run:
            print(f"Would send alert: {result}")
        else:
            send_alert(result)
```

### 3. Logging Everything
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def monitor_service():
    logger.info("Starting health check")
    try:
        result = check_health()
        logger.info(f"Health check result: {result}")
        return result
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        raise
```

---

## 📊 Performance Profiling

### Find Slow Operations
```python
import time

def profile(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper

@profile
def slow_operation():
    # Your code here
    pass
```

### Memory Profiling
```python
import tracemalloc

tracemalloc.start()

# Your code here

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()
```

---

## 🆘 Getting Help

1. **Check documentation:** https://docs.openclaw.ai
2. **Search issues:** https://github.com/openclaw/openclaw/issues
3. **Ask community:** https://discord.gg/openclaw
4. **Open issue:** Include logs, config, and minimal reproduction

---

## 📝 Debugging Checklist

Before asking for help, check:

- [ ] Logs reviewed (`/var/log/openclaw.log`)
- [ ] Session status checked (`session_status()`)
- [ ] Cron job enabled (`cron(action="list")`)
- [ ] Timeouts configured properly
- [ ] Permissions correct (`ls -la`)
- [ ] Network connectivity (`ping`, `curl`)
- [ ] Token usage reasonable (`session_status()`)
- [ ] Error messages captured
- [ ] Minimal reproduction created

---

**Still stuck?** [Open an issue](https://github.com/147API/awesome-openclaw/issues) with:
- What you're trying to do
- What you expected
- What actually happened
- Relevant logs/code
