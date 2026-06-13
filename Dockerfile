FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir uvicorn

# Copy application code
COPY . .

# Environment variables
ENV SHOTAPI_BASE_URL=https://aiphotoshop.mynatapp.cc
ENV SHOTAPI_KEY=""
ENV PORT=3000

# Expose port for streamable-http transport
EXPOSE 3000

# Health check via MCP streamable-http endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s \
    CMD python -c "import httpx; r=httpx.get('http://localhost:3000/health'); exit(0 if r.status_code==200 else 1)" || exit 1

# Start server in streamable-http mode for remote deployment
CMD ["python", "-c", "from mcp_server import mcp; import uvicorn; app = mcp.streamable_http_app(); uvicorn.run(app, host='0.0.0.0', port=3000)"]
