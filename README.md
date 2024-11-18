# Italian Restaurant Finder

**Italian Restaurant Finder** is a Python-based web scraping and search engine project designed to discover, collect, and explore restaurant data from the Michelin Guide website. This repository includes tools for web scraping, data extraction, preprocessing, and implementing a search engine with features like conjunctive search and ranking using TF-IDF and cosine similarity.

---

## Features

### 1. **Web Scraping**
- Collects restaurant data (name, address, cuisine, price range, etc.) from the Michelin Guide website.
- Saves restaurant web pages for offline processing.

### 2. **Data Extraction**
- Extracts structured information like:
  - Restaurant name
  - Address, city, postal code, and country
  - Description, facilities, and services
  - Accepted credit cards
  - Contact details (phone and website)

### 3. **Search Engine**
- Supports two types of searches:
  - **Conjunctive Search:** Returns restaurants matching all terms in the query.
  - **Ranked Search:** Uses TF-IDF and cosine similarity to rank results based on relevance to the query.

### 4. **Text Preprocessing**
- Includes functions for cleaning and processing text:
  - Tokenization, stopword removal, stemming
  - Building vocabularies and inverted indices for fast search operations.
