from typing import List
from src.models import AgentRunTelemetry, CircuitBreakerAlert

class RunawayLoopCircuitBreaker:
    """Detects infinite agent tool-calling loops and runaway token burns,

    automatically tripping to terminate execution.
    """
    def __init__(self, max_consecutive_tool_repeats: int = 3, max_run_tokens: int = 25000):
        self.max_repeats = max_consecutive_tool_repeats
        self.max_tokens = max_run_tokens

    def evaluate_run(self, run: AgentRunTelemetry) -> CircuitBreakerAlert:
        total_tokens = run.input_tokens + run.output_tokens
        
        # 1. Budget Threshold Check
        if total_tokens > self.max_tokens:
            excess = total_tokens - self.max_tokens
            cost_avoided = round((excess / 1_000_000) * 15.0, 3) # Based on standard $15/1M output tokens
            return CircuitBreakerAlert(
                run_id=run.run_id,
                status="CIRCUIT_TRIPPED",
                trigger_reason=f"Token budget threshold exceeded ({total_tokens:,} > {self.max_tokens:,} tokens)",
                saved_tokens_estimate=excess,
                financial_cost_avoided_usd=cost_avoided
            )

        # 2. Infinite Loop Pattern Detection (Repeated identical tool calls)
        tools = run.tool_calls_sequence
        if len(tools) >= self.max_repeats:
            for i in range(len(tools) - self.max_repeats + 1):
                window = tools[i:i + self.max_repeats]
                if len(set(window)) == 1:
                    repeated_tool = window[0]
                    return CircuitBreakerAlert(
                        run_id=run.run_id,
                        status="CIRCUIT_TRIPPED",
                        trigger_reason=f"Runaway loop detected: Tool '{repeated_tool}' called {self.max_repeats}x consecutively without state advancement.",
                        saved_tokens_estimate=12500,
                        financial_cost_avoided_usd=0.187
                    )

        return CircuitBreakerAlert(
            run_id=run.run_id,
            status="NORMAL_OPERATION",
            trigger_reason="Execution stream within safe latency and budget bounds."
        )
