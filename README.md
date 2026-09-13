# 🎭 JokeGenerator

**A fun and simple random joke generator using multiple free external APIs**

Fetch random jokes from 3 different free APIs with built-in caching, CLI options, and error handling.

## ✨ Features

✅ **Multiple API Sources**
  - JokeAPI (v2.jokeapi.dev) - 7 categories, 100+ jokes
  - Official Joke API - Programming, Knock-Knock, General
  - Dad Jokes API (icanhazdadjoke.com) - Classic dad jokes

✅ **Smart Caching** - Cache results locally for faster subsequent requests
✅ **Category Support** - Filter jokes by category (Programming, Dark, Spooky, etc.)
✅ **Batch Mode** - Fetch multiple jokes at once
✅ **Error Handling** - Graceful fallbacks and timeout handling
✅ **Clean CLI** - Easy-to-use command-line interface
✅ **Free & Open Source** - No API keys required, MIT Licensed

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/johnwangui374-bot/JokeGenerator.git
cd JokeGenerator
pip install -r requirements.txt
```

### 2. Run

```bash
# Get a random joke
python joke_generator.py

# Get a programming joke
python joke_generator.py --source jokeapi --category Programming

# Get 5 random jokes
python joke_generator.py --count 5

# Use Dad Jokes API
python joke_generator.py --source dad

# Disable caching
python joke_generator.py --no-cache
```

## 📖 Usage

### Basic Commands

```bash
# Get a single random joke (default)
python joke_generator.py

# List available sources
python joke_generator.py --list-sources

# List categories for a source
python joke_generator.py --list-categories --source jokeapi

# Clear cache
python joke_generator.py --clear-cache
```

### Advanced Usage

```bash
# Get 10 programming jokes
python joke_generator.py --source jokeapi --category Programming --count 10

# Get jokes without caching
python joke_generator.py --no-cache --count 3

# Use custom cache directory
python joke_generator.py --cache-dir /tmp/jokes

# Mix different sources (run multiple times)
python joke_generator.py --source official
python joke_generator.py --source dad
```

## 📚 Available Sources & Categories

### JokeAPI (Default)
**Source:** `jokeapi`

**Categories:**
- `General` - General jokes
- `Knock-Knock` - Knock-knock jokes
- `Programming` - Programming/tech jokes
- `Miscellaneous` - Misc jokes
- `Dark` - Dark humor jokes
- `Spooky` - Spooky jokes
- `Christmas` - Christmas jokes

**Features:**
- Support for both single-line and two-part jokes
- Largest collection of jokes
- NSFW filter available (not implemented in this version)

### Official Joke API
**Source:** `official`

**Categories:**
- `Programming` - Programming jokes
- `Knock-Knock` - Knock-knock jokes  
- `General` - General jokes

**Features:**
- Simple, reliable API
- Numbered joke IDs
- Two-part joke format

### Dad Jokes API
**Source:** `dad`

**Categories:**
- `Dad Joke` - Classic dad jokes

**Features:**
- Pure dad humor
- Unique joke IDs
- Single-line format

## 🎯 Examples

### Example 1: Get a Programming Joke

```bash
$ python joke_generator.py --source jokeapi --category Programming

INFO - 🎭 JokeGenerator Started (caching: enabled)
INFO - 🔄 Fetching from JokeAPI (category: Programming)...
INFO - 📦 Retrieved from cache

============================================================
🎭 Joke #1
============================================================
Source: JokeAPI
Category: Programming
------------------------------------------------------------
Why do Java developers wear glasses?

Because they don't C#
============================================================
```

### Example 2: Get 3 Random Jokes

```bash
$ python joke_generator.py --count 3

INFO - 🎭 JokeGenerator Started (caching: enabled)

[1/3]
INFO - 🔄 Fetching from JokeAPI (category: any)...

============================================================
🎭 Joke #1
============================================================
Source: JokeAPI
Category: General
------------------------------------------------------------
Why don't scientists trust atoms?

Because they make up everything!
============================================================

[2/3]
INFO - 🔄 Fetching from JokeAPI (category: any)...
INFO - 📦 Retrieved from cache

[Joke #2 displayed...]

[3/3]
INFO - 🔄 Fetching from JokeAPI (category: any)...

[Joke #3 displayed...]

INFO - ✅ Successfully fetched 3/3 jokes
```

### Example 3: List Available Options

```bash
$ python joke_generator.py --list-sources

INFO - 📚 Available Joke Sources:
INFO -   • jokeapi
INFO -   • official
INFO -   • dad

$ python joke_generator.py --list-categories --source jokeapi

INFO - 📂 Available Categories for 'jokeapi':
INFO -   • General
INFO -   • Knock-Knock
INFO -   • Programming
INFO -   • Miscellaneous
INFO -   • Dark
INFO -   • Spooky
INFO -   • Christmas
```

## 🛠️ Command-Line Reference

```
usage: joke_generator.py [-h] [--source {jokeapi,official,dad}]
                         [--category CATEGORY] [--count COUNT]
                         [--cache] [--no-cache] [--list-sources]
                         [--list-categories] [--clear-cache]
                         [--cache-dir CACHE_DIR]

JokeGenerator: Get random jokes from multiple APIs

options:
  -h, --help                    Show this help message and exit
  --source {jokeapi,official,dad}
                                Joke API source (default: jokeapi)
  --category CATEGORY           Joke category (JokeAPI only)
  --count COUNT                 Number of jokes to fetch (default: 1)
  --cache                       Enable caching (default: enabled)
  --no-cache                    Disable caching
  --list-sources                List available joke sources
  --list-categories             List available categories for a source
  --clear-cache                 Clear all cached jokes
  --cache-dir CACHE_DIR         Cache directory (default: ./joke_cache)
```

## 💾 Caching

### How Caching Works

- **Enabled by default** for faster repeated requests
- **TTL (Time To Live):** 24 hours
- **Storage:** Local `joke_cache/` directory
- **Cache Key:** Source + Category combination

### Cache Management

```bash
# View cache (it's just JSON files)
ls -la joke_cache/

# Clear all cached jokes
python joke_generator.py --clear-cache

# Disable cache for a single request
python joke_generator.py --no-cache

# Use custom cache directory
python joke_generator.py --cache-dir ~/.jokes_cache
```

## 🔧 API Details

### JokeAPI (v2.jokeapi.dev)

```
Endpoint: https://v2.jokeapi.dev/joke/{category}
Response time: ~100-500ms
Rate limit: ~100 requests/minute (no key required)
Formats: Single-line, Two-part jokes
```

### Official Joke API

```
Endpoint: https://official-joke-api.appspot.com/jokes/random
Response time: ~200-800ms
Rate limit: Generous (no explicit limit)
Formats: Two-part jokes (setup + punchline)
```

### Dad Jokes API

```
Endpoint: https://icanhazdadjoke.com (with Accept: application/json)
Response time: ~100-300ms
Rate limit: High (no explicit limit)
Formats: Single-line jokes
```

## ⚡ Performance

| Operation | Time |
|-----------|------|
| First joke fetch | 0.5-1.5s |
| Cached joke retrieval | 10-50ms |
| Batch fetch (5 jokes) | 2-8s |
| API timeout | 10 seconds |

## 🐛 Troubleshooting

### `ModuleNotFoundError: No module named 'requests'`

```bash
pip install -r requirements.txt
```

### `API request timed out`

Check your internet connection. The default timeout is 10 seconds.

```bash
# Try with a different source
python joke_generator.py --source dad
```

### `Category not found`

Not all categories are available for all sources. Check available categories:

```bash
python joke_generator.py --list-categories --source jokeapi
```

### Cache not working

Ensure write permissions in the current directory:

```bash
# Use custom cache directory
python joke_generator.py --cache-dir /tmp/jokes

# Or clear cache
python joke_generator.py --clear-cache
```

## 📊 Project Structure

```
JokeGenerator/
├── joke_generator.py      # Main application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── INSTALL.md            # Installation guide
├── Makefile              # Development commands
└── joke_cache/           # Cached jokes (generated)
    └── *.json            # Cache files
```

## 🎓 Learning Resources

### About the APIs

- **JokeAPI**: https://jokeapi.dev/
- **Official Joke API**: https://official-joke-api.appspot.com/
- **Dad Jokes**: https://icanhazdadjoke.com/

### Python Concepts Used

- HTTP requests with `requests` library
- JSON parsing
- File I/O and caching
- Command-line argument parsing with `argparse`
- Exception handling and logging
- Object-oriented programming (OOP)

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions are welcome! Ideas:

- Add more joke API sources
- Implement database-backed caching (SQLite, Redis)
- Add web UI (Flask/FastAPI)
- Add statistics tracking
- Implement joke rating system
- Add joke filtering (language, content warnings)
- Create API wrapper library

## ✨ Fun Ideas

- **Slack Bot**: Integrate with Slack for daily jokes
- **Discord Bot**: Send jokes to Discord servers
- **Web Dashboard**: Build a web UI to browse jokes
- **Mobile App**: Create a mobile app with Flutter/React Native
- **Random Schedule**: Cron job to send jokes at intervals
- **Analytics**: Track which jokes are funniest
- **Custom API**: Build your own joke API backend

## 📞 Support

If you encounter issues:

1. Check the Troubleshooting section
2. Review error messages in the logs
3. Open a GitHub issue with:
   - Command you ran
   - Full error message
   - System info (OS, Python version)
   - Internet connection status

---

**Made with 😄 for humor lovers everywhere**

Give us a ⭐ if JokeGenerator makes you laugh!
