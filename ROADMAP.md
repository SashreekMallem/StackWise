# Project Roadmap: Building the AI Money Co-Pilot

This document outlines the strategic build order for the Smart Budget Optimizer AI. We will build features in the same logical order a user would interact with them, ensuring each new component has the necessary foundation.

---

### ✅ **Phase 1: Foundational Analysis Engine (Complete)**

The core engine for raw price analysis is complete.

*   **[✅ DONE] Real-time Price Fetching**: Implemented a robust fetcher for Google Shopping.
*   **[✅ DONE] Intelligent Unit Pricing**: Created a generic function to analyze price per gallon, pound, count, etc. [[memory:3909304]]
*   **[✅ DONE] Multi-Item Analysis**: Built an efficient endpoint (`/shopping_list_value`) to process entire lists concurrently.

---

### ✅ **Phase 2: Core User & AI Agent Inputs (Complete)**

The essential tools for a user (or AI agent) to input their data and intentions are complete.

*   **[✅ DONE] Budget Management**: Implemented the `set_budget` MCP tool.
*   **[✅ DONE] Distinct Shopping Lists**: Created separate in-memory `wishlist` and `groceries` lists.
*   **[✅ DONE] List Management Tools**: Implemented `add_to_wishlist` and `add_to_groceries` MCP tools.
*   **[✅ DONE] Holistic Analysis Tool**: Implemented the `analyze_all_lists` MCP tool that provides a categorized summary of the best shelf-price deals for both lists.

---

### ⏳ **Phase 3: The Stackable Smart Savings Engine (Current Focus)**

This is the next major development phase. We will build the "stack" layer by layer, making the AI's recommendations progressively smarter.

*   **[🔲 PENDING] Layer 1: Discounted Gift Cards**:
    *   Integrate with a gift card API (e.g., Raise, CardCash).
    *   Create a new internal function to check for gift card deals for a specific store.
    *   Upgrade the `analyze_all_lists` tool to include gift card savings in its final recommendation, calculating the *effective cost*.

*   **[🔲 PENDING] Layer 2: Digital Coupons & Promos**:
    *   Integrate with a coupon provider.
    *   Add coupon scanning to the analysis workflow.

*   **[_PENDING] Layer 3: Credit Card Perks**:
    *   Build a simple database of common credit card offers (e.g., "5% back on groceries").
    *   Allow the user to specify which cards they have.
    *   Incorporate these perks into the final effective cost calculation.

*   **[🔲 PENDING] Layer 4: Platform Cashback**:
    *   Integrate with affiliate cashback APIs like Rakuten.
    *   Complete the savings stack by adding this final layer.

---

### ⏳ **Phase 4: Full AI Co-Pilot & App Experience (Future)**

Once the savings engine is mature, we will focus on the end-user application and advanced AI features.

*   **[🔲 PENDING] Persistent Database**: Replace the in-memory lists with a proper database (e.g., SQLite, Supabase) to store user data permanently.
*   **[🔲 PENDING] User Interface (UI)**: Develop the front-end application (e.g., Flutter, React Native) for user interaction.
*   **[🔲 PENDING] Advanced AI Prompts**: Develop sophisticated prompts that allow the AI to perform "Live Budget Intelligence" and "Smart Purchase Sequencing" as described in the vision.
*   **[🔲 PENDING] Notifications & Alerts**: Implement the agent-driven alerts for price drops and deals.
*   **[🔲 PENDING] Budget Sync**: For a premium experience, integrate with Plaid to automate expense tracking. 