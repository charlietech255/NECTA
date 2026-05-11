"""
NECTA CSEE Results API - Kupata matokeo ya mtihani wa kidato cha nne
API ya kupata matokeo ya mtihani wa CSEE kutoka tovuti ya NECTA
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re
import random
import time

# URLs za msingi
BASE_URL = "https://necta.go.tz/results/view/csee"

# User agents mbalimbali ili kuepuka kublockiwa na firewall ya necta
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]

# function ya kupata headers za random
def pata_headers_za_random():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

# Function ya kufanya request safe
def fanya_request_salama(url, max_retries=3):
    for jaribio in range(max_retries):
        try:
            headers = pata_headers_za_random()
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:  # Maombi mengi sana
                time.sleep(5 * (jaribio + 1))  # Kuchelewesha kwa muda
            else:
                time.sleep(1)
        except requests.RequestException:
            time.sleep(2)
    raise HTTPException(status_code=500, detail="Imeshindikana kupata data baada ya kujaribu")

# Models za data
class Mwaka(BaseModel):
    mwaka: str

class Shule(BaseModel):
    nambari: str
    jina: str

class Mwanafunzi(BaseModel):
    nambari_ya_mwanafunzi: str
    jinsia: str
    jumla: str
    daraja: str
    masomo: dict  # e.g., {"CIV": "D", "HIST": "C", ...}

# Unda app ya FastAPI
app = FastAPI(
    title="NECTA CSEE Results API",
    description="API ya kupata matokeo ya mtihani wa CSEE kutoka tovuti ya NECTA"
)

def safe_request(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            headers = get_random_headers()
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:  # Too many requests
                time.sleep(5 * (attempt + 1))  # Exponential backoff
            else:
                time.sleep(1)
        except requests.RequestException:
            time.sleep(2)
    raise HTTPException(status_code=500, detail="Failed to fetch data after retries")

class Mwaka(BaseModel):
    mwaka: str

class Shule(BaseModel):
    nambari: str
    jina: str

class Mwanafunzi(BaseModel):
    nambari_ya_mwanafunzi: str
    jinsia: str
    jumla: str
    daraja: str
    masomo: dict  # e.g., {"CIV": "D", "HIST": "C", ...}

def pata_miaka():
    """Pata miaka ya matokeo iliyopo kutoka ukurasa wa NECTA."""
    response = fanya_request_salama(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Chota miaka kutoka elementi za h4
    miaka = []
    for h4 in soup.find_all('h4'):
        text = h4.text.strip()
        if text.isdigit() and len(text) == 4:  # create mwaka wa tarakimu 4
            miaka.append(text)
    return miaka

def pata_shule(mwaka: str):
    """Pata shule za mwaka fulani."""
    base_url = f"https://onlinesys.necta.go.tz/results/{mwaka}/csee/"
    # Tafuta indexes za shule
    response = fanya_request_salama(base_url + "index.htm")
    soup = BeautifulSoup(response.text, 'html.parser')
    sub_indexes = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('indexfiles/index_') and href.endswith('.htm'):
            sub_indexes.append(href)
    shule = []
    for sub in sub_indexes:
        time.sleep(random.uniform(0.5, 2.0))  # Kuchelewesha kwa random
        sub_response = fanya_request_salama(base_url + sub)
        sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
        for a in sub_soup.find_all('a', href=True):
            href = a['href']
            if 'results' in href and href.endswith('.htm'):
                nambari = href.split('\\')[-1][:-4].upper()
                full_text = a.text.strip()
                if ' - ' in full_text:
                    jina = full_text.split(' - ')[0].strip()
                    shule.append({'nambari': nambari, 'jina': jina})
    # Ondoa duplicates
    zilizojulikana = set()
    shule_zisizo_na_rudufu = []
    for s in shule:
        key = s['nambari']
        if key not in zilizojulikana:
            zilizojulikana.add(key)
            shule_zisizo_na_rudufu.append(s)
    return shule_zisizo_na_rudufu

def pata_wanafunzi(mwaka: str, shule: str):
    """Pata wanafunzi wa shule fulani kwa mwaka fulani."""
    base_url = f"https://onlinesys.necta.go.tz/results/{mwaka}/csee/"
    # Ikiwa shule si nambari (haianza na S au P), chukulia kama jina na pata nambari
    if not shule.startswith(('S', 'P')):
        shule_zote = pata_shule(mwaka)
        zinazofanana = [s for s in shule_zote if s['jina'].lower() == shule.lower()]
        if not zinazofanana:
            raise HTTPException(status_code=404, detail="Shule haijapatikana")
        shule = zinazofanana[0]['nambari']
    url = base_url + "results/" + shule.lower() + ".htm"
    response = fanya_request_salama(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Tafuta jedwali la wanafunzi (kawaida jedwali la tatu)
    tables = soup.find_all('table')
    if len(tables) < 3:
        raise HTTPException(status_code=500, detail="Jedwali la matokeo halijapatikana")
    table = tables[2]  # Jedwali la wanafunzi
    wanafunzi = []
    rows = table.find_all('tr')[1:]  # Ruka header
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:  # CNO, SEX, AGGT, DIV, SUBJECTS
            nambari_ya_mwanafunzi = cols[0].text.strip()
            jinsia = cols[1].text.strip()
            jumla = cols[2].text.strip()
            daraja = cols[3].text.strip()
            masomo_str = cols[4].text.strip()
            # Changanua masomo, e.g., "CIV - 'D' HIST - 'C'"
            masomo = {}
            matches = re.findall(r"(\w+) - '(\w)'", masomo_str)
            for code, grade in matches:
                masomo[code] = grade
            wanafunzi.append({
                'nambari_ya_mwanafunzi': nambari_ya_mwanafunzi,
                'jinsia': jinsia,
                'jumla': jumla,
                'daraja': daraja,
                'masomo': masomo
            })
    return wanafunzi

@app.get("/")
def root():
    return {"message": "NECTA CSEE Results API inafanya kazi. Tembelea /docs kwa maelezo ya API."}

@app.get("/miaka", response_model=list[str])
def orodha_miaka():
    return pata_miaka()

@app.get("/shule/{mwaka}", response_model=list[Shule])
def orodha_shule(mwaka: str):
    return pata_shule(mwaka)

@app.get("/wanafunzi/{mwaka}/{shule}", response_model=list[Mwanafunzi])
def orodha_wanafunzi(mwaka: str, shule: str):
    return pata_wanafunzi(mwaka, shule)

strart the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
