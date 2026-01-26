"""
Multi-Agent Business Plan Development System

10 Specialized Agents + 1 Governor AI for developing comprehensive SaaS business plans.

Usage:
    from agents import GovernorAI
    
    governor = GovernorAI()
    await governor.deploy_all_agents(mode="hybrid")
    governor.quality_control()
    governor.generate_executive_summary()
    if governor.authorize_commit():
        governor.save_all_outputs("./plans", commit=True)

Architecture:
    - Governor AI (Orchestrator/CEO)
    - 10 Specialized Agents (Business Plan Experts)
    - Claude API Integration
    - Async/Parallel Processing
    
Deliverables per Agent:
    1. Business Plan (25 pages)
    2. Pitch Deck (13 slides)
    3. Technical Roadmap (12 months)
"""

from .agent_orchestrator import GovernorAI, SpecializedAgent, SaaSType, AgentOutput, GovernorState
from .llm_provider import LLMProvider, LLMProviderError
from .schemas import BusinessPlan, PitchDeck, TechnicalRoadmap
from .agent_prompts import get_agent_prompt, get_all_saas_types

__all__ = [
    "GovernorAI",
    "SpecializedAgent",
    "SaaSType",
    "AgentOutput",
    "GovernorState",
    "get_agent_prompt",
    "get_all_saas_types",
    "LLMProvider",
    "LLMProviderError",
    "BusinessPlan",
    "PitchDeck",
    "TechnicalRoadmap",
]

__version__ = "1.0.0"
__author__ = "Hamiltonian Framework Team"
