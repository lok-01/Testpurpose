import requests
from typing import Dict, Any, List
from app.config import settings

SYSTEM_PROMPT_TEMPLATE = """You are AstroRize Vedic AI, a classical Parashari Vedic Astrology calculation and interpretation assistant.
You strictly adhere to these immutable rules:
1. Ground every statement exclusively on the astronomical and Vedic calculation data provided below.
2. Never invent, guess, or hallucinate planetary positions, signs, degrees, house placements, Dasha periods, Yogas, or Doshas.
3. Clearly state the exact planetary placement, house, or dasha that underpins each astrological insight.
4. Distinguish clearly between empirical astronomical facts (e.g. degrees, retrograde status) and traditional interpretive principles.
5. Do NOT make fatalistic or fear-based predictions. Avoid predicting exact dates of death, marriage, illness, or wealth.
6. Speak in professional, encouraging, and scholarly English.

--- CALCULATED CHART DATA ---
{chart_context}
-----------------------------
"""

class AIChatService:
    def __init__(self):
        self.ollama_url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        self.model = settings.OLLAMA_MODEL

    def generate_chat_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        chart_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Grounded Vedic Chatbot: Builds context from Swiss Ephemeris chart calculation,
        queries Ollama local LLM, or smoothly falls back to deterministic rule-based analysis.
        """
        chart_context_str = self._build_context_summary(chart_data)
        system_instruction = SYSTEM_PROMPT_TEMPLATE.format(chart_context=chart_context_str)

        # Attempt query via Ollama
        try:
            messages = [{"role": "system", "content": system_instruction}]
            for msg in conversation_history[-6:]:  # Context window for past turns
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_message})

            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": settings.LLM_TEMPERATURE,
                    "num_ctx": settings.LLM_CONTEXT_LENGTH,
                }
            }

            resp = requests.post(self.ollama_url, json=payload, timeout=8.0)
            if resp.status_code == 200:
                resp_json = resp.json()
                content = resp_json.get("message", {}).get("content", "")
                if content:
                    return {
                        "response": content,
                        "source": "LLM",
                        "model": self.model,
                        "provider": "Ollama",
                        "grounded_context": chart_context_str,
                    }
        except Exception:
            pass  # Fall through to rule-based engine

        # Deterministic Rule-Based Fallback
        fallback_reply = self._generate_rule_based_response(user_message, chart_data)
        return {
            "response": fallback_reply,
            "source": "Rule-Based Engine (Local Fallback)",
            "model": "Parashari Expert System v1.0",
            "provider": "AstroRize Deterministic Engine",
            "grounded_context": chart_context_str,
        }

    def _build_context_summary(self, chart_data: Dict[str, Any]) -> str:
        summary = chart_data.get("chart_summary", {})
        planets = chart_data.get("planets", [])
        houses = chart_data.get("houses", [])
        yogas = chart_data.get("yogas", [])
        doshas = chart_data.get("doshas", [])
        dashas = chart_data.get("dashas", {})

        lines = []
        lines.append(f"Ascendant (Lagna): {summary.get('lagna_rashi')} at {summary.get('lagna_dms')} (Lord: {summary.get('lagna_lord')}, Nakshatra: {summary.get('lagna_nakshatra')} Pada {summary.get('lagna_pada')}).")
        lines.append(f"Ayanamsa: {summary.get('ayanamsa_name')} ({summary.get('ayanamsa_value'):.4f}°).")
        lines.append(f"Current Mahadasha: {dashas.get('current_mahadasha')}, Antardasha: {dashas.get('current_antardasha')}, Pratyantardasha: {dashas.get('current_pratyantardasha')}.")
        lines.append("\nPlanetary Placements:")
        for p in planets:
            comb = " (Combust)" if p.get("is_combust") else ""
            ret = " [Retrograde]" if p.get("is_retrograde") else ""
            lines.append(f"- {p['name']}: {p['rashi']} {p['dms']} in House {p['house']} ({p['dignity']}), Nakshatra {p['nakshatra']} Pada {p['pada']} (Lord: {p['nakshatra_lord']}){comb}{ret}")

        if yogas:
            present_yogas = [y['name'] for y in yogas if y.get('is_present') and not y.get('is_cancelled')]
            if present_yogas:
                lines.append(f"\nActive Yogas: {', '.join(present_yogas)}")

        if doshas:
            present_doshas = [f"{d['name']} ({d['severity']})" for d in doshas if d.get('is_present')]
            if present_doshas:
                lines.append(f"Dosha Conditions: {', '.join(present_doshas)}")

        return "\n".join(lines)

    def _generate_rule_based_response(self, query: str, chart_data: Dict[str, Any]) -> str:
        q = query.lower()
        summary = chart_data.get("chart_summary", {})
        planets = {p["name"]: p for p in chart_data.get("planets", [])}
        dashas = chart_data.get("dashas", {})
        yogas = [y for y in chart_data.get("yogas", []) if y.get("is_present") and not y.get("is_cancelled")]
        doshas = [d for d in chart_data.get("doshas", []) if d.get("is_present")]

        if "lagna" in q or "ascendant" in q:
            return (
                f"**Ascendant (Lagna) Analysis**:\n\n"
                f"Your Lagna is **{summary.get('lagna_rashi')}** at **{summary.get('lagna_dms')}**, ruled by **{summary.get('lagna_lord')}**.\n"
                f"The Lagna falls in the Nakshatra of **{summary.get('lagna_nakshatra')}** (Pada {summary.get('lagna_pada')}).\n\n"
                f"In Vedic astrology, the Lagna defines your physical constitution, innate orientation, and life direction. "
                f"The ruler, {summary.get('lagna_lord')}, is situated in House {planets.get(summary.get('lagna_lord', ''), {}).get('house', 'N/A')} "
                f"in {planets.get(summary.get('lagna_lord', ''), {}).get('rashi', 'N/A')}, directing focus towards the affairs of that house."
            )

        elif "moon" in q or "nakshatra" in q:
            m = planets.get("Moon", {})
            return (
                f"**Moon and Nakshatra Analysis**:\n\n"
                f"Your Moon is located in **{m.get('rashi')}** at **{m.get('dms')}** in House **{m.get('house')}**.\n"
                f"The birth Nakshatra is **{m.get('nakshatra')}** (Pada {m.get('pada')}), governed by the planetary lord **{m.get('nakshatra_lord')}**.\n\n"
                f"The Moon represents the psychological mind (Manas) and emotional memory. Placed in {m.get('rashi')} with dignity '{m.get('dignity')}', "
                f"it shapes how you instinctively respond to environmental stressors and relationship dynamics."
            )

        elif "dasha" in q or "mahadasha" in q or "period" in q:
            return (
                f"**Vimshottari Dasha Progression**:\n\n"
                f"- **Current Mahadasha**: {dashas.get('current_mahadasha', 'N/A')}\n"
                f"- **Current Antardasha**: {dashas.get('current_antardasha', 'N/A')}\n"
                f"- **Current Pratyantardasha**: {dashas.get('current_pratyantardasha', 'N/A')}\n"
                f"- **Birth Nakshatra**: {dashas.get('birth_nakshatra', 'N/A')}\n"
                f"- **Starting Balance**: {dashas.get('balance_years', 'N/A')} years of {dashas.get('starting_mahadasha_lord', 'N/A')} Mahadasha.\n\n"
                f"The Vimshottari cycle unfolds past karma chronologically. Events and psychological themes during this period are primarily activated through the house rulerships and dignity of {dashas.get('current_mahadasha')}."
            )

        elif "yoga" in q:
            if not yogas:
                return "No major standard Parashari Yogas are uniquely activated in this chart without mitigating cancellations."
            y_list = "\n".join([f"- **{y['name']}** ({y['category']}): {y['description']}" for y in yogas])
            return f"**Active Parashari Yogas Identified in Your Chart**:\n\n{y_list}"

        elif "dosha" in q or "manglik" in q:
            if not doshas:
                return "No primary Dosha afflictions (such as Manglik or Kala Sarpa) are active in this chart."
            d_list = "\n".join([f"- **{d['name']}**: Severity is *{d['severity']}*. Rule: {d['rule_applied']} {d['explanation']}" for d in doshas])
            return f"**Dosha Evaluation (Objective Vedic Verification)**:\n\n{d_list}"

        elif "career" in q or "10th" in q or "job" in q:
            p10 = [p["name"] for p in planets.values() if p["house"] == 10]
            occupants_str = ", ".join(p10) if p10 else "None (Empty house, analyzed via sign lord)"
            h10_lord = chart_data.get("houses", [{}])[9].get("sign_lord", "N/A") if len(chart_data.get("houses", [])) >= 10 else "N/A"
            return (
                f"**10th House (Karma Bhava) & Professional Orientation**:\n\n"
                f"- **10th House Sign**: {chart_data.get('houses', [{}])[9].get('sign', 'N/A') if len(chart_data.get('houses', [])) >= 10 else 'N/A'}\n"
                f"- **10th Lord**: {h10_lord} (located in House {planets.get(h10_lord, {}).get('house', 'N/A')})\n"
                f"- **Occupants in 10th House**: {occupants_str}\n\n"
                f"In Parashari astrology, career direction and societal impact emerge from the interplay between the 10th lord and any occupying grahas, synthesized with the Dashamsha (D10) division."
            )

        else:
            return (
                f"**Vedic Chart Overview for {summary.get('lagna_rashi')} Lagna**:\n\n"
                f"- **Lagna**: {summary.get('lagna_rashi')} at {summary.get('lagna_dms')}\n"
                f"- **Moon**: {planets.get('Moon', {}).get('rashi')} in {planets.get('Moon', {}).get('nakshatra')} Pada {planets.get('Moon', {}).get('pada')}\n"
                f"- **Sun**: {planets.get('Sun', {}).get('rashi')} at {planets.get('Sun', {}).get('dms')}\n"
                f"- **Current Dasha**: {dashas.get('current_mahadasha')} - {dashas.get('current_antardasha')}\n\n"
                f"You can ask specific questions such as:\n"
                f"- *'Explain my Lagna and 1st house'*\n"
                f"- *'Tell me about my Moon Nakshatra'*\n"
                f"- *'Explain my current Mahadasha'*\n"
                f"- *'Which Yogas are present in my chart?'*\n"
                f"- *'Do I have Manglik or Kala Sarpa Dosha?'*\n"
                f"- *'Analyze my career and 10th house'*"
            )

ai_chat_service = AIChatService()
