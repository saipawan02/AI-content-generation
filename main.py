import uvicorn

from fastapi import FastAPI

from api.blog_generator.controller import router as blog_router

_app =  FastAPI(
    title='Rag Fusion API',
    description='Retrieval augmented generation (RAG) is a natural language processing (NLP) technique that combines \
    the strengths of both retrieval- and generative-based artificial intelligence (AI) models.'
)

# Adding router to different API groups.
_app.include_router(blog_router)

@_app.get('/')
def check():
    return "Hey dev! This API endpoints are up and running."


if __name__ == "__main__":
    uvicorn.run(app='main:_app', host='0.0.0.0', port=3000)