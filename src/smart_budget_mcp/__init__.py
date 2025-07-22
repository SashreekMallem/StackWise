# Removed import of main to prevent circular import issues.
# import asyncio

# def run_server():
#     """Main entry point for the package."""
#     import uvicorn
#     uvicorn.run(main.app, host="127.0.0.1", port=8000, reload=True)

# Optionally expose other important items at package level
__all__ = []