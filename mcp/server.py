"""MCP server exposing the interview study guides in resources/."""
from __future__ import annotations

from pathlib import Path

from fastmcp import FastMCP

RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"

mcp = FastMCP("interview-guides")


@mcp.tool()
def list_guides() -> list[str]:
    """Return the names of the available interview guides."""
    return [p.stem for p in sorted(RESOURCES_DIR.glob("*.md"))]


@mcp.tool()
def get_guide(name: str) -> str:
    """Return the full markdown content of one guide.

    Args:
        name: Guide name without the .md extension
              (e.g. "behavioral-star-guide").
    """
    path = RESOURCES_DIR / f"{name}.md"
    if not path.exists():
        available = ", ".join(p.stem for p in sorted(RESOURCES_DIR.glob("*.md")))
        raise ValueError(f"Guide '{name}' not found. Available: {available}")
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
