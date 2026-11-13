import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
import re
from urllib.parse import urlencode, urlparse
import hashlib

logger = logging.getLogger(__name__)

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    aiohttp = None  # type: ignore
    AIOHTTP_AVAILABLE = False
    logger.warning("aiohttp not available — async web search disabled")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    logger.warning("BeautifulSoup not available - HTML parsing will be limited")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("Requests not available - fallback to aiohttp only")

@dataclass
class SearchResult:
    """Represents a single search result"""
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float
    timestamp: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DocumentationResult:
    """Represents a documentation lookup result"""
    title: str
    content: str
    url: str
    section: str
    api_version: Optional[str]
    last_updated: Optional[str]
    relevance_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class WebSearchIntegration:
    """Advanced web search and documentation lookup system"""
    
    def __init__(self, 
                 cache_duration_hours: int = 24,
                 max_results_per_query: int = 10,
                 timeout_seconds: int = 30):
        
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.max_results = max_results_per_query
        self.timeout = timeout_seconds
        
        # Search result cache
        self.search_cache = {}
        self.documentation_cache = {}
        
        # Search providers configuration
        self.search_providers = {
            'duckduckgo': self._search_duckduckgo,
            'bing': self._search_bing,
            'google_custom': self._search_google_custom,
            'academic': self._search_academic_sources
        }
        
        # Documentation sources
        self.documentation_sources = {
            'python': {
                'base_url': 'https://docs.python.org/3/',
                'search_endpoint': 'search.html',
                'api_patterns': [r'python\.org/3/library/', r'python\.org/3/reference/']
            },
            'tensorflow': {
                'base_url': 'https://www.tensorflow.org/api_docs/',
                'search_endpoint': 'python/tf',
                'api_patterns': [r'tensorflow\.org/api_docs/']
            },
            'pytorch': {
                'base_url': 'https://pytorch.org/docs/',
                'search_endpoint': 'stable/search.html',
                'api_patterns': [r'pytorch\.org/docs/']
            },
            'scikit_learn': {
                'base_url': 'https://scikit-learn.org/',
                'search_endpoint': 'stable/search.html',
                'api_patterns': [r'scikit-learn\.org/']
            }
        }
        
        # Rate limiting
        self.last_request_time = {}
        self.min_request_interval = 1.0  # seconds between requests
        
    async def comprehensive_search(self, 
                                 query: str,
                                 search_types: List[str] = None,
                                 include_documentation: bool = True,
                                 filter_domains: List[str] = None) -> Dict[str, Any]:
        """Perform comprehensive search across multiple sources"""
        
        if search_types is None:
            search_types = ['web', 'academic', 'documentation']
            
        logger.info(f"Starting comprehensive search for: {query}")
        
        # Check cache first
        cache_key = self._generate_cache_key(query, search_types)
        if cache_key in self.search_cache:
            cached_result = self.search_cache[cache_key]
            if datetime.now() - datetime.fromisoformat(cached_result['timestamp']) < self.cache_duration:
                logger.info("Returning cached search results")
                return cached_result
                
        search_results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'search_types': search_types,
            'results': {},
            'summary': {},
            'metadata': {}
        }
        
        # Perform different types of searches
        search_tasks = []
        
        if 'web' in search_types:
            search_tasks.append(self._perform_web_search(query, filter_domains))
            
        if 'academic' in search_types:
            search_tasks.append(self._perform_academic_search(query))
            
        if 'documentation' in search_types and include_documentation:
            search_tasks.append(self._perform_documentation_search(query))
            
        # Execute searches concurrently
        try:
            search_task_results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(search_task_results):
                if isinstance(result, Exception):
                    logger.error(f"Search task {i} failed: {result}")
                    continue
                    
                if i == 0 and 'web' in search_types:
                    search_results['results']['web'] = result
                elif i == 1 and 'academic' in search_types:
                    search_results['results']['academic'] = result
                elif i == 2 and 'documentation' in search_types:
                    search_results['results']['documentation'] = result
                    
        except Exception as e:
            logger.error(f"Search execution failed: {e}")
            search_results['error'] = str(e)
            
        # Generate summary and insights
        search_results['summary'] = self._generate_search_summary(search_results['results'])
        search_results['metadata'] = self._extract_search_metadata(search_results['results'])
        
        # Cache results
        self.search_cache[cache_key] = search_results
        
        return search_results
        
    async def _perform_web_search(self, query: str, filter_domains: List[str] = None) -> List[SearchResult]:
        """Perform web search using multiple providers"""
        
        all_results = []
        
        # Try different search providers
        for provider_name, provider_func in self.search_providers.items():
            if provider_name == 'academic':  # Skip academic in web search
                continue
                
            try:
                await self._rate_limit_check(provider_name)
                results = await provider_func(query)
                
                # Apply domain filtering if specified
                if filter_domains:
                    results = [r for r in results if any(domain in r.url for domain in filter_domains)]
                    
                all_results.extend(results)
                
            except Exception as e:
                logger.warning(f"Search provider {provider_name} failed: {e}")
                
        # Remove duplicates and sort by relevance
        unique_results = self._deduplicate_results(all_results)
        unique_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return unique_results[:self.max_results]
        
    async def _perform_academic_search(self, query: str) -> List[SearchResult]:
        """Perform academic/research-focused search"""
        
        try:
            await self._rate_limit_check('academic')
            return await self.search_providers['academic'](query)
        except Exception as e:
            logger.error(f"Academic search failed: {e}")
            return []
            
    async def _perform_documentation_search(self, query: str) -> List[DocumentationResult]:
        """Search through technical documentation"""
        
        all_docs = []
        
        # Search each documentation source
        for doc_name, doc_config in self.documentation_sources.items():
            try:
                docs = await self._search_documentation_source(query, doc_name, doc_config)
                all_docs.extend(docs)
            except Exception as e:
                logger.warning(f"Documentation search for {doc_name} failed: {e}")
                
        # Sort by relevance
        all_docs.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return all_docs[:self.max_results]
        
    async def _search_duckduckgo(self, query: str) -> List[SearchResult]:
        """Search using DuckDuckGo API"""
        if not AIOHTTP_AVAILABLE or aiohttp is None:
            logger.warning("aiohttp unavailable; skipping DuckDuckGo search")
            return []

        # DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_duckduckgo_results(data, query)
                else:
                    logger.warning(f"DuckDuckGo search failed with status {response.status}")
                    return []
                    
    async def _search_bing(self, query: str) -> List[SearchResult]:
        """Search using Bing Web Search API (requires API key)"""
        
        # Note: This would require a Bing API key in production
        # For demo purposes, return mock results
        
        mock_results = [
            SearchResult(
                title=f"Bing Result for {query}",
                url="https://example.com/bing-result",
                snippet=f"This is a mock Bing search result for the query: {query}",
                source="bing",
                relevance_score=0.8,
                timestamp=datetime.now().isoformat(),
                metadata={'provider': 'bing', 'mock': True}
            )
        ]
        
        return mock_results
        
    async def _search_google_custom(self, query: str) -> List[SearchResult]:
        """Search using Google Custom Search API (requires API key)"""
        
        # Note: This would require a Google Custom Search API key in production
        # For demo purposes, return mock results
        
        mock_results = [
            SearchResult(
                title=f"Google Result for {query}",
                url="https://example.com/google-result",
                snippet=f"This is a mock Google search result for the query: {query}",
                source="google",
                relevance_score=0.9,
                timestamp=datetime.now().isoformat(),
                metadata={'provider': 'google', 'mock': True}
            )
        ]
        
        return mock_results
        
    async def _search_academic_sources(self, query: str) -> List[SearchResult]:
        """Search academic and research sources"""
        
        # Academic sources to search
        academic_sources = [
            {
                'name': 'arXiv',
                'base_url': 'http://export.arxiv.org/api/query',
                'params': {'search_query': f'all:{query}', 'max_results': 5}
            },
            {
                'name': 'PubMed',
                'base_url': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
                'params': {'db': 'pubmed', 'term': query, 'retmax': 5, 'retmode': 'json'}
            }
        ]
        
        results = []
        if not AIOHTTP_AVAILABLE or aiohttp is None:
            logger.warning("aiohttp unavailable; skipping academic search")
            return results
        
        for source in academic_sources:
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                    async with session.get(source['base_url'], params=source['params']) as response:
                        if response.status == 200:
                            if source['name'] == 'arXiv':
                                content = await response.text()
                                results.extend(self._parse_arxiv_results(content, query))
                            elif source['name'] == 'PubMed':
                                data = await response.json()
                                results.extend(self._parse_pubmed_results(data, query))
                                
            except Exception as e:
                logger.warning(f"Academic source {source['name']} search failed: {e}")
                
        return results
        
    async def _search_documentation_source(self, 
                                         query: str, 
                                         doc_name: str, 
                                         doc_config: Dict[str, Any]) -> List[DocumentationResult]:
        """Search a specific documentation source"""
        
        # For demo purposes, return mock documentation results
        # In production, this would scrape or use APIs of documentation sites
        
        mock_docs = [
            DocumentationResult(
                title=f"{doc_name.title()} Documentation for {query}",
                content=f"This is mock documentation content for {query} in {doc_name}. "
                       f"It would contain detailed API information, examples, and usage patterns.",
                url=f"{doc_config['base_url']}/search?q={query}",
                section="API Reference",
                api_version="latest",
                last_updated=datetime.now().strftime('%Y-%m-%d'),
                relevance_score=0.85
            )
        ]
        
        return mock_docs
        
    def _parse_duckduckgo_results(self, data: Dict[str, Any], query: str) -> List[SearchResult]:
        """Parse DuckDuckGo API response"""
        
        results = []
        
        # Parse instant answer
        if data.get('Answer'):
            results.append(SearchResult(
                title="Instant Answer",
                url=data.get('AnswerURL', ''),
                snippet=data['Answer'],
                source="duckduckgo_instant",
                relevance_score=0.95,
                timestamp=datetime.now().isoformat(),
                metadata={'type': 'instant_answer'}
            ))
            
        # Parse related topics
        for topic in data.get('RelatedTopics', []):
            if isinstance(topic, dict) and 'Text' in topic:
                results.append(SearchResult(
                    title=topic.get('Text', '')[:50] + "...",
                    url=topic.get('FirstURL', ''),
                    snippet=topic.get('Text', ''),
                    source="duckduckgo_related",
                    relevance_score=0.7,
                    timestamp=datetime.now().isoformat(),
                    metadata={'type': 'related_topic'}
                ))
                
        return results
        
    def _parse_arxiv_results(self, xml_content: str, query: str) -> List[SearchResult]:
        """Parse arXiv API XML response"""
        
        results = []
        
        if not BS4_AVAILABLE:
            return results
            
        try:
            soup = BeautifulSoup(xml_content, 'xml')
            entries = soup.find_all('entry')
            
            for entry in entries:
                title = entry.find('title').text.strip() if entry.find('title') else 'No title'
                summary = entry.find('summary').text.strip() if entry.find('summary') else 'No summary'
                link = entry.find('id').text.strip() if entry.find('id') else ''
                
                results.append(SearchResult(
                    title=title,
                    url=link,
                    snippet=summary[:200] + "..." if len(summary) > 200 else summary,
                    source="arxiv",
                    relevance_score=0.8,
                    timestamp=datetime.now().isoformat(),
                    metadata={'type': 'academic_paper'}
                ))
                
        except Exception as e:
            logger.warning(f"Failed to parse arXiv results: {e}")
            
        return results
        
    def _parse_pubmed_results(self, data: Dict[str, Any], query: str) -> List[SearchResult]:
        """Parse PubMed API JSON response"""
        
        results = []
        
        try:
            if 'esearchresult' in data and 'idlist' in data['esearchresult']:
                for pmid in data['esearchresult']['idlist'][:5]:  # Limit to 5 results
                    results.append(SearchResult(
                        title=f"PubMed Article {pmid}",
                        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        snippet=f"Medical research article related to {query}",
                        source="pubmed",
                        relevance_score=0.75,
                        timestamp=datetime.now().isoformat(),
                        metadata={'pmid': pmid, 'type': 'medical_research'}
                    ))
                    
        except Exception as e:
            logger.warning(f"Failed to parse PubMed results: {e}")
            
        return results
        
    def _deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Remove duplicate search results"""
        
        seen_urls = set()
        unique_results = []
        
        for result in results:
            # Normalize URL for comparison
            normalized_url = result.url.lower().rstrip('/')
            
            if normalized_url not in seen_urls:
                seen_urls.add(normalized_url)
                unique_results.append(result)
                
        return unique_results
        
    def _generate_search_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of search results"""
        
        summary = {
            'total_results': 0,
            'sources': [],
            'top_domains': [],
            'content_types': {},
            'average_relevance': 0.0
        }
        
        all_results = []
        
        # Collect all results
        for search_type, type_results in results.items():
            if isinstance(type_results, list):
                all_results.extend(type_results)
                summary['sources'].append(search_type)
                
        summary['total_results'] = len(all_results)
        
        if all_results:
            # Extract domains
            domains = []
            relevance_scores = []
            content_types = {}
            
            for result in all_results:
                if hasattr(result, 'url') and result.url:
                    domain = urlparse(result.url).netloc
                    domains.append(domain)
                    
                if hasattr(result, 'relevance_score'):
                    relevance_scores.append(result.relevance_score)
                    
                if hasattr(result, 'metadata') and 'type' in result.metadata:
                    content_type = result.metadata['type']
                    content_types[content_type] = content_types.get(content_type, 0) + 1
                    
            # Top domains
            from collections import Counter
            domain_counts = Counter(domains)
            summary['top_domains'] = [domain for domain, count in domain_counts.most_common(5)]
            
            # Average relevance
            if relevance_scores:
                summary['average_relevance'] = sum(relevance_scores) / len(relevance_scores)
                
            summary['content_types'] = content_types
            
        return summary
        
    def _extract_search_metadata(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from search results"""
        
        metadata = {
            'search_providers_used': [],
            'documentation_sources': [],
            'academic_sources': [],
            'total_processing_time': 0.0,
            'cache_hits': 0,
            'api_calls_made': 0
        }
        
        # Extract provider information
        for search_type, type_results in results.items():
            if isinstance(type_results, list):
                for result in type_results:
                    if hasattr(result, 'source'):
                        if search_type == 'web':
                            if result.source not in metadata['search_providers_used']:
                                metadata['search_providers_used'].append(result.source)
                        elif search_type == 'documentation':
                            if result.source not in metadata['documentation_sources']:
                                metadata['documentation_sources'].append(result.source)
                        elif search_type == 'academic':
                            if result.source not in metadata['academic_sources']:
                                metadata['academic_sources'].append(result.source)
                                
        return metadata
        
    async def _rate_limit_check(self, provider: str):
        """Check and enforce rate limiting"""
        
        current_time = time.time()
        
        if provider in self.last_request_time:
            time_since_last = current_time - self.last_request_time[provider]
            if time_since_last < self.min_request_interval:
                sleep_time = self.min_request_interval - time_since_last
                await asyncio.sleep(sleep_time)
                
        self.last_request_time[provider] = time.time()
        
    def _generate_cache_key(self, query: str, search_types: List[str]) -> str:
        """Generate cache key for search results"""
        
        key_data = f"{query}_{sorted(search_types)}"
        return hashlib.md5(key_data.encode()).hexdigest()
        
    async def get_real_time_data(self, topic: str, data_type: str = "general") -> Dict[str, Any]:
        """Get real-time data for specific topics"""
        
        data_sources = {
            'financial': self._get_financial_data,
            'weather': self._get_weather_data,
            'news': self._get_news_data,
            'technology': self._get_tech_data,
            'general': self._get_general_data
        }
        
        if data_type in data_sources:
            try:
                return await data_sources[data_type](topic)
            except Exception as e:
                logger.error(f"Failed to get real-time data for {data_type}: {e}")
                return {'error': str(e)}
        else:
            return {'error': f"Unknown data type: {data_type}"}
            
    async def _get_financial_data(self, symbol: str) -> Dict[str, Any]:
        """Get real-time financial data (mock implementation)"""
        
        # In production, this would use APIs like Alpha Vantage, Yahoo Finance, etc.
        import random
        
        return {
            'symbol': symbol.upper(),
            'price': round(random.uniform(50, 500), 2),
            'change': round(random.uniform(-10, 10), 2),
            'change_percent': round(random.uniform(-5, 5), 2),
            'volume': random.randint(100000, 10000000),
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_financial_api'
        }
        
    async def _get_weather_data(self, location: str) -> Dict[str, Any]:
        """Get real-time weather data (mock implementation)"""
        
        # In production, this would use APIs like OpenWeatherMap
        import random
        
        return {
            'location': location,
            'temperature': random.randint(-10, 40),
            'humidity': random.randint(30, 90),
            'conditions': random.choice(['sunny', 'cloudy', 'rainy', 'snowy']),
            'wind_speed': random.randint(0, 30),
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_weather_api'
        }
        
    async def _get_news_data(self, topic: str) -> Dict[str, Any]:
        """Get real-time news data (mock implementation)"""
        
        # In production, this would use APIs like NewsAPI
        return {
            'topic': topic,
            'headlines': [
                f"Breaking: Latest developments in {topic}",
                f"Analysis: {topic} trends and implications",
                f"Expert opinion on {topic} situation"
            ],
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_news_api'
        }
        
    async def _get_tech_data(self, technology: str) -> Dict[str, Any]:
        """Get real-time technology data (mock implementation)"""
        
        return {
            'technology': technology,
            'latest_version': '2.1.0',
            'release_date': '2024-01-15',
            'github_stars': random.randint(1000, 50000),
            'issues_open': random.randint(10, 500),
            'last_commit': '2 hours ago',
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_tech_api'
        }
        
    async def _get_general_data(self, topic: str) -> Dict[str, Any]:
        """Get general real-time data"""
        
        return {
            'topic': topic,
            'data': f"Real-time information about {topic}",
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_general_api'
        }
        
    def clear_cache(self):
        """Clear search and documentation caches"""
        self.search_cache.clear()
        self.documentation_cache.clear()
        logger.info("Search caches cleared")
        
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'search_cache_size': len(self.search_cache),
            'documentation_cache_size': len(self.documentation_cache),
            'cache_duration_hours': self.cache_duration.total_seconds() / 3600,
            'oldest_cache_entry': min(
                [datetime.fromisoformat(entry['timestamp']) for entry in self.search_cache.values()],
                default=datetime.now()
            ).isoformat()
        }

# Example usage
async def main():
    """Example usage of web search integration"""
    
    search_integration = WebSearchIntegration()
    
    # Perform comprehensive search
    results = await search_integration.comprehensive_search(
        query="machine learning performance optimization",
        search_types=['web', 'academic', 'documentation'],
        include_documentation=True
    )
    
    print(json.dumps(results, indent=2, default=str))
    
    # Get real-time data
    financial_data = await search_integration.get_real_time_data("AAPL", "financial")
    print(json.dumps(financial_data, indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 