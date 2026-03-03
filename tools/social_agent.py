"""
Social Media Agent

Automatically promotes content across multiple platforms:
- Twitter/X
- V2EX
- Reddit
- WeChat

Inspired by Fu Sheng's practice of using AI for social media management.
"""

import requests
import json
from datetime import datetime
from typing import Dict, List

class SocialAgent:
    """
    Social media automation agent.
    
    Capabilities:
    - Generate platform-specific content
    - Auto-post to multiple channels
    - Track engagement metrics
    - Respond to mentions
    """
    
    def __init__(self, wxwork_webhook: str = None):
        # 从环境变量读取webhook，避免硬编码
        import os
        self.wxwork_webhook = wxwork_webhook or os.getenv("WXWORK_WEBHOOK", "")
        if not self.wxwork_webhook:
            raise ValueError("请设置 WXWORK_WEBHOOK 环境变量")
        self.platforms = ["twitter", "v2ex", "reddit", "wechat"]
    
    def generate_post(self, content_type: str, project: str, details: Dict) -> Dict[str, str]:
        """
        Generate platform-specific posts.
        
        Args:
            content_type: "release", "update", "tip", "showcase"
            project: "awesome-openclaw" or "ai-weekly"
            details: Additional context
        
        Returns:
            Dict with posts for each platform
        """
        posts = {}
        
        if content_type == "release":
            # Twitter (280 chars)
            posts["twitter"] = f"🚀 {project} just released!\n\n{details.get('highlight', '')}\n\n⭐ Star: {details.get('repo_url', '')}\n\n#AI #OpenClaw #OpenSource"
            
            # V2EX (longer format)
            posts["v2ex"] = f"""# {project} 发布更新

{details.get('description', '')}

**主要特性：**
{details.get('features', '')}

**GitHub：** {details.get('repo_url', '')}

欢迎 Star 和反馈！"""
            
            # Reddit
            posts["reddit"] = f"""**{project} - New Release**

{details.get('description', '')}

Key features:
{details.get('features', '')}

GitHub: {details.get('repo_url', '')}

Feedback welcome!"""
            
            # WeChat
            posts["wechat"] = f"""🎉 {project} 更新啦！

{details.get('description', '')}

✨ 亮点：
{details.get('features', '')}

🔗 {details.get('repo_url', '')}

欢迎体验和反馈！"""
        
        elif content_type == "tip":
            # Daily tip format
            posts["twitter"] = f"💡 OpenClaw Tip:\n\n{details.get('tip', '')}\n\n#AI #Productivity"
            posts["wechat"] = f"💡 每日技巧\n\n{details.get('tip', '')}"
        
        return posts
    
    def post_to_wechat(self, content: str) -> bool:
        """Post to WeChat Work."""
        try:
            response = requests.post(
                self.wxwork_webhook,
                json={"msgtype": "text", "text": {"content": content}},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"WeChat post failed: {e}")
            return False
    
    def post_to_v2ex(self, title: str, content: str, node: str = "programmer") -> Dict:
        """
        Post to V2EX.
        
        Note: Requires V2EX API token and manual posting for now.
        Returns draft for manual posting.
        """
        return {
            "platform": "v2ex",
            "node": node,
            "title": title,
            "content": content,
            "action": "manual_post_required",
            "url": f"https://www.v2ex.com/new/{node}"
        }
    
    def post_to_reddit(self, subreddit: str, title: str, content: str) -> Dict:
        """
        Post to Reddit.
        
        Note: Requires Reddit API credentials.
        Returns draft for manual posting.
        """
        return {
            "platform": "reddit",
            "subreddit": subreddit,
            "title": title,
            "content": content,
            "action": "manual_post_required",
            "url": f"https://reddit.com/r/{subreddit}/submit"
        }
    
    def promote_project(self, project: str, announcement: str) -> Dict:
        """
        Promote a project across all platforms.
        
        Example:
            agent.promote_project(
                "awesome-openclaw",
                "New multi-agent templates added!"
            )
        """
        results = {}
        
        # Generate posts
        posts = self.generate_post(
            "update",
            project,
            {
                "description": announcement,
                "repo_url": f"https://github.com/147API/{project}"
            }
        )
        
        # Post to WeChat (automatic)
        if "wechat" in posts:
            results["wechat"] = {
                "success": self.post_to_wechat(posts["wechat"]),
                "content": posts["wechat"]
            }
        
        # Generate drafts for other platforms
        if "v2ex" in posts:
            results["v2ex"] = self.post_to_v2ex(
                f"{project} 更新",
                posts["v2ex"]
            )
        
        if "reddit" in posts:
            results["reddit"] = self.post_to_reddit(
                "OpenClaw",
                f"{project} Update",
                posts["reddit"]
            )
        
        if "twitter" in posts:
            results["twitter"] = {
                "platform": "twitter",
                "content": posts["twitter"],
                "action": "manual_post_required",
                "note": "Copy and paste to Twitter"
            }
        
        return results
    
    def daily_engagement(self) -> str:
        """
        Generate daily engagement content.
        
        Tips, insights, or interesting findings to keep audience engaged.
        """
        tips = [
            "💡 OpenClaw Tip: Use `sessions_spawn` to run background tasks without blocking your main workflow.",
            "🔥 Did you know? You can create a team of AI agents that work together, just like Fu Sheng's 8-agent setup.",
            "⚡ Pro tip: Use `cron` jobs to automate repetitive tasks. Set it and forget it!",
            "🎯 Best practice: Always add error handling to your agents. Graceful degradation is key.",
            "🚀 Quick win: Start with monitoring agents. They're easy to build and immediately useful."
        ]
        
        # Rotate through tips
        import random
        return random.choice(tips)


# Example usage
if __name__ == "__main__":
    agent = SocialAgent()
    
    # Promote Awesome OpenClaw
    print("🚀 Promoting Awesome OpenClaw...\n")
    
    results = agent.promote_project(
        "awesome-openclaw",
        "Added multi-agent team templates inspired by Fu Sheng's practice!"
    )
    
    print("Results:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    print("\n" + "="*50)
    print("\n💡 Daily engagement tip:")
    print(agent.daily_engagement())
