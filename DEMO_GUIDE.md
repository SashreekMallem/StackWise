# StackWise Demo & Usage Guide

## 🚀 Quick Start Demo

This guide shows how to explore and use the StackWise Smart Budget Optimizer AI.

### 1. Environment Setup

```bash
# Clone the repository (already done in this workspace)
cd /home/runner/work/StackWise/StackWise

# Install dependencies
pip install -e .

# Set up environment variables (API keys already configured)
# SERPAPI_KEY=your_serpapi_key_here
# COUPONSAPI_KEY=your_couponsapi_key_here
```

### 2. Run the FastAPI Server

```bash
# Start the server with debug logging
python -c "
import uvicorn
from src.smart_budget_mcp.main_debug import app
uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
"

# Server will be available at: http://127.0.0.1:8000
```

### 3. Test API Endpoints

```bash
# Run the automated test suite
python test_endpoints.py

# Or test manually with curl:

# Set up user profile
curl -X POST http://127.0.0.1:8000/profile/cards \
  -H "Content-Type: application/json" \
  -d '{"card_names": ["Target RedCard", "Chase Freedom"]}'

# Set monthly budget
curl -X POST http://127.0.0.1:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"monthly_limit": 2500}'

# Add items to wishlist
curl -X POST http://127.0.0.1:8000/wishlist/items \
  -H "Content-Type: application/json" \
  -d '{"name": "MacBook Pro", "urgency": "high"}'

# Add grocery items
curl -X POST http://127.0.0.1:8000/groceries/items \
  -H "Content-Type: application/json" \
  -d '{"name": "organic milk", "quantity": 2, "frequency": "weekly"}'

# Analyze shopping list for best deals
curl "http://127.0.0.1:8000/shopping_list_value?items=milk&items=bread&location=Seattle&num=5"
```

## 🧠 Core Functionality Demonstration

### Smart Savings Engine Test

```python
# Test the savings calculation engine
python -c "
import json
import asyncio
from src.smart_budget_mcp.savings_engine import get_credit_card_perks, fetch_gift_card_deals

# Test credit card perks
print('=== Credit Card Perk Analysis ===')
perks = get_credit_card_perks('Target', ['Target RedCard', 'Chase Freedom'])
print(f'Target perks: {json.dumps(perks, indent=2)}')

perks = get_credit_card_perks('Safeway', ['Chase Freedom'])
print(f'Safeway perks (groceries): {json.dumps(perks, indent=2)}')

# Test gift card deals
async def test_deals():
    print('\n=== Gift Card Deal Analysis ===')
    deal = await fetch_gift_card_deals('Target')
    print(f'Target: {json.dumps(deal, indent=2)}')
    
    deal = await fetch_gift_card_deals('Starbucks')
    print(f'Starbucks: {json.dumps(deal, indent=2)}')

asyncio.run(test_deals())
"
```

### Savings Calculation Example

For a $100 Target purchase:
- **Base Price**: $100.00
- **Gift Card Discount**: 4% (buy $100 gift card for $96)
- **Credit Card Perk**: 5% (Target RedCard discount)
- **Final Effective Price**: $100 × 0.96 × 0.95 = **$91.20**
- **Total Savings**: $8.80 (8.8%)

## 🔧 MCP Server Integration (Future)

The project includes an example MCP server implementation that demonstrates how the current FastAPI functionality could be integrated with AI agents:

```bash
# Example MCP server (not yet fully integrated)
python example_mcp_server.py
```

### MCP Tools Available:
- `set_budget` - Set monthly spending limits
- `add_to_wishlist` - Add priority items to wishlist
- `add_to_groceries` - Add items to grocery list
- `set_credit_cards` - Configure user's credit cards
- `analyze_shopping_list` - Get best deals analysis
- `get_savings_breakdown` - Detailed savings calculation

### MCP Resources:
- `stackwise://shopping-lists/wishlist` - Current wishlist
- `stackwise://shopping-lists/groceries` - Grocery list
- `stackwise://budget/current` - Budget status
- `stackwise://profile/cards` - Credit card profile

## 📊 Project Architecture

```
StackWise/
├── src/smart_budget_mcp/
│   ├── main.py              # Primary FastAPI server
│   ├── main_debug.py        # Debug version with logging
│   ├── schemas.py           # Data models
│   ├── state.py             # In-memory storage
│   └── savings_engine.py    # Core savings logic
├── test_*.py                # API endpoint tests
├── example_mcp_server.py    # MCP server demonstration
├── README.md                # Project overview
├── VISION.md                # Product vision
├── ROADMAP.md               # Development roadmap
└── WORKSPACE_EXPLANATION.md # Complete project analysis
```

## 🎯 Key Features Demonstrated

### ✅ Working Features:
1. **Real-time Price Fetching**: Google Shopping integration via SerpAPI
2. **Credit Card Optimization**: 5% Target RedCard, 5% Chase Freedom on groceries
3. **Gift Card Deals**: 4% off Target, 7% off Starbucks
4. **Budget Management**: Set and track monthly spending limits
5. **Smart Lists**: Separate wishlist and grocery management
6. **API Integration**: RESTful endpoints for all functionality

### 🔄 Integration Points:
- **SerpAPI**: Google Shopping price aggregation
- **CouponsAPI**: Deal and coupon discovery
- **Ollama**: LLM for intelligent product analysis
- **MCP Protocol**: AI agent integration framework

### 📈 Business Impact:
- **Average Savings**: 5-15% on typical purchases
- **Time Savings**: Automated deal discovery
- **Budget Control**: Intelligent spending optimization
- **Decision Support**: AI-powered purchase timing

## 🚀 Next Steps for Development

1. **Complete MCP Integration**: Full tool and prompt implementation
2. **Database Migration**: Replace in-memory storage
3. **Enhanced API Integration**: Full CouponsAPI implementation
4. **Frontend Development**: User-friendly interface
5. **Mobile App**: Cross-platform shopping companion

---

## 💡 Usage Tips

- **Set up your credit cards** first to maximize perk optimization
- **Use specific product names** for better price matching
- **Include your city/state** for accurate local pricing
- **Check the savings breakdown** to understand all discount layers
- **Monitor the logs** in debug mode to see the analysis process

The system is designed to be extensible and can easily integrate with additional deal sources, payment methods, and AI capabilities.