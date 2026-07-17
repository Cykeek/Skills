#!/usr/bin/env python3
"""
Product Designer Diagnostics
============================
Core diagnostic logic for Product Designer Skill.
"""

from typing import Any, Dict, List


class ProductDesignerDiagnostics:
    """Product designer diagnostic tools."""

    def __init__(self):
        pass

    def design_review(self, design: str, context: str, goals: List[str]) -> Dict[str, Any]:
        """Conduct a design review."""
        return {
            "design": design,
            "context": context,
            "goals": goals,
            "review": {
                "overall_read": f"Review of {design} in context of {context}",
                "what_is_working": [
                    "Clear visual hierarchy",
                    "Consistent spacing and typography"
                ],
                "breakdowns": [
                    {
                        "area": "Problem/goal fit",
                        "issue": "Design may not address the core user job",
                        "severity": "medium"
                    },
                    {
                        "area": "Flow/interaction",
                        "issue": "Secondary actions compete with primary CTA",
                        "severity": "high"
                    }
                ],
                "recommendations": [
                    "Reduce visual weight of secondary actions",
                    "Validate problem framing with user research"
                ],
                "open_questions": [
                    "What does success look like for this design?"
                ],
                "principles_referenced": ["Krug", "Rams", "Norman"]
            },
            "reference_files": ["references/design-craft.md", "references/design-thinking.md"]
        }

    def problem_framing(self, user: str, context: str, desired_progress: str, evidence: List[str], assumptions: List[str]) -> Dict[str, Any]:
        """Frame a design problem."""
        return {
            "decision_to_make": f"Design solution for {user} in {context}",
            "user_and_context": f"{user} in {context}",
            "job_story": f"When {context}, {user} wants to {desired_progress}",
            "what_we_know": evidence,
            "riskiest_assumptions": assumptions,
            "smallest_viable_next_step": "Low-fidelity concept test with 3-5 users",
            "success_signal": f"Users can complete {desired_progress} without confusion",
            "reference_files": ["references/design-thinking.md", "references/design-templates.md"]
        }

    def research_plan(self, decision: str, goal: str, constraints: List[str]) -> Dict[str, Any]:
        """Create a research plan."""
        return {
            "decision_this_supports": decision,
            "research_goal": goal,
            "constraints": constraints,
            "recommended_method": "Moderated usability testing with 5 users",
            "method_rationale": "Best for evaluating flow and interaction at this fidelity level",
            "participants": "5 users matching target persona",
            "tasks": [
                "Complete primary workflow",
                "Find and use secondary feature",
                "Recover from common error state"
            ],
            "metrics": ["Task success rate", "Time on task", "SEQ score"],
            "timeline": "1 week recruitment, 2 days testing, 1 day synthesis",
            "reference_files": ["references/ux-research.md", "references/design-templates.md"]
        }

    def design_brief(self, problem: str, user: str, constraints: List[str], scope: str) -> Dict[str, Any]:
        """Create a design brief."""
        return {
            "problem": problem,
            "user": user,
            "constraints": constraints,
            "scope": scope,
            "brief": {
                "project_name": f"Design: {problem[:50]}",
                "problem_statement": problem,
                "target_user": user,
                "non_goals": [
                    "Redesigning the entire platform",
                    "Changing the design system"
                ],
                "assumptions": [
                    "Users have basic digital literacy",
                    "Existing design system covers base components"
                ],
                "appetite": scope,
                "success_criteria": [
                    "Task completion rate > 90%",
                    "SUS score > 75",
                    "No critical accessibility issues"
                ],
                "risks": [
                    "Scope creep from stakeholder requests",
                    "Technical feasibility of proposed interactions"
                ],
                "next_steps": [
                    "Kickoff with PM and engineering",
                    "Competitive audit",
                    "Low-fidelity exploration"
                ]
            },
            "reference_files": ["references/design-templates.md", "references/design-thinking.md"]
        }

    def get_critique_template(self) -> Dict[str, Any]:
        """Get the critique template."""
        return {
            "template_name": "Principled Critique",
            "structure": [
                "Overall read",
                "What is working",
                "Where the design breaks down (Problem/goal fit, Flow/interaction, Craft/hierarchy, Trust/accessibility)",
                "Recommendations with rationale",
                "Open questions",
                "Principles referenced"
            ],
            "principles": ["Krug", "Rams", "Norman", "Maeda", "JTBD", "WCAG"],
            "example": {
                "overall_read": "Strong visual design but primary action is buried",
                "what_is_working": [
                    "Typography scale is consistent",
                    "Color palette supports brand"
                ],
                "breakdowns": [
                    {
                        "area": "Problem/goal fit",
                        "issue": "Design solves a different problem than stated",
                        "severity": "high"
                    }
                ],
                "recommendations": [
                    "Elevate primary CTA - because Krug says don't make them think",
                    "Reduce secondary actions - Rams says less but better"
                ],
                "open_questions": [
                    "What is the actual user job here?"
                ],
                "principles_referenced": ["Krug", "Rams"]
            },
            "reference_file": "references/design-templates.md"
        }

    def get_design_checklist(self, checklist_type: str = "handoff") -> Dict[str, Any]:
        """Get design review checklist."""
        checklists = {
            "handoff": {
                "name": "Design Handoff Checklist",
                "items": [
                    {"category": "User Flows", "item": "Happy path complete", "required": True},
                    {"category": "User Flows", "item": "Empty, loading, error, edge states designed", "required": True},
                    {"category": "User Flows", "item": "Walked entire flow without stopping", "required": True},
                    {"category": "Specifications", "item": "Responsive layouts covered", "required": True},
                    {"category": "Specifications", "item": "Interactive states defined", "required": True},
                    {"category": "Specifications", "item": "Typography, spacing, color, tokens documented", "required": True},
                    {"category": "Specifications", "item": "Behavior notes and transitions included", "required": True},
                    {"category": "Accessibility", "item": "Contrast meets target", "required": True},
                    {"category": "Accessibility", "item": "Touch targets and focus states defined", "required": True},
                    {"category": "Accessibility", "item": "Screen-reader labels accounted for", "required": True},
                    {"category": "Accessibility", "item": "Keyboard flow works", "required": True},
                    {"category": "Trust", "item": "Data disclosures clear", "required": True},
                    {"category": "Trust", "item": "Error recovery defined", "required": True},
                    {"category": "Trust", "item": "Destructive/irreversible actions protected", "required": True},
                    {"category": "Design System", "item": "Existing components reused", "required": True},
                    {"category": "Design System", "item": "New components documented", "required": True},
                    {"category": "Design System", "item": "Behavior contracts clear", "required": True}
                ]
            },
            "accessibility": {
                "name": "Accessibility Audit Checklist",
                "items": [
                    {"category": "Color", "item": "Text contrast >= 4.5:1 (AA) / 7:1 (AAA)", "required": True},
                    {"category": "Color", "item": "Non-text contrast >= 3:1", "required": True},
                    {"category": "Color", "item": "Color not sole means of conveying info", "required": True},
                    {"category": "Interaction", "item": "Touch targets >= 44x44px", "required": True},
                    {"category": "Interaction", "item": "Focus indicators visible and clear", "required": True},
                    {"category": "Interaction", "item": "Keyboard navigation works fully", "required": True},
                    {"category": "Interaction", "item": "No keyboard traps", "required": True},
                    {"category": "Content", "item": "Alt text for all meaningful images", "required": True},
                    {"category": "Content", "item": "Heading hierarchy logical (h1-h6)", "required": True},
                    {"category": "Content", "item": "Form labels associated with inputs", "required": True},
                    {"category": "Content", "item": "Error messages descriptive and actionable", "required": True},
                    {"category": "Content", "item": "Language declared and changes identified", "required": True},
                    {"category": "Motion", "item": "Reduced motion respected", "required": True},
                    {"category": "Motion", "item": "No auto-playing content > 5s without controls", "required": True}
                ]
            },
            "trust": {
                "name": "Trust & Ethics Review Checklist",
                "items": [
                    {"category": "Clarity", "item": "User understands what happens next", "required": True},
                    {"category": "Clarity", "item": "System actions stated clearly (Nielsen #1)", "required": True},
                    {"category": "Consent", "item": "Data collection explained in plain language", "required": True},
                    {"category": "Consent", "item": "Automated actions disclosed", "required": True},
                    {"category": "Consent", "item": "Billing changes communicated clearly", "required": True},
                    {"category": "Control", "item": "Undo/edit/delete available for user actions", "required": True},
                    {"category": "Control", "item": "Easy opt-out from non-essential features", "required": True},
                    {"category": "Fairness", "item": "Choices balanced and honestly presented", "required": True},
                    {"category": "Fairness", "item": "No dark patterns (confirmshaming, hidden costs, etc.)", "required": True},
                    {"category": "Recovery", "item": "Errors prevented with constraints", "required": True},
                    {"category": "Recovery", "item": "User content preserved on error", "required": True},
                    {"category": "Recovery", "item": "Clear recovery path for every error", "required": True}
                ]
            }
        }
        return checklists.get(checklist_type, checklists["handoff"])