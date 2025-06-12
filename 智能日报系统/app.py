from fastapi import FastAPI
# 导入 Response 和 FileResponse 用于返回 HTML 文件
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles # <--- 1. 添加这行导入
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import webbrowser # 用于自动打开浏览器

from fetcher import fetch_by_theme
from summarizer import generate_summary
from reporter import save_to_markdown

app = FastAPI()

# 允许跨域请求 (开发时可以保持宽松，生产环境应收紧)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 或者指定前端来源，例如 "http://127.0.0.1:8000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 静态文件服务 ---
# 1. 创建 reports 目录 (如果不存在)
reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
os.makedirs(reports_dir, exist_ok=True)

# 2. 挂载 /reports 路径以提供 reports 目录下的文件
app.mount("/reports", StaticFiles(directory=reports_dir), name="reports")

# 2.5 新增：挂载 /images 路径以提供 images 目录下的文件 <--- 2. 添加这行挂载
app.mount("/images", StaticFiles(directory="images"), name="images")

# 3. 根路由，提供 frontend.html
@app.get("/")
async def read_index():
    # 确保 frontend.html 在项目根目录
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend.html')
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return JSONResponse(content={"error": "frontend.html not found"}, status_code=404)

# --- API ---
# 请求数据模型
class ThemeRequest(BaseModel):
    theme: str

# 日报生成接口
@app.post("/generate")
async def generate_report(request: ThemeRequest):
    print(f"⚙️ 收到日报生成请求，主题：{request.theme}")

    try:
        results = await fetch_by_theme(request.theme)
        summary = generate_summary(results)

        # !! 重要：确保 save_to_markdown 将文件保存在 reports_dir 中 !!
        # 你可能需要修改 reporter.py 或这里的调用方式
        # 假设 save_to_markdown 返回的是完整路径
        full_html_path = save_to_markdown(summary, results, theme=request.theme, output_dir=reports_dir)

        # 获取相对于 reports_dir 的文件名
        report_filename = os.path.basename(full_html_path)

        # 返回可以通过 /reports/... 访问的 URL
        report_url = f"/reports/{report_filename}"
        print(f"✅ 报告生成完毕，访问 URL: {report_url}")
        return JSONResponse(content={"status": "ok", "url": report_url})

    except Exception as e:
        print(f"❌ 生成报告时出错: {e}")
        # 可以考虑打印更详细的错误堆栈信息用于调试
        # import traceback
        # traceback.print_exc()
        return JSONResponse(content={"status": "error", "message": f"生成报告失败: {e}"}, status_code=500)

# --- 运行服务器 ---
if __name__ == "__main__":
    # 自动在浏览器中打开主页
    # webbrowser.open("http://127.0.0.1:8000") # 可以在启动后手动打开
    print("🚀 FastAPI 服务器启动，请访问 http://127.0.0.1:8000")
    import uvicorn
    # 使用 uvicorn 运行 FastAPI 应用
    uvicorn.run(app, host="127.0.0.1", port=8000)