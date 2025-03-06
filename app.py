from typing import Any
from mcp.server.fastmcp import FastMCP
import asyncio
import shlex
from typing import Tuple

# Initialize FastMCP server
mcp = FastMCP("exec-cli")


@mcp.tool()
async def exec(cmd: str) -> str:
    """Run local cli commands

    Args:
        cmd: command to execute

    Returns:
        The stdout output of the command as a string

    Raises:
        RuntimeError: If the command fails with a non-zero exit code
    """
    # Use shlex to properly handle command arguments with spaces/quotes
    proc = await asyncio.create_subprocess_exec(
        *shlex.split(cmd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Wait for the command to complete and capture output
    stdout, stderr = await proc.communicate()

    # Check if the command executed successfully
    if proc.returncode != 0:
        error_msg = stderr.decode("utf-8").strip()
        raise RuntimeError(
            f"Command failed with exit code {proc.returncode}: {error_msg}"
        )

    # Return the stdout as a string
    return stdout.decode("utf-8").strip()


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
