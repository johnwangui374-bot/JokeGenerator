#!/usr/bin/env python3
"""
JokeGenerator: A fun random joke generator using multiple free APIs
Supports JokeAPI, Official Joke API, and Quotable API with caching.

Usage:
    python joke_generator.py [--source SOURCE] [--category CATEGORY] [--count N] [--cache] [--no-cache]
    
Examples:
    python joke_generator.py                           # Get a random joke
    python joke_generator.py --source jokeapi          # Use specific API
    python joke_generator.py --category programming   # Get programming jokes
    python joke_generator.py --count 5                 # Get 5 jokes
    python joke_generator.py --cache                   # Cache results
"""

import os
import sys
import json
import logging
import argparse
import requests
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import hashlib

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class JokeCache:
    """Simple file-based cache for jokes"""
    def __init__(self, cache_dir: Path = None, ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir or "./joke_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _hash_key(self, key: str) -> str:
        """Generate hash of cache key"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Dict]:
        """Retrieve from cache if valid"""
        cache_file = self.cache_dir / f"{self._hash_key(key)}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            # Check if expired
            cached_time = datetime.fromisoformat(data.get('timestamp'))
            if datetime.now() - cached_time > self.ttl:
                cache_file.unlink()  # Delete expired cache
                return None
            
            return data.get('value')
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
            return None
    
    def set(self, key: str, value: Dict) -> bool:
        """Store in cache"""
        cache_file = self.cache_dir / f"{self._hash_key(key)}.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'value': value
                }, f)
            return True
        except Exception as e:
            logger.warning(f"Cache write error: {e}")
            return False
    
    def clear(self) -> int:
        """Clear all cache files"""
        count = 0
        for cache_file in self.cache_dir.glob('*.json'):
            try:
                cache_file.unlink()
                count += 1
            except Exception as e:
                logger.warning(f"Failed to delete {cache_file}: {e}")
        return count

class JokeAPI:
    """Base class for joke APIs"""
    
    BASE_URLS = {
        'jokeapi': 'https://v2.jokeapi.dev/joke',
        'official': 'https://official-joke-api.appspot.com/jokes',
        'dad': 'https://icanhazdadjoke.com'
    }
    
    TIMEOUT = 10  # API timeout in seconds
    
    def __init__(self, cache: Optional[JokeCache] = None):
        self.cache = cache or JokeCache()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JokeGenerator/1.0 (Educational)'
        })
    
    def get_joke(self, source: str = 'jokeapi', category: Optional[str] = None) -> Optional[Dict]:
        """Get a joke from specified source"""
        
        # Check cache first
        cache_key = f"{source}:{category or 'random'}"
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached:
                logger.info("📦 Retrieved from cache")
                return cached
        
        # Fetch from API
        joke = None
        if source == 'jokeapi':
            joke = self._fetch_jokeapi(category)
        elif source == 'official':
            joke = self._fetch_official(category)
        elif source == 'dad':
            joke = self._fetch_dad_joke()
        else:
            logger.error(f"❌ Unknown source: {source}")
            return None
        
        # Cache the result
        if joke and self.cache:
            self.cache.set(cache_key, joke)
        
        return joke
    
    def _fetch_jokeapi(self, category: Optional[str] = None) -> Optional[Dict]:
        """Fetch from JokeAPI (v2.jokeapi.dev)"""
        try:
            logger.info(f"🔄 Fetching from JokeAPI (category: {category or 'any'})...")
            
            # JokeAPI supports: General, Knock-Knock, Programming, Miscellaneous, Dark, Spooky, Christmas
            if category:
                url = f"{self.BASE_URLS['jokeapi']}/{category}"
            else:
                url = f"{self.BASE_URLS['jokeapi']}/Any"
            
            response = self.session.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get('error'):
                logger.warning(f"⚠️  API error: {data.get('message')}")
                return None
            
            # Format response
            if data.get('type') == 'single':
                return {
                    'source': 'JokeAPI',
                    'category': data.get('category', 'General'),
                    'joke': data.get('joke'),
                    'type': 'single'
                }
            else:
                return {
                    'source': 'JokeAPI',
                    'category': data.get('category', 'General'),
                    'joke': f"{data.get('setup')}\n{data.get('delivery')}",
                    'type': 'two-part',
                    'setup': data.get('setup'),
                    'delivery': data.get('delivery')
                }
        
        except requests.exceptions.Timeout:
            logger.error("❌ JokeAPI request timed out")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ JokeAPI error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return None
    
    def _fetch_official(self, category: Optional[str] = None) -> Optional[Dict]:
        """Fetch from Official Joke API"""
        try:
            logger.info("🔄 Fetching from Official Joke API...")
            
            if category and category.lower() in ['programming', 'knock-knock', 'general']:
                url = f"{self.BASE_URLS['official']}/random"
            else:
                url = f"{self.BASE_URLS['official']}/random"
            
            response = self.session.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            return {
                'source': 'Official Joke API',
                'category': data.get('type', 'General'),
                'joke': f"{data.get('setup', '')}\n{data.get('punchline', '')}".strip(),
                'type': 'two-part',
                'setup': data.get('setup'),
                'punchline': data.get('punchline')
            }
        
        except requests.exceptions.Timeout:
            logger.error("❌ Official Joke API request timed out")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Official Joke API error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return None
    
    def _fetch_dad_joke(self) -> Optional[Dict]:
        """Fetch from icanhazdadjoke API"""
        try:
            logger.info("🔄 Fetching from Dad Jokes API...")
            
            response = self.session.get(
                self.BASE_URLS['dad'],
                headers={'Accept': 'application/json'},
                timeout=self.TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'source': 'Dad Jokes',
                'category': 'Dad Joke',
                'joke': data.get('joke'),
                'type': 'single',
                'id': data.get('id')
            }
        
        except requests.exceptions.Timeout:
            logger.error("❌ Dad Jokes API request timed out")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Dad Jokes API error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return None
    
    def get_multiple_jokes(self, count: int = 5, source: str = 'jokeapi') -> List[Dict]:
        """Get multiple jokes"""
        jokes = []
        for i in range(count):
            logger.info(f"\n[{i+1}/{count}]")
            joke = self.get_joke(source)
            if joke:
                jokes.append(joke)
            else:
                logger.warning(f"Failed to fetch joke {i+1}")
        return jokes
    
    def get_available_sources(self) -> List[str]:
        """List available joke sources"""
        return list(self.BASE_URLS.keys())
    
    def get_categories(self, source: str = 'jokeapi') -> List[str]:
        """Get available categories for a source"""
        categories = {
            'jokeapi': ['General', 'Knock-Knock', 'Programming', 'Miscellaneous', 'Dark', 'Spooky', 'Christmas'],
            'official': ['Programming', 'Knock-Knock', 'General'],
            'dad': ['Dad Joke']
        }
        return categories.get(source, [])

def format_joke_output(joke: Dict, index: int = 1) -> str:
    """Format joke for nice terminal output"""
    if not joke:
        return "❌ No joke available"
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"🎭 Joke #{index}")
    output.append(f"{'='*60}")
    output.append(f"Source: {joke.get('source', 'Unknown')}")
    output.append(f"Category: {joke.get('category', 'N/A')}")
    output.append(f"-" * 60)
    output.append(f"{joke.get('joke', 'N/A')}")
    output.append(f"{'='*60}\n")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description="🎭 JokeGenerator: Get random jokes from multiple APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Sources:
  jokeapi  - JokeAPI (v2.jokeapi.dev)
  official - Official Joke API
  dad      - icanhazdadjoke.com

JokeAPI Categories:
  General, Knock-Knock, Programming, Miscellaneous, Dark, Spooky, Christmas

Examples:
  python joke_generator.py
  python joke_generator.py --source jokeapi --category Programming
  python joke_generator.py --count 5
  python joke_generator.py --no-cache
  python joke_generator.py --list-sources
  python joke_generator.py --list-categories
  python joke_generator.py --clear-cache
        """
    )
    
    parser.add_argument(
        '--source',
        default='jokeapi',
        choices=['jokeapi', 'official', 'dad'],
        help='Joke API source (default: jokeapi)'
    )
    parser.add_argument(
        '--category',
        help='Joke category (JokeAPI only: General, Programming, Dark, etc.)'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of jokes to fetch (default: 1)'
    )
    parser.add_argument(
        '--cache',
        action='store_true',
        help='Enable caching (default: enabled)'
    )
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable caching'
    )
    parser.add_argument(
        '--list-sources',
        action='store_true',
        help='List available joke sources'
    )
    parser.add_argument(
        '--list-categories',
        action='store_true',
        help='List available categories for a source'
    )
    parser.add_argument(
        '--clear-cache',
        action='store_true',
        help='Clear all cached jokes'
    )
    parser.add_argument(
        '--cache-dir',
        default='./joke_cache',
        help='Cache directory (default: ./joke_cache)'
    )
    
    args = parser.parse_args()
    
    # Initialize cache
    use_cache = not args.no_cache
    cache = JokeCache(cache_dir=args.cache_dir) if use_cache else None
    
    # Initialize API
    api = JokeAPI(cache=cache)
    
    # Handle special commands
    if args.list_sources:
        logger.info("📚 Available Joke Sources:")
        for source in api.get_available_sources():
            logger.info(f"  • {source}")
        return
    
    if args.list_categories:
        categories = api.get_categories(args.source)
        logger.info(f"📂 Available Categories for '{args.source}':")
        for cat in categories:
            logger.info(f"  • {cat}")
        return
    
    if args.clear_cache:
        count = cache.clear() if cache else 0
        logger.info(f"🗑️  Cleared {count} cache files")
        return
    
    # Validate category for JokeAPI
    if args.source == 'jokeapi' and args.category:
        valid_cats = api.get_categories('jokeapi')
        if args.category.title() not in valid_cats:
            logger.warning(f"⚠️  Category '{args.category}' not found for JokeAPI")
            logger.info(f"Valid categories: {', '.join(valid_cats)}")
    
    # Get jokes
    logger.info(f"🎭 JokeGenerator Started (caching: {'enabled' if use_cache else 'disabled'})\n")
    
    if args.count == 1:
        joke = api.get_joke(source=args.source, category=args.category)
        if joke:
            print(format_joke_output(joke))
        else:
            logger.error("Failed to fetch joke")
            sys.exit(1)
    else:
        jokes = api.get_multiple_jokes(count=args.count, source=args.source)
        if not jokes:
            logger.error("Failed to fetch jokes")
            sys.exit(1)
        
        for idx, joke in enumerate(jokes, 1):
            print(format_joke_output(joke, idx))
        
        logger.info(f"✅ Successfully fetched {len(jokes)}/{args.count} jokes")

if __name__ == "__main__":
    main()
