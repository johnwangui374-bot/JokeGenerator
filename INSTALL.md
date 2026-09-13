# JokeGenerator Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Internet**: Stable connection to reach external APIs
- **Disk Space**: ~50MB (includes cache)

## Quick Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/johnwangui374-bot/JokeGenerator.git
cd JokeGenerator
```

### Step 2: Install Python (if needed)

#### macOS
```bash
brew install python@3.11
python3 --version  # Verify
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
python3 --version  # Verify
```

#### Windows
Download from https://www.python.org/downloads/ and run installer

### Step 3: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python joke_generator.py --help
```

You should see the help message. If you do, installation is complete! ✅

## Running the Application

### Basic Usage

```bash
# Get a random joke
python joke_generator.py

# Get a programming joke
python joke_generator.py --category Programming

# Get 5 jokes
python joke_generator.py --count 5
```

### Without Virtual Environment

If you prefer not to use a virtual environment:

```bash
pip3 install -r requirements.txt
python3 joke_generator.py
```

## Troubleshooting

### Python not found

**Problem**: `command not found: python`

**Solution**:
```bash
# Try python3 instead
python3 joke_generator.py

# Or add alias
alias python=python3
```

### Module not found: requests

**Problem**: `ModuleNotFoundError: No module named 'requests'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Virtual environment issues

**Problem**: Virtual environment not activating

**Solution**:
```bash
# Recreate virtual environment
rm -rf venv  # or: rmdir venv /s /q (Windows)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### API connection errors

**Problem**: `API request timed out`

**Solution**:
- Check your internet connection
- Try a different API source: `python joke_generator.py --source dad`
- Wait a moment and try again (rate limiting)

## Optional: Make it Executable (Linux/macOS)

```bash
# Make script executable
chmod +x joke_generator.py

# Run directly
./joke_generator.py

# Or add to PATH for global access
sudo cp joke_generator.py /usr/local/bin/joke-generator
joke-generator --help
```

## Optional: Using with Make

If you have `make` installed:

```bash
make help              # Show available commands
make install           # Install dependencies
make run               # Run the application
make format            # Format code
make test              # Run tests (if available)
```

## Upgrading

To update to the latest version:

```bash
cd JokeGenerator
git pull origin main
pip install --upgrade -r requirements.txt
```

## Uninstalling

```bash
# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir venv /s /q  # Windows

# Remove project folder
cd ..
rm -rf JokeGenerator  # macOS/Linux
rmdir JokeGenerator /s /q  # Windows
```

## Next Steps

1. **Read the README**: `cat README.md`
2. **Get a joke**: `python joke_generator.py`
3. **Explore options**: `python joke_generator.py --help`
4. **Check categories**: `python joke_generator.py --list-categories`

## Getting Help

- **README.md**: Full documentation and examples
- **Command help**: `python joke_generator.py --help`
- **GitHub Issues**: Open an issue on the repository

---

**Installation complete! Time to laugh! 😄**
