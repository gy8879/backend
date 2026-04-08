from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, posts, comments, rooms, reservations, groups, applications

app = FastAPI(title="스터디 플랫폼 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록 — prefix="/api/v1"이 앞에 붙는다
app.include_router(auth.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")
app.include_router(comments.management_router, prefix="/api/v1")
app.include_router(rooms.router, prefix="/api/v1")
app.include_router(reservations.router, prefix="/api/v1")
app.include_router(groups.router, prefix="/api/v1")
app.include_router(applications.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "스터디 플랫폼 API 서버가 실행 중입니다."}
