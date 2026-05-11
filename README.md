# NECTA CSEE Results API

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)

A professional FastAPI-based web API for retrieving Certificate of Secondary Education Examination (CSEE) results from the National Examinations Council of Tanzania (NECTA) website. This API provides programmatic access to examination data, making it easier for developers and institutions to integrate Tanzanian secondary school results into their applications.

## 🌟 Features

- **Comprehensive Data Access**: Retrieve available examination years, school lists, and detailed student results
- **Flexible Querying**: Query schools by code or name
- **Anti-Blocking Measures**: Built-in protections against rate limiting and blocking
- **Humanized Code**: Clean, readable code with Swahili comments and naming conventions
- **FastAPI Integration**: Modern, high-performance API with automatic documentation
- **Error Handling**: Robust error handling with meaningful responses

## 📋 Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)
- [Repository](#repository)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Dependencies

The project uses the following main dependencies:

- `fastapi==0.104.1` - Modern web framework for building APIs
- `uvicorn==0.24.0` - ASGI server for running FastAPI
- `requests==2.31.0` - HTTP library for making requests
- `beautifulsoup4==4.12.2` - HTML parsing library

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/charlietech255/NECTA.git
cd NECTA
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Setup

1. Ensure all dependencies are installed
2. Run the API server:
```bash
python main.py
```

3. The API will be available at `http://127.0.0.1:8001`
4. Access the interactive API documentation at `http://127.0.0.1:8001/docs`

## 📖 Usage

### Basic Usage

```python
import requests

# Get available years
response = requests.get("http://127.0.0.1:8001/miaka")
years = response.json()
print(years)  # ['2025', '2024', '2023']

# Get schools for a specific year
response = requests.get("http://127.0.0.1:8001/shule/2024")
schools = response.json()
print(len(schools))  # Number of schools

# Get student results for a school
response = requests.get("http://127.0.0.1:8001/wanafunzi/2024/S5191")
students = response.json()
print(students[0])  # First student's data
```

### Advanced Usage

The API supports querying schools by name:

```python
# Query by school name (URL-encoded)
response = requests.get("http://127.0.0.1:8001/wanafunzi/2024/A.I.C.T%20KATUNGURU%20CHRISTIAN%20SEMINARY")
```

## 🔗 API Endpoints

### GET /
Returns API status information.

**Response:**
```json
{
  "message": "NECTA CSEE Results API inafanya kazi. Tembelea /docs kwa maelezo ya API."
}
```

### GET /miaka
Retrieves available examination years.

**Response:** `["2025", "2024", "2023"]`

### GET /shule/{mwaka}
Retrieves all schools for a given year.

**Parameters:**
- `mwaka` (string): Examination year (e.g., "2024")

**Response:**
```json
[
  {
    "nambari": "S5191",
    "jina": "A.I.C.T KATUNGURU CHRISTIAN SEMINARY"
  }
]
```

### GET /wanafunzi/{mwaka}/{shule}
Retrieves student results for a specific school and year.

**Parameters:**
- `mwaka` (string): Examination year
- `shule` (string): School code (e.g., "S5191") or school name

**Response:**
```json
[
  {
    "nambari_ya_mwanafunzi": "S5191/0001",
    "jinsia": "F",
    "jumla": "24",
    "daraja": "III",
    "masomo": {
      "CIV": "D",
      "HIST": "C",
      "GEO": "D",
      "KNOWL": "C",
      "KISW": "D",
      "ENGL": "C",
      "BIO": "C",
      "MATH": "D"
    }
  }
]
```

## ⚙️ Configuration

The API includes several configuration options for anti-blocking:

- **User Agent Rotation**: Uses multiple browser user agents
- **Random Delays**: 0.5-2 second delays between requests
- **Retry Mechanism**: Up to 3 retries with exponential backoff
- **Timeout**: 10-second request timeout

These settings are hardcoded in the source code for optimal performance.

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) 
## ⚠️ Disclaimer

This API is for educational and informational purposes only. Users should:

- Respect NECTA's terms of service
- Not use for commercial purposes without permission
- Be aware that web scraping may violate website terms
- Use responsibly to avoid overloading NECTA's servers

The developers are not responsible for any misuse of this tool. Always ensure compliance with applicable laws and regulations.

## 📚 Repository

**GitHub**: [github.com/charlietech255/NECTA](https://github.com/charlietech255/NECTA)

## 🙏 Acknowledgments

- National Examinations Council of Tanzania (NECTA) for providing examination data even though I got no permission from You
- FastAPI community for the excellent web framework
- Contributors and users of this project

---

**Built with ❤️ for Tanzanian education**
