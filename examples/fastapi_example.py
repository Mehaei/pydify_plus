# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-10 11:11:43
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-12 16:30:40

import os
from fastapi import FastAPI
from pydify_plus.async_client import AsyncClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DIFY_API_KEY")
base_url = os.getenv("DIFY_BASE_URL", "https://api.dify.ai/v1")

if not api_key:
    raise ValueError("DIFY_API_KEY environment variable not set")

dify = AsyncClient(base_url=base_url, api_key=api_key)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await dify.__aenter__()

@app.on_event("shutdown")
async def shutdown():
    await dify.aclose()

@app.post("/chat")
async def chat_endpoint(payload: dict):
    return await dify.chat.create_chat_message(**payload)