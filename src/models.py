from pydantic import BaseModel, Field
from typing import List, Optional

class AgentRunTelemetry(BaseModel):
    run_id: str
    squad_name: str  # e.g., 'Games Studio Alpha', 'Streaming Core', 'Platform Services'
    model_name: str  # e.g., 'llama3.2', 'claude-3-5-sonnet', 'gpt-4o'
    input_tokens: int
    output_tokens: int
    latency_ms: int
    tool_calls_sequence: List[str] = []
    task_completed: bool = True

class CircuitBreakerAlert(BaseModel):
    run_id: str
    status: str  # 'NORMAL_OPERATION' or 'CIRCUIT_TRIPPED'
    trigger_reason: Optional[str] = None
    saved_tokens_estimate: int = 0
    financial_cost_avoided_usd: float = 0.0
