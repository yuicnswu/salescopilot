# Lean, production-grade Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Copy assets and server
COPY warrix_products_data.json ./
COPY index.html ./
COPY warrix_product_rag.html ./
COPY server.py ./

# Standard container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request, os; urllib.request.urlopen(f'http://localhost:{os.environ.get(\"PORT\", 8080)}/health')" || exit 1

EXPOSE 8080

CMD ["python3", "server.py"]
