from fastapi import APIRouter

from app.endpoints import albums, playlists, songs, genres
from app.endpoints.base import response_codes


router = APIRouter()
router.include_router(albums.router, responses = {401: response_codes[401]})
router.include_router(playlists.router, responses ={401: response_codes[401]})
router.include_router(songs.router, responses = {401: response_codes[401]})
router.include_router(genres.router, responses = {401: response_codes[401]})
