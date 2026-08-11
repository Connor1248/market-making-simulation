# Simple Limit Order Book & Market Maker Engine

A lightweight Python implementation of a Limit Order Book (LOB) engine with price-time priority matching and an inventory-aware Market Maker agent.

---

## Overview

* **`OrderBook`**: Handles bid and ask side order storage, sorting, spread calculation, and order matching for both market and limit orders.
* **`MarketMaker`**: Places two-sided quotes around a theoretical fair value, applying inventory skewing (`skew = 0.5 * inventory`) to manage directional risk and track cash/inventory fills.

---

## Key Components

### 1. OrderBook Engine
* **Order Sorting**: Automatically sorts bids in descending order and asks in ascending order.
* **Limit Order Matching**: Attempts to immediately cross resting liquidity on the opposite side before adding remaining unmatched quantity to the book.
* **Market Order Execution**: Sweeps available liquidity starting at the top of the book.

### 2. MarketMaker Strategy
* **Inventory Skewing**: Shifts bid and ask quotes downward when long inventory, and upward when short inventory, to incentivize risk-reducing trades.
* **Position Tracking**: Tracks real-time cash and asset inventory via `on_fill`.
