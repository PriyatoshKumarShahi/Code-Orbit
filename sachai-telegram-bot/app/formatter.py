from typing import Dict, Any

def format_verification_result(data: Dict[str, Any]) -> str:
    """
    Takes the JSON response from the SachAI backend and formats it
    into a beautiful, persuasive Telegram HTML message.
    """
    
    # Extract fields based on the VerifyResponse schema from backend
    verdict = data.get("verdict", "Unknown")
    fake_prob = data.get("fake_probability", 0.0)
    credibility = data.get("credibility_score", 0.0)
    explanation = data.get("explanation", "No explanation available.")
    consequences = data.get("consequences")
    social_impact = data.get("social_impact")
    family_tree = data.get("family_tree", [])
    
    # Determine emoji based on verdict
    verdict_emoji = "⚠️"
    if "Fake" in verdict or "Suspicious" in verdict:
        verdict_emoji = "🚨"
    elif "Real" in verdict:
        verdict_emoji = "✅"
    elif "Needs More Evidence" in verdict:
        verdict_emoji = "🔎"

    # Start building the message using HTML tags
    msg = f"🤖 <b>SachAI Analysis</b>\n\n"
    msg += f"🔎 <b>Verdict:</b> {verdict_emoji} {verdict}\n"
    msg += f"📉 <b>Fake News Risk:</b> {int(fake_prob * 100)}/100\n"
    msg += f"📊 <b>Credibility Score:</b> {int(credibility)}/100\n\n"
    
    # Escape HTML characters in explanation just in case
    import html
    explanation_safe = html.escape(explanation)
    msg += f"🧾 <b>Truth Summary / Why:</b>\n<i>{explanation_safe}</i>\n\n"
    
    if family_tree:
        msg += f"🌳 <b>Previous Similar Versions:</b>\n"
        # Take up to 3 family tree items
        for node in family_tree[:3]:
            title = html.escape(node.get("title", "Unknown Claim"))
            year = node.get("year", "Past")
            msg += f"• [{year}] {title}\n"
        msg += "\n"
        
    # Combine consequences and social impact into the warning section
    if consequences or social_impact:
        msg += f"⚠️ <b>If this spreads further:</b>\n"
        if consequences:
            consequences_safe = html.escape(consequences)
            msg += f"• {consequences_safe}\n"
        if social_impact:
            social_impact_safe = html.escape(social_impact)
            msg += f"• {social_impact_safe}\n"
        msg += "\n"
        
    # Persuasive advice block
    if "Fake" in verdict or "Suspicious" in verdict:
        msg += f"🚫 <b>Advice:</b> Please do NOT forward this message! Spread the truth, not rumors."
    elif "Real" in verdict:
        msg += f"💡 <b>Advice:</b> This appears to be verified. However, always exercise caution with forwards."
    else:
        msg += f"🛡️ <b>Advice:</b> We need more evidence to be sure. Please wait before forwarding this to family or friends."

    return msg
