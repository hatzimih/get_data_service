import traceback
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from curl_cffi.requests import AsyncSession

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "message": "Scraper is active"}


@app.get("/scrape")
async def scrape(url: str = Query(...)):
    try:
        # Use an AsyncSession with a recent Chrome profile
        async with AsyncSession(impersonate="chrome124") as s:
            res = await s.get(
                url,
                timeout=30,
                headers={
                    "Accept-Language": "en-US,en;q=0.9",
                },
            )

        return {"status": "success", "upstream_status": res.status_code, "html": res.text}
    except Exception as e:
        # Print the exact Python traceback directly into Render's Logs
        print("--- SCRAPER CRASH TRACEBACK ---")
        traceback.print_exc()
        print("-------------------------------")

        raise HTTPException(status_code=500, detail=f"Scraper error: {str(e)}")
