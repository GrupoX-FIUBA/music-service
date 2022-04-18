from fastapi import APIRouter

from app.endpoints import albums, playlists, songs


router = APIRouter()
router.include_router(albums.router)
router.include_router(playlists.router)
router.include_router(songs.router)
