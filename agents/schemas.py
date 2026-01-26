"""
Pydantic schemas for agent deliverables.
"""

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field


class PlanSection(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class BusinessPlan(BaseModel):
    type: Literal["business_plan"]
    title: str = Field(..., min_length=1)
    sections: List[PlanSection]


class PitchSlide(BaseModel):
    title: str = Field(..., min_length=1)
    bullets: List[str]


class PitchDeck(BaseModel):
    type: Literal["pitch_deck"]
    title: str = Field(..., min_length=1)
    slides: List[PitchSlide]


class RoadmapPhase(BaseModel):
    name: str = Field(..., min_length=1)
    duration: str = Field(..., min_length=1)
    milestones: List[str]


class TechnicalRoadmap(BaseModel):
    type: Literal["technical_roadmap"]
    title: str = Field(..., min_length=1)
    phases: List[RoadmapPhase]
