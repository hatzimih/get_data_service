from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from curl_cffi import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/scrape")
def scrape(url: str = Query(...)):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        res = requests.get(
            url,
            impersonate="chrome124",
            headers=headers,
            timeout=25,
            allow_redirects=True
        )
        
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code, 
                detail=f"BasketNews returned status {res.status_code}"
            )
            
        return {"status": "success", "html": res.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))