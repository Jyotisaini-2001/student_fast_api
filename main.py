
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Response

from routes.route import router

app = FastAPI()
@app.get("/", response_class=HTMLResponse)
async def index():
    html_content = """
    <html>
    <body>
          <h4>👋 Welcome to the Student API</h4>
        <p>Add '/docs/' to the URL to see all routes in the Swagger UI</p>
        <p>Admin: Jyoti Saini 😊</p>
    </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")
app.include_router(router)
