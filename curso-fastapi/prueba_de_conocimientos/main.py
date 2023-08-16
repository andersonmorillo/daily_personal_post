from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:3000",  # Replace with the URL of your Next.js app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/markdown", response_class=HTMLResponse)
def render_markdown():
    file_path = "template_example.md"  # Replace with the actual path to your file

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    markdown_content = "# Hello, *FastAPI*!\nThis is **Markdown** content."
    return str(file_content)
