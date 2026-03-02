# 🚀 Quick Start Guide

Get started with OpenClaw agent development in 5 minutes.

## 📋 Prerequisites

- OpenClaw account and API access
- Basic Python knowledge
- A problem to solve with automation

## 🎯 Your First Agent in 3 Steps

### Step 1: Choose a Template

Pick a template that matches your use case:

```bash
cd foropenclaw/templates/

# For monitoring
monitoring_agent.py

# For scheduled tasks
../examples/cron_monitoring.py

# For content generation
../examples/newsletter_agent.py
```

### Step 2: Customize It

Edit the template with your specific needs:

```python
# Example: Customize monitoring agent
from templates.monitoring_agent import MonitoringAgent

agent = MonitoringAgent(
    service_name="My API",
    service_url="https://api.myservice.com/health",
    check_interval=300,  # 5 minutes
    alert_webhook="https://your-webhook-url"
)

# Run it
agent.run_check()
```

### Step 3: Deploy with Cron

Schedule it to run automatically:

```python
# In your OpenClaw session
cron(action="add", job={
    "name": "My API Monitor",
    "schedule": {
        "kind": "cron",
        "expr": "*/5 * * * *",  # Every 5 minutes
        "tz": "UTC"
    },
    "sessionTarget": "isolated",
    "payload": {
        "kind": "agentTurn",
        "message": "Run monitoring check for My API",
        "timeoutSeconds": 60
    }
})
```

**Done!** Your agent is now running automatically. ✅

---

## 🎓 Common Use Cases

### Use Case 1: Service Monitoring

**Goal:** Get alerted when your service goes down

**Template:** `templates/monitoring_agent.py`

**Time to deploy:** 10 minutes

```python
agent = MonitoringAgent(
    service_name="Production API",
    service_url="https://api.example.com/health",
    alert_webhook="https://your-webhook"
)

# Test it first
result = agent.run_check()
print(result)

# Deploy with cron (every 5 minutes)
```

---

### Use Case 2: Daily Reports

**Goal:** Automated daily summary reports

**Template:** `examples/newsletter_agent.py`

**Time to deploy:** 20 minutes

```python
agent = NewsletterAgent(
    sources=["github://python/daily", "hn://"]
)

# Test generation
report = agent.run(channels=["github"])

# Deploy with cron (daily at 9 AM)
schedule = {"kind": "cron", "expr": "0 9 * * *"}
```

---

### Use Case 3: Data Pipeline

**Goal:** Process data from multiple sources

**Pattern:** Pipeline (see `docs/patterns.md`)

**Time to deploy:** 30 minutes

```python
from docs.patterns import Pipeline

pipeline = Pipeline()
pipeline.add_stage(fetch_from_api)
pipeline.add_stage(transform_data)
pipeline.add_stage(validate_data)
pipeline.add_stage(save_to_database)

# Run pipeline
result = pipeline.run(initial_data)
```

---

## 🧪 Testing Your Agent

Before deploying, test it:

```python
from tools.testing import AgentTester

tester = AgentTester()

@tester.test("Service responds")
def test_service():
    result = agent.check_health()
    assert result["status"] == "healthy"

@tester.test("Alert sends successfully")
def test_alert():
    agent.send_alert({"status": "test"})
    # Verify alert was received

# Run tests
results = tester.run_all()
```

---

## 🐛 Debugging

If something goes wrong:

1. **Check logs:**
   ```python
   exec(command="tail -100 /var/log/openclaw.log")
   ```

2. **Test manually:**
   ```python
   # Run your agent function directly
   result = agent.run_check()
   print(result)
   ```

3. **Check cron status:**
   ```python
   cron(action="list")
   cron(action="runs", jobId="your-job-id")
   ```

See [Troubleshooting Guide](docs/troubleshooting.md) for more help.

---

## 📚 Next Steps

### Learn More

- 📖 [Best Practices](docs/best-practices.md) - Production tips
- 🎨 [Design Patterns](docs/patterns.md) - Common patterns
- 🐛 [Troubleshooting](docs/troubleshooting.md) - Fix issues

### Explore Examples

- 📊 [Monitoring Agent](examples/cron_monitoring.py)
- 📰 [Newsletter Agent](examples/newsletter_agent.py)
- 🧪 [Testing Tools](tools/testing.py)

### Get Help

- 💬 [GitHub Discussions](https://github.com/147API/awesome-openclaw/discussions)
- 🐛 [Report Issues](https://github.com/147API/awesome-openclaw/issues)
- 📧 Email: ai_147api@163.com

---

## 💡 Pro Tips

### Tip 1: Start Small
Don't build a complex agent on day one. Start with a simple monitoring task and iterate.

### Tip 2: Test Locally First
Run your agent manually before scheduling it with cron.

### Tip 3: Monitor Your Agents
Set up alerts for your monitoring agents (yes, monitor the monitors!).

### Tip 4: Use Templates
Don't reinvent the wheel. Start with our templates and customize.

### Tip 5: Read the Patterns
Understanding design patterns will save you hours of debugging.

---

## 🎯 Success Checklist

Before deploying to production:

- [ ] Agent tested manually
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Alerts set up
- [ ] Timeout configured
- [ ] Cron schedule verified
- [ ] Documentation written
- [ ] Monitoring in place

---

## 🚀 Ready to Build?

1. Clone this repo
2. Pick a template
3. Customize it
4. Test it
5. Deploy it
6. Monitor it

**Questions?** [Ask in Discussions](https://github.com/147API/awesome-openclaw/discussions)

---

<div align="center">

**Happy building! 🦞**

[⬅️ Back to README](../README.md)

</div>
