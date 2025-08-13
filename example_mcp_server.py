#!/usr/bin/env python3
"""
Example MCP Server implementation for StackWise Smart Budget Optimizer

This demonstrates how the current FastAPI functionality could be integrated
into a proper MCP server for AI agent interactions.
"""

import asyncio
import logging
from typing import Any, Sequence

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource

from src.smart_budget_mcp.state import wishlist, groceries, budget, user_profile
from src.smart_budget_mcp.savings_engine import get_credit_card_perks, fetch_gift_card_deals

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stackwise-mcp-server")

server = Server("stackwise-mcp-server")

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """
    List available resources for the AI agent to access.
    """
    return [
        Resource(
            uri="stackwise://shopping-lists/wishlist",
            name="User Wishlist",
            description="Current user wishlist with priority items",
            mimeType="application/json",
        ),
        Resource(
            uri="stackwise://shopping-lists/groceries",
            name="Grocery List",
            description="Current grocery shopping list with quantities and frequencies",
            mimeType="application/json",
        ),
        Resource(
            uri="stackwise://budget/current",
            name="Budget Status",
            description="Current budget limits, spending, and financial status",
            mimeType="application/json",
        ),
        Resource(
            uri="stackwise://profile/cards",
            name="Credit Card Profile",
            description="User's credit cards for optimizing cashback and perks",
            mimeType="application/json",
        ),
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """
    Read resource content for AI agent consumption.
    """
    import json
    
    if uri == "stackwise://shopping-lists/wishlist":
        return json.dumps({
            "type": "wishlist",
            "items": wishlist,
            "count": len(wishlist)
        }, indent=2)
    elif uri == "stackwise://shopping-lists/groceries":
        return json.dumps({
            "type": "groceries",
            "items": groceries,
            "count": len(groceries)
        }, indent=2)
    elif uri == "stackwise://budget/current":
        return json.dumps({
            "type": "budget",
            "monthly_limit": budget["monthly_limit"],
            "spent": budget["spent"],
            "remaining": budget["monthly_limit"] - budget["spent"],
            "history": budget["history"]
        }, indent=2)
    elif uri == "stackwise://profile/cards":
        return json.dumps({
            "type": "user_profile",
            "credit_cards": user_profile["credit_cards"],
            "card_count": len(user_profile["credit_cards"])
        }, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools for the AI agent to use.
    """
    return [
        Tool(
            name="set_budget",
            description="Set the user's monthly budget limit",
            inputSchema={
                "type": "object",
                "properties": {
                    "monthly_limit": {
                        "type": "number",
                        "description": "Monthly budget limit in dollars",
                    },
                },
                "required": ["monthly_limit"],
            },
        ),
        Tool(
            name="add_to_wishlist",
            description="Add an item to the user's wishlist",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the item to add",
                    },
                    "urgency": {
                        "type": "string",
                        "description": "Urgency level: low, medium, high",
                        "enum": ["low", "medium", "high"],
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="add_to_groceries",
            description="Add an item to the grocery shopping list",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the grocery item",
                    },
                    "quantity": {
                        "type": "number",
                        "description": "Quantity needed",
                        "default": 1,
                    },
                    "frequency": {
                        "type": "string",
                        "description": "How often this item is needed",
                        "enum": ["daily", "weekly", "monthly"],
                        "default": "weekly",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="set_credit_cards",
            description="Set the user's credit cards for perk optimization",
            inputSchema={
                "type": "object",
                "properties": {
                    "card_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of credit card names the user has",
                    },
                },
                "required": ["card_names"],
            },
        ),
        Tool(
            name="analyze_shopping_list",
            description="Analyze shopping list items for best deals and savings",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of items to analyze for best deals",
                    },
                    "location": {
                        "type": "string",
                        "description": "Location to search for nearby stores (city, state)",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Maximum number of offers to analyze per item",
                        "default": 10,
                    },
                },
                "required": ["items", "location"],
            },
        ),
        Tool(
            name="get_savings_breakdown",
            description="Get detailed savings breakdown for a specific store and user's cards",
            inputSchema={
                "type": "object",
                "properties": {
                    "store_name": {
                        "type": "string",
                        "description": "Name of the store to check for savings",
                    },
                },
                "required": ["store_name"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """
    Execute tool calls from the AI agent.
    """
    import json
    
    if name == "set_budget":
        monthly_limit = arguments["monthly_limit"]
        budget["monthly_limit"] = monthly_limit
        return [
            TextContent(
                type="text",
                text=f"Budget successfully set to ${monthly_limit} per month. Current remaining: ${monthly_limit - budget['spent']}"
            )
        ]
    
    elif name == "add_to_wishlist":
        name_item = arguments["name"]
        urgency = arguments.get("urgency", "medium")
        wishlist.append({"name": name_item, "urgency": urgency})
        return [
            TextContent(
                type="text",
                text=f"Added '{name_item}' to wishlist with urgency: {urgency}. Total wishlist items: {len(wishlist)}"
            )
        ]
    
    elif name == "add_to_groceries":
        name_item = arguments["name"]
        quantity = arguments.get("quantity", 1)
        frequency = arguments.get("frequency", "weekly")
        groceries.append({"name": name_item, "quantity": quantity, "frequency": frequency})
        return [
            TextContent(
                type="text",
                text=f"Added {quantity}x '{name_item}' to grocery list (frequency: {frequency}). Total grocery items: {len(groceries)}"
            )
        ]
    
    elif name == "set_credit_cards":
        card_names = arguments["card_names"]
        user_profile["credit_cards"] = card_names
        return [
            TextContent(
                type="text",
                text=f"Credit cards updated: {', '.join(card_names)}. This will be used for perk optimization."
            )
        ]
    
    elif name == "analyze_shopping_list":
        items = arguments["items"]
        location = arguments["location"]
        max_results = arguments.get("max_results", 10)
        
        # This would call the actual analysis function
        # For demo purposes, we'll show what the analysis would include
        analysis_summary = {
            "location": location,
            "items_analyzed": len(items),
            "items": items,
            "max_results_per_item": max_results,
            "analysis_includes": [
                "Real-time prices from Google Shopping",
                "Gift card discount opportunities",
                "Credit card perk optimization",
                "Unit price calculations (per lb, gallon, etc.)",
                "Effective final prices after all savings"
            ]
        }
        
        return [
            TextContent(
                type="text",
                text=f"Shopping list analysis initiated for {len(items)} items in {location}:\n\n" +
                     json.dumps(analysis_summary, indent=2) +
                     "\n\nNote: This is a demo response. In production, this would return actual price data and savings recommendations."
            )
        ]
    
    elif name == "get_savings_breakdown":
        store_name = arguments["store_name"]
        
        # Get credit card perks for this store
        perks = get_credit_card_perks(store_name, user_profile["credit_cards"])
        
        # Get gift card deals
        gift_card_deal = await fetch_gift_card_deals(store_name)
        
        breakdown = {
            "store": store_name,
            "credit_card_perks": perks,
            "gift_card_deal": gift_card_deal,
            "user_cards": user_profile["credit_cards"]
        }
        
        return [
            TextContent(
                type="text",
                text=f"Savings breakdown for {store_name}:\n\n" +
                     json.dumps(breakdown, indent=2)
            )
        ]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """
    Main entry point for the MCP server.
    """
    # Run the server using stdio
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="stackwise-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())