from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine
from .models import Base
from .api import customers_router, auditors_router, workflow_router
from .config import settings

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="银行投资风险审核系统API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# 注册路由
app.include_router(customers_router)
app.include_router(auditors_router)
app.include_router(workflow_router)

@app.get("/")
async def root():
    return FileResponse("../frontend/index.html")

@app.get("/customer.html")
async def customer_page():
    return FileResponse("../frontend/customer.html")

@app.get("/auditor.html")
async def auditor_page():
    return FileResponse("../frontend/auditor.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
