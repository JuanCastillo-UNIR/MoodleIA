import asyncio
from fastapi.responses import StreamingResponse
import uvicorn, os

if not __name__.startswith("__mp"):
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    from api.common.dependency_container import DependencyContainer
    from api.workflows.FAQs.extract_FAQs import obtener_faqs, obtener_faqs_unir
    faqs = obtener_faqs(); faqs_unir = obtener_faqs_unir()
    DependencyContainer.initialize()
    
    app = FastAPI(title="Chatbot FAQs Becat", version="1.0.0")
    current_directory = os.path.dirname(os.path.abspath(__file__))
    static_files_directory = os.path.join(current_directory, 'server')
    app.mount(path="/server", app=StaticFiles(directory=static_files_directory), name='server')
    templates = Jinja2Templates(directory=static_files_directory)
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    async def async_generator_sync(generator):
        for item in generator:
            yield item
            await asyncio.sleep(0.01)  # Yield control to the event loop
    @app.post("/chat")
    async def get_response_faqs(request: Request) -> HTMLResponse:
        request_data = await request.json()
        response_generator = DependencyContainer.get_faqs_workflow().execute(request_data.get('message'), faqs + faqs_unir)
        return StreamingResponse(async_generator_sync(response_generator), media_type="text/html")

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=10000, reload=True)