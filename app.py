from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import subprocess
import tempfile
import os
import shutil

app = FastAPI(title="LaTeX Compiler API", description="API to compile LaTeX code to PDF")

@app.post("/compile")
async def compile_latex(file: UploadFile = File(...)):
    """
    Compile LaTeX file to PDF.
    Upload a .tex file and get the compiled PDF back.
    If compilation fails, returns the error message.
    """
    if not file.filename.endswith('.tex'):
        raise HTTPException(status_code=400, detail="File must be a .tex file")

    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded file
        tex_path = os.path.join(temp_dir, file.filename)
        with open(tex_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        # Change to temp directory
        os.chdir(temp_dir)

        # Compile with pdflatex
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', file.filename],
                capture_output=True,
                text=True,
                timeout=30
            )

            pdf_filename = file.filename.replace('.tex', '.pdf')
            pdf_path = os.path.join(temp_dir, pdf_filename)

            if result.returncode == 0 and os.path.exists(pdf_path):
                # Success: return PDF
                return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)
            else:
                # Error: return error message
                error_msg = result.stderr if result.stderr else result.stdout
                raise HTTPException(status_code=400, detail=f"LaTeX compilation failed: {error_msg}")

        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=408, detail="Compilation timed out")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/")
def read_root():
    return {
        "message": "LaTeX Compiler API",
        "endpoint": "/compile (POST with .tex file)",
        "docs": "/docs (Swagger UI)",
        "redoc": "/redoc (ReDoc)"
    }