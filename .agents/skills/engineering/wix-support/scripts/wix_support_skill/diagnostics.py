#!/usr/bin/env python3
"""
Wix Support Diagnostics Module
==============================
Core diagnostic logic for Wix platform issues.
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from wix_support_skill.output_manager import OutputManager, OutputFormat


class WixDiagnostics:
    """Wix platform diagnostic tools."""

    # Editor type indicators
    EDITOR_INDICATORS = {
        "classic": [
            "left sidebar with big + button",
            "separate mobile editor toggle",
            "add elements panel on left",
            "pages menu on left"
        ],
        "studio": [
            "breakpoint selector bar at top center",
            "inspector panel on right",
            "canvas with responsive breakpoints",
            "layers panel"
        ],
        "editorx": [
            "similar to studio but older ui",
            "being migrated to studio"
        ]
    }

    # Common DNS record types for Wix
    WIX_DNS_RECORDS = {
        "A": {"name": "@", "value": "185.230.63.107", "description": "Root domain points to Wix"},
        "CNAME": {"name": "www", "value": "www.wixdns.net", "description": "www subdomain"},
        "TXT": {"name": "@", "value": "wix-site-verification", "description": "Wix site verification"}
    }

    def __init__(self):
        self.output_manager = OutputManager(OutputFormat.JSON)

    def diagnose_editor_issue(self, editor: str, issue: str) -> Dict[str, Any]:
        """Diagnose common editor issues."""
        editor = editor.lower()
        issue_lower = issue.lower()

        diagnosis = {
            "editor": editor,
            "issue": issue,
            "diagnosis": "",
            "steps": [],
            "reference_file": ""
        }

        # Mobile-only issues
        if "mobile" in issue_lower and "desktop" not in issue_lower:
            if editor == "classic":
                diagnosis["diagnosis"] = "Mobile-only layout issue in Classic Editor"
                diagnosis["steps"] = [
                    "Open Classic Editor",
                    "Click mobile icon (phone symbol) in top bar to switch to mobile editor",
                    "Rearrange elements for mobile layout - changes here don't affect desktop",
                    "Publish when done"
                ]
                diagnosis["reference_file"] = "references/editors.md"
            elif editor == "studio":
                diagnosis["diagnosis"] = "Mobile breakpoint issue in Wix Studio"
                diagnosis["steps"] = [
                    "Open Wix Studio editor",
                    "Click mobile breakpoint icon in breakpoint bar (top center)",
                    "Adjust layout using Inspector panel on right",
                    "Use auto-layout or manual positioning per breakpoint",
                    "Publish when done"
                ]
                diagnosis["reference_file"] = "references/editors.md"

        # Element-specific issues
        elif "text" in issue_lower and ("wrong" in issue_lower or "missing" in issue_lower):
            diagnosis["diagnosis"] = "Text content issue - likely CMS binding or dynamic text"
            diagnosis["steps"] = [
                "Click the text element in editor",
                "Check Settings panel -> Connect to Data (CMS binding)",
                "If bound to CMS: verify collection has data, check dataset filter",
                "If not bound: check if text is set via Velo code (.text property)",
                "Republish site"
            ]
            diagnosis["reference_file"] = "references/cms.md"

        elif "image" in issue_lower and ("broken" in issue_lower or "missing" in issue_lower or "not showing" in issue_lower):
            diagnosis["diagnosis"] = "Image not loading - source URL or CMS issue"
            diagnosis["steps"] = [
                "Right-click image in browser -> Copy image address",
                "Paste URL in new tab - does it load?",
                "If 404: re-upload image in Media Manager",
                "If CMS-bound: check collection has image field populated",
                "Check dataset is connected and in Read/Read-Write mode"
            ]
            diagnosis["reference_file"] = "references/cms.md"

        elif "button" in issue_lower and ("dead" in issue_lower or "not working" in issue_lower or "link" in issue_lower):
            diagnosis["diagnosis"] = "Button/link not functioning"
            diagnosis["steps"] = [
                "Click button in editor -> Settings panel -> Link",
                "Verify link destination (page, URL, anchor, email, phone)",
                "If Velo handler: check console (F12) for errors",
                "Verify element ID matches Velo selector (#exactMatch)",
                "Check $w.onReady() wrapper in Velo code"
            ]
            diagnosis["reference_file"] = "references/velo-apis.md"

        # Site-wide issues
        elif "header" in issue_lower or "footer" in issue_lower or "all pages" in issue_lower:
            diagnosis["diagnosis"] = "Site-wide header/footer/master page issue"
            diagnosis["steps"] = [
                "In editor, look for Master Page / Header & Footer section",
                "Classic: Pages menu -> Master Page",
                "Studio: Layers panel -> Master Section (header/footer)",
                "Edit the master element - changes apply to all pages",
                "Publish"
            ]
            diagnosis["reference_file"] = "references/editors.md"

        # Editor vs live
        elif "editor" in issue_lower and "live" not in issue_lower:
            diagnosis["diagnosis"] = "Editor-only rendering glitch"
            diagnosis["steps"] = [
                "Refresh browser (Ctrl+R / Cmd+R)",
                "Clear browser cache",
                "Try incognito/private window",
                "If persists: check Wix status page for platform issues"
            ]
            diagnosis["reference_file"] = "references/debug-known-bugs.md"

        elif "live" in issue_lower or "published" in issue_lower:
            diagnosis["diagnosis"] = "Live site issue - check publish status"
            diagnosis["steps"] = [
                "Verify you clicked Publish in editor",
                "Check specific URL - test direct link",
                "Clear browser cache / try incognito",
                "Check DNS if custom domain"
            ]
            diagnosis["reference_file"] = "references/seo-performance.md"

        # Generic fallback
        else:
            diagnosis["diagnosis"] = "General layout/rendering issue"
            diagnosis["steps"] = [
                f"Confirm editor: {editor.title()}",
                "Check if issue is mobile-only, desktop-only, or both",
                "Identify specific element(s) affected",
                "Try refresh and cache clear",
                "Check publish status"
            ]
            diagnosis["reference_file"] = "references/debug-known-bugs.md"

        return diagnosis

    def diagnose_cms_404(self, collection: str, page_slug: str) -> Dict[str, Any]:
        """Diagnose CMS dynamic page 404 issues."""
        is_dynamic = "/{item" in page_slug or "dynamic" in page_slug.lower() or page_slug.count("/") >= 2

        checks = [
            {
                "check": "Is it a Dynamic Item Page?",
                "status": "info",
                "details": "In CMS, open the collection -> check if page is 'Dynamic Item Page' type",
                "action": "If yes, go to check 2. If no, go to check 3."
            },
            {
                "check": "Pages Generated count",
                "status": "info",
                "details": "Dataset Settings -> Pages Generated",
                "action": "If Pages Generated < Total Items -> ACTIVE FILTER: delete filter -> Publish"
            },
            {
                "check": "CMS-connected?",
                "status": "info",
                "details": "Check if element/dataset is connected to collection",
                "action": "If connected, go to check 4. If not, connect dataset to collection."
            },
            {
                "check": "Dataset mode",
                "status": "info",
                "details": "Dataset Settings -> Mode must be 'Read' or 'Read & Write' (NOT 'Write Only')",
                "action": "If correct mode, go to check 5. If not, change mode -> Publish"
            },
            {
                "check": "Collection permissions",
                "status": "info",
                "details": "CMS -> Collection -> Permissions -> 'Visitor' must have 'Read' access",
                "action": "If Visitor has Read, go to check 6. If not, add Read permission -> Publish"
            },
            {
                "check": "CMS synced to Live?",
                "status": "info",
                "details": "CMS -> top bar: ensure 'Live' is selected (not just Sandbox)",
                "action": "If synced, go to check 7. If not, click 'Sync to Live' -> Publish"
            },
            {
                "check": "Hidden by Velo?",
                "status": "info",
                "details": "Search Velo code for .hide() or .collapse() on this element/page",
                "action": "If found, remove or fix the hiding logic. If not, contact Wix Support."
            }
        ]

        return {
            "collection": collection,
            "page_slug": page_slug,
            "is_dynamic_item_page": is_dynamic,
            "checks": checks,
            "reference_file": "references/cms.md",
            "next_steps": [
                "Run through checks 1-7 in order",
                "Most common fix: Active filter in Dataset Settings (check 2)",
                "Second most common: CMS not synced to Live (check 6)"
            ]
        }

    def diagnose_velo_issue(self, element_id: str, code: str, error: str = "") -> Dict[str, Any]:
        """Diagnose Velo code issues."""
        issues = []
        suggestions = []

        # Check $w.onReady wrapper
        if "$w.onReady" not in code and "onReady" not in code:
            issues.append("Missing $w.onReady() wrapper")
            suggestions.append("Wrap all element selectors in: $w.onReady(function() { ... })")

        # Check element ID format
        if element_id and not element_id.startswith("#"):
            issues.append(f"Element ID '{element_id}' missing # prefix")
            suggestions.append(f"Use '#{element_id}' in $w() selector")

        # Check for imports
        if "import" not in code and ("backend" in code or "wix-" in code):
            issues.append("Missing imports for Wix APIs")
            suggestions.append("Add imports at top: import { authentication } from 'wix-auth'; etc.")

        # Check for CORS patterns
        if "fetch(" in code and "backend" not in code.lower():
            issues.append("Possible CORS issue - frontend fetch to external API")
            suggestions.append("Move external API calls to backend .jsw file")

        # Check for auth patterns
        if any(kw in code.lower() for kw in ["apikey", "api_key", "secret", "token"]):
            issues.append("API secret/key in frontend code - SECURITY RISK")
            suggestions.append("Move secrets to Secrets Manager, call via backend .jsw")

        # Check for common Velo patterns
        if "console.log" not in code and error:
            suggestions.append("Add console.log() statements to debug the flow")

        return {
            "element_id": element_id,
            "code_provided": bool(code.strip()),
            "error_reported": error,
            "issues_found": issues,
            "suggestions": suggestions,
            "reference_file": "references/velo-apis.md",
            "template": self._get_velo_template(element_id),
            "confidence": "high" if issues else "medium"
        }

    def _get_velo_template(self, element_id: str) -> str:
        """Generate a basic Velo template."""
        clean_id = element_id.lstrip("#")
        return f"""$w.onReady(function () {{
    // Element selector - ID must match exactly: {element_id}
    const $element = $w("#{clean_id}");

    // Example: Click handler
    $element.onClick(() => {{
        console.log("Element clicked");
        // Your logic here
    }});

    // Example: Backend call
    // import {{ myFunction }} from 'backend/myModule';
    // myFunction().then(result => console.log(result));
}});"""

    def check_dns(self, domain: str) -> Dict[str, Any]:
        """Check domain DNS configuration (returns expected config)."""
        return {
            "domain": domain,
            "expected_records": [
                {
                    "type": "A",
                    "name": "@",
                    "value": "185.230.63.107",
                    "description": "Root domain points to Wix"
                },
                {
                    "type": "CNAME",
                    "name": "www",
                    "value": "www.wixdns.net",
                    "description": "www subdomain"
                }
            ],
            "common_issues": [
                "Conflicting A records (multiple @ records)",
                "CNAME for www pointing elsewhere",
                "Missing SSL - auto-provisions after DNS propagates (up to 24h)",
                "Propagation delay - can take up to 48 hours"
            ],
            "verification_url": f"https://dnschecker.org/#A/{domain}",
            "escalation_criteria": "If DNS correct for 48h+ and SSL not provisioned -> Wix Support",
            "reference_file": "references/seo-performance.md"
        }

    def get_editor_comparison(self) -> Dict[str, Any]:
        """Get editor comparison for user identification."""
        return {
            "editors": [
                {
                    "name": "Classic Editor",
                    "description": "Original Wix editor with fixed layouts",
                    "indicators": [
                        "Left sidebar with large '+' (Add) button",
                        "Separate 'Mobile Editor' toggle in top bar",
                        "Pages panel on left side",
                        "No breakpoint bar at top"
                    ],
                    "key_features": [
                        "Fixed layouts per device",
                        "Separate mobile editor",
                        "Master Page for headers/footers",
                        "App Market integration"
                    ],
                    "mobile_editing": "Click mobile icon in top bar -> rearrange independently",
                    "status": "Maintained but legacy"
                },
                {
                    "name": "Wix Studio",
                    "description": "Modern responsive editor with breakpoint-based design",
                    "indicators": [
                        "Breakpoint selector bar at top center (Desktop/Tablet/Mobile)",
                        "Inspector panel on right side (Design, Layout, Interactions)",
                        "Layers panel showing component hierarchy",
                        "Canvas shows responsive grid"
                    ],
                    "key_features": [
                        "Responsive breakpoints",
                        "CSS Grid / Flexbox layouts",
                        "Global design tokens",
                        "Master Sections for headers/footers",
                        "Developer mode with Velo"
                    ],
                    "mobile_editing": "Click mobile breakpoint in top bar -> adjust in Inspector",
                    "status": "Current flagship editor"
                },
                {
                    "name": "Editor X",
                    "description": "Legacy editor - being migrated to Wix Studio",
                    "indicators": [
                        "Similar to Studio but older UI",
                        "Grid-based layout system",
                        "Migration banner may appear"
                    ],
                    "key_features": [
                        "Responsive design with breakpoints",
                        "CSS Grid / Flexbox",
                        "Custom breakpoints",
                        "Velo integration"
                    ],
                    "mobile_editing": "Similar to Studio breakpoint workflow",
                    "status": "Legacy - migrate to Wix Studio"
                }
            ]
        }

    def get_ai_tools_summary(self) -> Dict[str, Any]:
        """Get Wix AI tools summary."""
        return {
            "ai_site_generator": {
                "location": "Create New Site -> AI Website Builder",
                "description": "Generates full site from text prompt",
                "note": "Produces starting point - customize after generation"
            },
            "ai_content_generator": {
                "location": "Blog/CMS/Product editor -> 'Write with AI'",
                "description": "Rewrites, extends, or changes tone of text",
                "note": "Always proofread before publishing"
            },
            "ai_image_generator": {
                "location": "Dashboard -> Media -> AI Image Generator",
                "description": "Text-to-image, 4 variations per prompt",
                "note": "Works best with specific, detailed prompts"
            },
            "ai_seo_assistant": {
                "location": "Dashboard -> Marketing -> AI SEO Tools",
                "description": "Generates meta tags, alt text, keywords"
            },
            "ai_email_generator": {
                "location": "Email Marketing -> Create -> Write with AI",
                "description": "Generates full email campaigns"
            },
            "ai_chatbot": {
                "location": "Inbox -> Chat Settings -> AI Assistant",
                "description": "Auto-reply to visitors from knowledge base"
            },
            "ai_automation_builder": {
                "location": "Automations -> Create with AI",
                "description": "Generates workflows from natural language"
            },
            "ai_translation": {
                "location": "Settings -> Multilingual -> Translate with AI",
                "description": "Auto-translates entire site (180+ languages)"
            },
            "availability": "All paid plans (some limitations on Free/entry plans)"
        }

    def get_escalation_guide(self) -> Dict[str, Any]:
        """Get escalation guide."""
        return {
            "escalate_to_wix_support": [
                "Account access issues (locked out, billing disputes, cannot log in)",
                "Platform bugs not fixable by user configuration (editor crashes, publish failures)",
                "Domain issues that DNS checking can't explain",
                "Data loss incidents",
                "Payment provider disputes involving Wix Payments",
                "DMCA/copyright claims against the site",
                "Site flagged or suspended by Wix"
            ],
            "support_channels": {
                "help_center": "support.wix.com",
                "live_chat": "Inside Wix dashboard (business hours)",
                "community_forum": "support.wix.com/en/forum",
                "studio_community": "Separate dedicated community for Studio users"
            }
        }


def validate_request(schema_name: str, data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Validate request against JSON schema (basic validation)."""
    errors = []

    if schema_name == "diagnose-request":
        if "editor" not in data:
            errors.append("Missing required field: editor")
        elif data["editor"] not in ["classic", "studio", "editorx"]:
            errors.append(f"Invalid editor: {data['editor']}. Must be: classic, studio, or editorx")
        if "issue" not in data:
            errors.append("Missing required field: issue")

    elif schema_name == "velo-check-request":
        if "element_id" not in data:
            errors.append("Missing required field: element_id")
        elif not data["element_id"].startswith("#"):
            errors.append("element_id must start with #")
        if "code" not in data:
            errors.append("Missing required field: code")

    elif schema_name == "cms-debug-request":
        if "collection" not in data:
            errors.append("Missing required field: collection")
        if "page_slug" not in data:
            errors.append("Missing required field: page_slug")

    elif schema_name == "dns-check-request":
        if "domain" not in data:
            errors.append("Missing required field: domain")

    return len(errors) == 0, errors


def validate_response(schema_name: str, data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Validate response against JSON schema (basic validation)."""
    errors = []

    # Add basic validation for each response type
    required_fields = {
        "diagnose-response": ["editor", "issue", "diagnosis", "steps", "reference_file", "confidence"],
        "velo-check-response": ["element_id", "code_provided", "issues_found", "suggestions", "reference_file", "template", "confidence"],
        "cms-debug-response": ["collection", "page_slug", "is_dynamic_item_page", "checks", "reference_file", "next_steps"],
        "dns-check-response": ["domain", "expected_records", "common_issues", "verification_url", "escalation_criteria", "reference_file"]
    }

    if schema_name in required_fields:
        for field in required_fields[schema_name]:
            if field not in data:
                errors.append(f"Missing required response field: {field}")

    return len(errors) == 0, errors