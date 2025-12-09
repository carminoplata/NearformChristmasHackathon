# Product Overview

Elf Agent is an AI-powered Christmas gift advisor that searches multiple online marketplaces (Amazon, Alibaba) to identify the best deals for Christmas gifts.

## Core Functionality

- Multi-marketplace search across Amazon and Alibaba for Christmas gifts
- Product feature analysis and gift suitability assessment using Google Search
- User confirmation workflow before executing searches
- Aggregation and ranking of deals by quality-to-price ratio and gift appropriateness
- Returns top gift deals with pricing, ratings, images, and URLs

## Agent Architecture

The system uses Google ADK (Agent Development Kit) with a hierarchical agent structure:
- **ElfAgent**: Root coordinator and Christmas gift advisor (built by `build_root_agent()`)
- **DirectorAgent**: Sequential workflow coordinator within ElfAgent
- **ProductSearchAgent**: Gathers product information and gift ideas via Google Search (built by `google_agent()`)
- **VerifierAgent**: Requests user confirmation before marketplace searches (built by `build_verification_agent()`)
- **MarketplaceAgent**: Coordinates and aggregates marketplace search results (built by `build_markeplace_agent()`)
- **MarketplaceSearchTeam**: Parallel agent that executes searches across multiple marketplaces
  - **amazon_agent**: Amazon marketplace search (built by `build_amazon_agent()`)
  - **AlibabaAgent**: Alibaba marketplace search (built by `build_alibaba_agent()`)

## Target Market

Italian market (IT locale, EUR currency) with support for Italian language.
