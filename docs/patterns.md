# OpenClaw Agent Design Patterns

> Proven patterns for building robust AI agents

## 🎯 Pattern Categories

1. **Execution Patterns** - How agents run tasks
2. **Communication Patterns** - How agents interact
3. **Error Handling Patterns** - How agents handle failures
4. **Data Patterns** - How agents manage state

---

## 🔄 Execution Patterns

### 1. Single-Shot Pattern

**Use when:** One-time tasks with clear completion

```python
# Example: Send daily report
def daily_report():
    data = collect_data()
    report = generate_report(data)
    send_report(report)
    return "Report sent"

# Cron: Once per day
schedule = {"kind": "cron", "expr": "0 9 * * *"}
```

**Pros:**
- Simple and predictable
- Easy to debug
- Clear success/failure

**Cons:**
- No retry logic
- No state persistence

---

### 2. Retry Pattern

**Use when:** Tasks that may fail temporarily

```python
def task_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            result = unreliable_operation()
            return result
        except TemporaryError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
            log(f"Retry {attempt + 1}/{max_retries}")
```

**Pros:**
- Handles transient failures
- Exponential backoff prevents hammering
- Configurable retry count

**Cons:**
- Can delay completion
- May mask persistent issues

---

### 3. Circuit Breaker Pattern

**Use when:** Protecting against cascading failures

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError("Circuit breaker is open")
        
        try:
            result = func()
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            
            raise

# Usage
breaker = CircuitBreaker()

def monitored_task():
    return breaker.call(lambda: api.call())
```

**Pros:**
- Prevents cascading failures
- Automatic recovery
- Protects downstream services

**Cons:**
- More complex
- Requires state management

---

### 4. Pipeline Pattern

**Use when:** Multi-stage processing

```python
class Pipeline:
    def __init__(self):
        self.stages = []
    
    def add_stage(self, func):
        self.stages.append(func)
        return self
    
    def run(self, input_data):
        data = input_data
        for i, stage in enumerate(self.stages):
            try:
                data = stage(data)
                log(f"Stage {i+1} complete")
            except Exception as e:
                log(f"Stage {i+1} failed: {e}")
                raise
        return data

# Usage
pipeline = Pipeline()
pipeline.add_stage(fetch_data)
pipeline.add_stage(transform_data)
pipeline.add_stage(validate_data)
pipeline.add_stage(save_data)

result = pipeline.run(initial_input)
```

**Pros:**
- Clear separation of concerns
- Easy to add/remove stages
- Testable stages

**Cons:**
- Linear flow only
- All stages must complete

---

## 💬 Communication Patterns

### 1. Fire and Forget

**Use when:** No response needed

```python
# Send notification without waiting
def notify_user(message):
    message_tool(action="send", message=message, target="user")
    # Don't wait for response
```

**Pros:**
- Fast
- Non-blocking
- Simple

**Cons:**
- No delivery confirmation
- Can't handle failures

---

### 2. Request-Response

**Use when:** Need confirmation or result

```python
def request_approval(task):
    # Send request
    sessions_send(
        message=f"Approve task: {task}?",
        sessionKey="main"
    )
    
    # Wait for response (in next execution)
    # Store state to track pending approvals
```

**Pros:**
- Confirmation of delivery
- Can get response data
- Synchronous flow

**Cons:**
- Blocking
- Requires state management

---

### 3. Pub-Sub Pattern

**Use when:** Multiple consumers need same data

```python
class EventBus:
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type, handler):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    def publish(self, event_type, data):
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    log(f"Handler failed: {e}")

# Usage
bus = EventBus()

bus.subscribe("service_down", send_alert)
bus.subscribe("service_down", log_incident)
bus.subscribe("service_down", create_ticket)

bus.publish("service_down", {"service": "api", "time": now()})
```

**Pros:**
- Decoupled components
- Multiple consumers
- Easy to extend

**Cons:**
- No delivery guarantee
- Order not guaranteed

---

## 🛡️ Error Handling Patterns

### 1. Graceful Degradation

**Use when:** Service can operate with reduced functionality

```python
def get_recommendations():
    try:
        # Try AI-powered recommendations
        return ai_recommendations()
    except AIServiceDown:
        # Fall back to rule-based
        log("AI down, using fallback")
        return rule_based_recommendations()
    except Exception:
        # Last resort: popular items
        return popular_items()
```

**Pros:**
- Service stays available
- User experience maintained
- Automatic recovery

**Cons:**
- Reduced quality
- May hide issues

---

### 2. Dead Letter Queue

**Use when:** Failed tasks need manual review

```python
def process_with_dlq(task):
    try:
        result = process_task(task)
        return result
    except Exception as e:
        # Move to dead letter queue
        dead_letter_queue.add({
            "task": task,
            "error": str(e),
            "timestamp": now(),
            "retry_count": task.get("retry_count", 0)
        })
        
        # Alert if too many failures
        if dead_letter_queue.size() > 10:
            send_alert("DLQ threshold exceeded")
```

**Pros:**
- No data loss
- Manual intervention possible
- Failure tracking

**Cons:**
- Requires monitoring
- Manual cleanup needed

---

### 3. Bulkhead Pattern

**Use when:** Isolating failures

```python
class ResourcePool:
    def __init__(self, max_concurrent=5):
        self.semaphore = threading.Semaphore(max_concurrent)
    
    def execute(self, func):
        if not self.semaphore.acquire(blocking=False):
            raise ResourceExhaustedError("Pool full")
        
        try:
            return func()
        finally:
            self.semaphore.release()

# Separate pools for different services
api_pool = ResourcePool(max_concurrent=10)
db_pool = ResourcePool(max_concurrent=5)

# API failures won't exhaust DB pool
api_pool.execute(lambda: api.call())
db_pool.execute(lambda: db.query())
```

**Pros:**
- Failure isolation
- Resource protection
- Predictable behavior

**Cons:**
- Resource limits
- More complex

---

## 💾 Data Patterns

### 1. State Machine

**Use when:** Complex workflows with states

```python
class WorkflowState:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Workflow:
    def __init__(self):
        self.state = WorkflowState.PENDING
        self.data = {}
    
    def transition(self, new_state):
        valid_transitions = {
            WorkflowState.PENDING: [WorkflowState.PROCESSING],
            WorkflowState.PROCESSING: [WorkflowState.COMPLETED, WorkflowState.FAILED],
            WorkflowState.FAILED: [WorkflowState.PENDING]  # Retry
        }
        
        if new_state not in valid_transitions.get(self.state, []):
            raise InvalidTransitionError(f"Cannot go from {self.state} to {new_state}")
        
        self.state = new_state
        self.save()
```

**Pros:**
- Clear state transitions
- Prevents invalid states
- Easy to visualize

**Cons:**
- Can be complex
- Requires persistence

---

### 2. Event Sourcing

**Use when:** Need complete audit trail

```python
class EventStore:
    def __init__(self):
        self.events = []
    
    def append(self, event):
        event["timestamp"] = now()
        event["id"] = generate_id()
        self.events.append(event)
        self.save()
    
    def replay(self):
        state = {}
        for event in self.events:
            state = apply_event(state, event)
        return state

# Usage
store = EventStore()
store.append({"type": "task_started", "task_id": 123})
store.append({"type": "task_completed", "task_id": 123, "result": "success"})

# Rebuild state from events
current_state = store.replay()
```

**Pros:**
- Complete history
- Time travel debugging
- Audit trail

**Cons:**
- Storage overhead
- Replay can be slow

---

## 🎓 Real-World Examples

### Example: Monitoring Agent with Multiple Patterns

```python
class ProductionMonitor:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker()
        self.event_bus = EventBus()
        self.retry_policy = RetryPolicy(max_retries=3)
    
    def check_service(self, service_url):
        # Circuit breaker pattern
        try:
            result = self.circuit_breaker.call(
                lambda: self._health_check(service_url)
            )
        except CircuitOpenError:
            self.event_bus.publish("circuit_open", {"service": service_url})
            return {"status": "circuit_open"}
        
        # Publish events
        if result["status"] != "healthy":
            self.event_bus.publish("service_unhealthy", result)
        
        return result
    
    def _health_check(self, url):
        # Retry pattern
        return self.retry_policy.execute(
            lambda: requests.get(url, timeout=10)
        )
```

---

## 📚 Pattern Selection Guide

| Scenario | Recommended Pattern |
|----------|-------------------|
| One-time task | Single-Shot |
| Unreliable API | Retry + Circuit Breaker |
| Multi-step process | Pipeline |
| Multiple consumers | Pub-Sub |
| Complex workflow | State Machine |
| Audit requirements | Event Sourcing |
| Failure isolation | Bulkhead |
| Graceful failures | Graceful Degradation |

---

**Questions?** [Open a discussion](https://github.com/147API/awesome-openclaw/discussions)
