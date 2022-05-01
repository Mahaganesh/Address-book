from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router


app = FastAPI(title='ADB Tool', version='2.0.0',debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix='/api/v1')