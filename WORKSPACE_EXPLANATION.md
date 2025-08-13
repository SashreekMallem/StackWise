# StackWise: Smart Budget Optimizer AI - Complete Workspace Explanation

## 🎯 What is StackWise?

**StackWise** is an advanced AI-powered budget optimization platform designed to help users make intelligent purchase decisions by aggregating prices, finding deals, and optimizing savings across multiple sources. The project uses the **Model Context Protocol (MCP)** for AI agent integrations to provide smart purchase planning and automated deal discovery.

## 🏗️ Project Architecture

### Core Components

```
src/smart_budget_mcp/
├── __init__.py           # Package initialization
├── main.py              # Primary FastAPI server with full features
├── main_debug.py        # Debug version with enhanced logging
├── schemas.py           # Pydantic data models for API
├── state.py             # In-memory data storage (wishlist, groceries, budget)
└── savings_engine.py    # Core savings calculation logic
```

### Key Technologies

- **FastAPI**: Modern web framework for API endpoints
- **MCP (Model Context Protocol)**: AI agent integration framework
- **SerpAPI**: Google Shopping price data aggregation
- **CouponsAPI**: Coupon and deal discovery
- **Ollama**: Local LLM for intelligent product analysis
- **Pydantic**: Data validation and serialization
- **Python-dotenv**: Environment configuration management

## 🚀 Core Features

### 1. Price Aggregation & Analysis
- **Real-time price fetching** from Google Shopping via SerpAPI
- **Location-aware results** to find nearby store prices
- **Intelligent unit price calculation** using LLM to extract quantities from product titles
- **Multi-store comparison** with delivery options and product details

### 2. Smart Savings Engine (Layered Approach)
- **Layer 1**: Discounted gift cards (4-7% savings on major retailers)
- **Layer 2**: Digital coupons and promotional deals
- **Layer 3**: Credit card perks and cashback optimization
- **Layer 4**: Platform-specific cashback (Rakuten, Honey integration planned)

### 3. Budget & List Management
- **Monthly budget tracking** with spending limits
- **Dual shopping lists**: Separate wishlist and grocery management
- **Item categorization** with urgency levels and frequency tracking
- **User profile management** including credit card optimization

### 4. AI-Powered Intelligence
- **LLM quantity extraction**: Automatically parses "2-pack", "gallon", "12 oz" from titles
- **Smart unit comparisons**: Price per gallon, pound, ounce, or count
- **Effective price calculation**: Final cost after all savings layers applied

## 📊 API Endpoints

### Budget Management
- `POST /budget` - Set monthly spending limit
- `POST /profile/cards` - Configure user's credit cards for perk optimization

### Shopping Lists
- `POST /wishlist/items` - Add items to wishlist with urgency levels
- `POST /groceries/items` - Add grocery items with quantity and frequency

### Price Analysis
- `GET /shopping_list_value` - Analyze entire shopping list for best deals
- `GET /store_coupons_deals` - Get coupons and deals for specific stores

## 🔧 Development Status

### ✅ Completed Features
- [x] Real-time price fetching via Google Shopping
- [x] Intelligent unit pricing with LLM extraction
- [x] Multi-item concurrent analysis
- [x] Budget management system
- [x] Dual shopping list management (wishlist + groceries)
- [x] Credit card perk integration
- [x] Gift card discount application
- [x] FastAPI REST endpoints

### ⏳ In Progress
- [ ] Full MCP server implementation (structure exists, needs tools/prompts)
- [ ] CouponsAPI integration completion
- [ ] Persistent database storage (currently in-memory)

### 🔮 Planned Features
- [ ] Advanced AI co-pilot with purchase timing recommendations
- [ ] Historical price tracking and trend analysis
- [ ] Mobile/web frontend application
- [ ] Bank account integration via Plaid
- [ ] Notification system for price drops and deals

## 🛠️ Setup & Usage

### Prerequisites
```bash
# Required API keys (add to .env file)
SERPAPI_KEY=your_serpapi_key_here
COUPONSAPI_KEY=your_couponsapi_key_here
```

### Installation
```bash
# Install dependencies
pip install -e .

# Run the FastAPI server
python -m src.smart_budget_mcp.server
# Server available at: http://localhost:8080
```

### Example Usage

1. **Set up user profile**:
```bash
curl -X POST http://localhost:8080/profile/cards \
  -H "Content-Type: application/json" \
  -d '{"card_names": ["Target RedCard", "Chase Freedom"]}'

curl -X POST http://localhost:8080/budget \
  -H "Content-Type: application/json" \
  -d '{"monthly_limit": 2500}'
```

2. **Add items to shopping lists**:
```bash
curl -X POST http://localhost:8080/wishlist/items \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone 15", "urgency": "high"}'

curl -X POST http://localhost:8080/groceries/items \
  -H "Content-Type: application/json" \
  -d '{"name": "milk", "quantity": 2, "frequency": "weekly"}'
```

3. **Analyze shopping list for best deals**:
```bash
curl "http://localhost:8080/shopping_list_value?items=milk&items=coffee&location=Seattle&num=5"
```

## 💡 How the Savings Engine Works

The system analyzes each product offer through multiple discount layers:

1. **Base Price**: Raw price from Google Shopping
2. **Gift Card Discount**: 4-7% savings for supported retailers
3. **Credit Card Perks**: Category-specific cashback (5% groceries, etc.)
4. **Final Effective Price**: Base × (1 - gift_card_discount) × (1 - credit_card_perk)

### Example Calculation
```
Base Price: $100 Target item
Gift Card Discount: 4% (buy $100 Target gift card for $96)
Credit Card Perk: 5% (Target RedCard discount)
Final Price: $100 × 0.96 × 0.95 = $91.20
Total Savings: $8.80 (8.8%)
```

## 🏢 Business Model & Vision

### Target Problem
- Users overspend without realizing optimal purchase timing
- Missed deals, cashback opportunities, and card-specific offers
- Lack of intelligent price comparison across stores
- No unified system for purchase planning and budget optimization

### Solution Approach
- **AI-powered purchase timing**: "Buy now or wait? Here's why."
- **Stackable savings optimization**: Combine gift cards, coupons, credit perks
- **Smart budget sequencing**: Optimal order for large purchases
- **Automated deal monitoring**: AI agents track prices and notify users

### Monetization Strategy
- **Affiliate revenue**: Cashback clicks, gift card purchases
- **Premium subscriptions**: Advanced AI features, deeper insights
- **Partner integrations**: Co-branded rewards with retailers/banks
- **Enterprise licensing**: White-label for financial institutions

## 🔐 Security & Privacy

- **API key management**: Secure environment variable storage
- **User data**: Currently in-memory (production will use encrypted databases)
- **External integrations**: Read-only price/deal data, no financial account access
- **Optional bank sync**: Premium feature via Plaid with user consent

## 🚀 Next Development Priorities

1. **Complete MCP Integration**: Full AI agent tool/prompt implementation
2. **Database Migration**: Replace in-memory storage with SQLite/PostgreSQL
3. **Enhanced Coupon Integration**: Full CouponsAPI implementation
4. **Testing Suite**: Comprehensive unit and integration tests
5. **Frontend Development**: User-friendly web/mobile interface

---

## 🤝 Contributing

The project follows modern Python development practices:
- **Type hints**: Full Pydantic model validation
- **Async/await**: Non-blocking I/O for external API calls
- **Modular design**: Clear separation of concerns
- **Environment configuration**: Secure API key management
- **Comprehensive logging**: Debug-friendly development experience

This workspace represents a sophisticated approach to AI-powered financial optimization, combining multiple external data sources with intelligent analysis to help users make better purchasing decisions.