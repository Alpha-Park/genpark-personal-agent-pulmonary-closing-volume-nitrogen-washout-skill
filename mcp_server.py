"""
MCP Server for Pulmonary Closing Volume & Nitrogen Washout Skill.
Exposes JSON-RPC Model Context Protocol tools for evaluating Closing Volume (CV), Closing Capacity (CC), and small airway patency.
"""

import sys
import json
from typing import Dict, Any
from client import PulmonaryClosingVolumeClient


def get_tools_manifest() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "evaluate_closing_volume",
                "description": "Calculates Single-Breath Nitrogen Washout (SBN2) Closing Volume (CV/VC %), Closing Capacity (CC/TLC %), Phase III slope, and small airway patency score.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "vital_capacity_l": {
                            "type": "number",
                            "description": "Slow or forced vital capacity in liters (e.g. 4.8 L)."
                        },
                        "closing_volume_l": {
                            "type": "number",
                            "description": "Phase IV closing volume in liters (e.g. 0.65 L)."
                        },
                        "residual_volume_l": {
                            "type": "number",
                            "description": "Residual volume in liters (e.g. 1.4 L)."
                        },
                        "phase3_slope_pct_n2_per_l": {
                            "type": "number",
                            "description": "Phase III alveolar plateau slope in %N2 per liter (normative 0.8 - 2.0 %N2/L, default: 1.2).",
                            "default": 1.2
                        },
                        "age_years": {
                            "type": "integer",
                            "description": "Subject age in years for calculating predicted CV/VC (default: 35).",
                            "default": 35
                        }
                    },
                    "required": ["vital_capacity_l", "closing_volume_l", "residual_volume_l"]
                }
            }
        ]
    }


def handle_request(client: PulmonaryClosingVolumeClient, req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": get_tools_manifest()
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "evaluate_closing_volume":
            res = client.evaluate_closing_volume(
                vital_capacity_l=float(args.get("vital_capacity_l", 4.5)),
                closing_volume_l=float(args.get("closing_volume_l", 0.6)),
                residual_volume_l=float(args.get("residual_volume_l", 1.4)),
                phase3_slope_pct_n2_per_l=float(args.get("phase3_slope_pct_n2_per_l", 1.2)),
                age_years=int(args.get("age_years", 35))
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {name}"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32600,
                "message": f"Invalid Request: Unsupported method {method}"
            }
        }


def main():
    client = PulmonaryClosingVolumeClient()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(client, req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error or exception: {str(e)}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
