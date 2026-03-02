# 🤝 Contributing to For OpenClaw

Thanks for your interest in contributing! This project is built by the community, for the community.

## 🎯 How You Can Help

### 1. Share Your Agent Templates
Have a production agent that works well? Share it!

**What we're looking for:**
- ✅ Production-tested code
- ✅ Clear documentation
- ✅ Real-world use case
- ✅ Error handling
- ✅ Example usage

**What to include:**
```python
"""
Agent Name: Brief description

Use case: What problem does it solve?
Tested in: Production/Staging
Dependencies: List any requirements

Example:
    agent = YourAgent(config)
    result = agent.run()
"""
```

### 2. Report Issues
Found a bug? Template not working? Let us know!

**Good issue includes:**
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/logs

[Open an issue →](https://github.com/147API/awesome-openclaw/issues/new)

### 3. Improve Documentation
- Fix typos
- Add examples
- Clarify confusing parts
- Translate to other languages

### 4. Share Your Experience
- Write a blog post
- Create a video tutorial
- Share on social media
- Present at meetups

---

## 📝 Contribution Guidelines

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused

```python
def good_function(param: str) -> Dict:
    """
    Brief description.
    
    Args:
        param: Description
    
    Returns:
        Description of return value
    """
    # Implementation
    pass
```

**Documentation:**
- Use clear, simple language
- Include code examples
- Add real-world context
- Link to related docs

### Commit Messages

Use conventional commits:

```
feat: Add new monitoring template
fix: Correct retry logic in agent
docs: Update quickstart guide
test: Add tests for newsletter agent
```

### Pull Request Process

1. **Fork the repo**
   ```bash
   git clone https://github.com/147API/awesome-openclaw.git
   cd foropenclaw
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write code
   - Add tests
   - Update docs

4. **Test locally**
   ```bash
   python3 your_agent.py
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: Your feature description"
   git push origin feature/your-feature-name
   ```

6. **Open a PR**
   - Describe what you changed
   - Link related issues
   - Add screenshots if relevant

---

## 🎨 Template Contribution Checklist

Submitting a new agent template? Make sure it has:

- [ ] Clear docstring with use case
- [ ] Type hints on functions
- [ ] Error handling
- [ ] Logging
- [ ] Example usage in `if __name__ == "__main__"`
- [ ] README or inline documentation
- [ ] No hardcoded secrets
- [ ] Configurable parameters

**Example structure:**
```
templates/
  your_agent.py          # Main agent code
  your_agent_config.py   # Configuration (optional)
examples/
  your_agent_example.py  # Usage example
docs/
  your_agent.md          # Detailed docs (optional)
```

---

## 📚 Documentation Contribution

### Adding a New Guide

1. Create markdown file in `docs/`
2. Follow existing structure
3. Include code examples
4. Add to README navigation

### Improving Existing Docs

- Fix typos/grammar
- Add missing examples
- Clarify confusing sections
- Update outdated info

---

## 🧪 Testing Guidelines

### Manual Testing
```python
# Test your agent manually first
agent = YourAgent(config)
result = agent.run()
assert result["status"] == "success"
```

### Automated Testing
```python
from tools.testing import AgentTester

tester = AgentTester()

@tester.test("Agent runs successfully")
def test_agent():
    agent = YourAgent(test_config)
    result = agent.run()
    assert result is not None

tester.run_all()
```

---

## 🌟 Recognition

Contributors will be:
- Listed in README
- Mentioned in release notes
- Given credit in documentation
- Invited to maintainer team (for regular contributors)

---

## 💬 Communication

### GitHub Discussions
Best for:
- Feature requests
- Design discussions
- Questions
- Sharing experiences

[Join discussions →](https://github.com/147API/awesome-openclaw/discussions)

### GitHub Issues
Best for:
- Bug reports
- Specific problems
- Documentation issues

[Open an issue →](https://github.com/147API/awesome-openclaw/issues)

### Email
For private matters: ai_147api@163.com

---

## 🚫 What We Don't Accept

- ❌ Untested code
- ❌ Code with hardcoded secrets
- ❌ Malicious code
- ❌ Plagiarized content
- ❌ Marketing spam
- ❌ Toy examples (we focus on production use)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution, no matter how small, helps make this project better for everyone.

**Questions about contributing?** [Ask in Discussions](https://github.com/147API/awesome-openclaw/discussions)

---

<div align="center">

**Ready to contribute?** [Fork the repo](https://github.com/147API/awesome-openclaw/fork) and get started!

Built with ❤️ by the OpenClaw community

</div>
