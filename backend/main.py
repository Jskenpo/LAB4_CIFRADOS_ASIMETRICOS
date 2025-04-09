from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import auth_router
from backend.routes import file_router  # Import the file router

app = FastAPI(
    title="Cifrados: Laboratorio 4",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])


app.include_router(file_router, prefix="/file", tags=["file"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )