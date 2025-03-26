"""
Tools for searching external knowledge sources like arXiv and DuckDuckGo.
"""

from typing import Dict, List
import os
import json
import logging
import arxiv
from datetime import datetime
from duckduckgo_search import DDGS


# ------------------------------------------------------------------------------
# Configure Logging
# ------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search Arxiv for papers and return the results including abstracts.
    
    Args:
        query (str): Search query for academic papers. Should include relevant geological terms,
                    formation names, or CO2 storage concepts for better results.
        max_results (int): Maximum number of results to return.
        
    Returns:
        List[Dict]: List of relevant papers with metadata.
    """
    logger.info(f"Searching Arxiv for: {query}")
    
    try:
        client = arxiv.Client(num_retries=3, delay_seconds=3)
        search = arxiv.Search(
            query=query, 
            max_results=max_results, 
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for paper in client.results(search):
            try:
                paper_data = {
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "published": paper.published.strftime("%Y-%m-%d"),
                    "abstract": paper.summary,
                    "pdf_url": paper.pdf_url,
                    "categories": paper.categories,
                    "relevance_score": _calculate_relevance_score(query, paper.title, paper.summary)
                }
                results.append(paper_data)
            except Exception as e:
                logger.error(f"Error processing paper: {e}")
                continue
                
        # Sort by relevance score
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return results
        
    except Exception as e:
        logger.error(f"Arxiv search failed: {e}")
        return [{"error": f"Search failed: {str(e)}"}]

def _calculate_relevance_score(query: str, title: str, abstract: str) -> float:
    """Calculate a simple relevance score based on keyword matches"""
    score = 0
    query_terms = set(query.lower().split())
    
    # Check title (higher weight)
    for term in query_terms:
        if term in title.lower():
            score += 2
            
    # Check abstract
    for term in query_terms:
        if term in abstract.lower():
            score += 1
            
    return score

def internet_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Perform an Internet search using DuckDuckGo with improved robustness.
    
    Args:
        query (str): The search query string. Should include specific geological terms,
                    formation names, or CO2 storage concepts for better results.
        max_results (int): Maximum number of results to return.
        
    Returns:
        List[Dict]: List of search results containing title, URL, and snippet.
    """
    logger.info(f"Searching internet for: {query}")
    
    try:
        ddgs = DDGS()
        results = []
        
        # Add specific CO2 storage related terms to improve search relevance
        enhanced_query = f"{query} CO2 storage reservoir characterization"
        
        for result in ddgs.text(keywords=enhanced_query, max_results=max_results):
            try:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", ""),
                    "relevance_score": _calculate_web_relevance(query, result.get("title", ""), result.get("body", ""))
                })
            except Exception as e:
                logger.warning(f"Error processing search result: {e}")
                continue
                
        # Sort results by relevance
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return results
        
    except Exception as e:
        logger.error(f"Internet search failed: {e}")
        return [{"error": f"Search failed: {str(e)}"}]

def _calculate_web_relevance(query: str, title: str, snippet: str) -> float:
    """Calculate relevance score for web search results"""
    score = 0
    co2_storage_terms = ["co2", "carbon", "storage", "sequestration", "reservoir", "porosity", 
                        "permeability", "cap rock", "formation", "injection", "geological"]
    
    # Check for query terms
    query_terms = query.lower().split()
    for term in query_terms:
        if term in title.lower():
            score += 3
        if term in snippet.lower():
            score += 1
            
    # Bonus for CO2 storage specific terms
    for term in co2_storage_terms:
        if term in title.lower():
            score += 2
        if term in snippet.lower():
            score += 0.5
            
    return score