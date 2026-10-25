from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .models import InvoicePreview
from .catalog import PRODUCTS, product
from .billing import preview


def create_app():
    app = FastAPI(title='Paper Trail — fictional practice')
    static = Path(__file__).parent / 'static'
    app.mount('/static', StaticFiles(directory=static), name='static')

    @app.get('/')
    def home():
        return FileResponse(static / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.get('/api/products')
    def products():
        return {'items': list(PRODUCTS.values())}

    @app.get('/api/products/{sku}')
    def product_detail(sku: str):
        return product(sku)

    @app.post('/api/invoices/preview')
    def invoice_preview(request: InvoicePreview):
        return preview(request)

    return app


app = create_app()
