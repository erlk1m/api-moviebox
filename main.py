from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from moviebox_api.v3.core import Search, ItemDetails, DownloadableVideoFilesDetail, Homepage
from moviebox_api.v3.http_client import MovieBoxHttpClient
from moviebox_api.v3.constants import SubjectType, TabID
from typing import Optional

app = FastAPI(title="MovieBox BFF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MovieBox API Server is running!"}

# --- 🏠 Home Routes ---

@app.get("/home")
async def get_home():
    try:
        async with MovieBoxHttpClient() as client:
            home = Homepage(client, tab_id=TabID.ALL)
            results = await home.get_content_model()
            return results.model_dump(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/home/banner")
async def get_home_banner():
    try:
        async with MovieBoxHttpClient() as client:
            home = Homepage(client, tab_id=TabID.ALL)
            results = await home.get_content_model()
            banners = []
            for item in results.items:
                if item.banner:
                    banners.append(item.banner.model_dump(by_alias=True))
            return {"banners": banners}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/home/sections")
async def get_home_sections():
    try:
        async with MovieBoxHttpClient() as client:
            home = Homepage(client, tab_id=TabID.ALL)
            results = await home.get_content_model()
            sections = []
            for item in results.items:
                if item.title:
                    sections.append({
                        "title": item.title,
                        "count": len(item.subjects) if item.subjects else 0
                    })
            return {"sections": sections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/home/trending")
async def get_home_trending():
    try:
        async with MovieBoxHttpClient() as client:
            home = Homepage(client, tab_id=TabID.ALL)
            results = await home.get_content_model()
            return {"trending_title": results.trending_title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- 🎬 Movies & TV Routes ---

@app.get("/movies")
async def get_movies():
    try:
        async with MovieBoxHttpClient() as client:
            home = Homepage(client, tab_id=TabID.MOVIE)
            results = await home.get_content_model()
            return results.model_dump(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tv-series")
async def get_tv_series():
    try:
        async with MovieBoxHttpClient() as client:
            home = Homepage(client, tab_id=TabID.TV_SERIES)
            results = await home.get_content_model()
            return results.model_dump(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/animation")
async def get_animation():
    try:
        async with MovieBoxHttpClient() as client:
            home = Homepage(client, tab_id=TabID.ANIME)
            results = await home.get_content_model()
            return results.model_dump(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ranking")
async def get_ranking():
    try:
        async with MovieBoxHttpClient() as client:
            home = Homepage(client, tab_id=TabID.ALL)
            results = await home.get_content_model()
            rankings = []
            for item in results.items:
                if item.ranking_data:
                    rankings.append(item.ranking_data)
            return {"rankings": rankings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- 🔍 Search & Details Routes ---

@app.get("/search")
async def search_content(q: str):
    try:
        async with MovieBoxHttpClient() as client:
            searcher = Search(client, query=q, subject_type=SubjectType.ALL)
            results = await searcher.get_content_model()
            return results.model_dump(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/suggest")
async def search_suggest(q: str):
    try:
        async with MovieBoxHttpClient() as client:
            searcher = Search(client, query=q, subject_type=SubjectType.ALL, per_page=10)
            results = await searcher.get_content_model()
            data = results.model_dump(by_alias=True)
            if 'items' in data:
                data['items'] = data['items'][:5]
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/detail/{slug}")
async def get_details(slug: str):
    try:
        async with MovieBoxHttpClient() as client:
            details = ItemDetails(client, include_seasons=True)
            results = await details.get_content_model(subject_id=slug)
            return results.model_dump(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stream/{id}")
async def get_stream(id: str, detail_path: Optional[str] = None):
    try:
        async with MovieBoxHttpClient() as client:
            downloadables = DownloadableVideoFilesDetail(client)
            results = await downloadables.get_content_model(subject_id=id)
            return results.model_dump(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
