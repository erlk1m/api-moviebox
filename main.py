from fastapi import FastAPI, HTTPException, Query
from moviebox_api.v3.core import Search, ItemDetails, DownloadableVideoFilesDetail
from moviebox_api.v3.http_client import MovieBoxHttpClient
from moviebox_api.v3.constants import SubjectType
from typing import Optional

app = FastAPI(title="MovieBox BFF API")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MovieBox API Server is running!"}

@app.get("/search")
async def search_content(query: str, type: Optional[str] = "ALL"):
    try:
        subject_enum = SubjectType.ALL
        if type.upper() == "MOVIE":
            subject_enum = SubjectType.MOVIE
        elif type.upper() == "SERIES":
            subject_enum = SubjectType.SERIES
            
        async with MovieBoxHttpClient() as client:
            searcher = Search(client, query=query, subject_type=subject_enum)
            results = await searcher.get_content_model()
            return results.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/details")
async def get_details(movie_id: str, type: str = "MOVIE"):
    try:
        subject_enum = SubjectType.MOVIE
        if type.upper() == "SERIES":
            subject_enum = SubjectType.SERIES
            
        async with MovieBoxHttpClient() as client:
            details = ItemDetails(client, include_seasons=True)
            results = await details.get_content_model(subject_id=movie_id)
            return results.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stream")
async def get_stream(movie_id: str, type: str = "MOVIE"):
    try:
        subject_enum = SubjectType.MOVIE
        if type.upper() == "SERIES":
            subject_enum = SubjectType.SERIES
            
        async with MovieBoxHttpClient() as client:
            downloadables = DownloadableVideoFilesDetail(client)
            results = await downloadables.get_content_model(subject_id=movie_id)
            return results.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
