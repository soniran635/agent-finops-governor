from typing import List, Dict, Any
from src.models import AgentRunTelemetry

class FinOpsTracker:
    """Calculates enterprise token costs, squad burn rates, and latency percentiles."""
    
    # Blended price per 1M tokens ($)
    MODEL_PRICING = {
        "llama3.2 (Local)": 0.00,
        "claude-3-5-sonnet": 3.00,
        "gpt-4o": 5.00,
        "deepseek-v3": 0.27
    }

    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        rate = self.MODEL_PRICING.get(model_name, 2.50)
        total_tokens = input_tokens + output_tokens
        return round((total_tokens / 1_000_000) * rate, 4)
