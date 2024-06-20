import uvicorn

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
    app.mount("/server", StaticFiles(directory="server"), name="server")
    templates = Jinja2Templates(directory="server")
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    @app.post("/chat", response_class=HTMLResponse)
    async def get_response_faqs(request: Request) -> HTMLResponse:
        request = await request.json()
        response = DependencyContainer.get_faqs_workflow().execute(request.get('message'), faqs + faqs_unir)
        return HTMLResponse(content=response)

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)