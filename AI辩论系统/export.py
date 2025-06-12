import os
import webbrowser
from xhtml2pdf import pisa
from utils import console


def export_to_html(html_content, filename="debate_log.html"):
    """保存 HTML 内容并尝试在浏览器中打开"""
    try:
        filepath = os.path.abspath(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        console.print(f"[green]✅ HTML 文件已保存: {filepath}[/green]")
        webbrowser.open(f"file://{filepath}")
    except Exception as e:
        console.print(f"[red]❌ HTML 导出失败: {e}[/red]")


def export_to_pdf(html_content, filename="debate_log.pdf"):
    """将 HTML 内容转为 PDF"""
    try:
        with open(filename, "w+b") as f:
            result = pisa.CreatePDF(src=html_content, dest=f, encoding='UTF-8')
        if result.err:
            console.print(f"[red]❌ PDF 转换出错[/red]")
        else:
            console.print(f"[green]✅ PDF 文件已保存: {filename}[/green]")
    except Exception as e:
        console.print(f"[red]❌ PDF 导出失败: {e}[/red]")
