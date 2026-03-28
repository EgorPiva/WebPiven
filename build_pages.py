import os
from pathlib import Path
import shutil

from app.app import app, posts_list, index, posts, post, about


BASE_URL = os.getenv("PAGES_BASE", "/WebPiven").rstrip("/")


def write_html(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if BASE_URL:
        prefix = BASE_URL if BASE_URL.startswith("/") else f"/{BASE_URL}"
        html = html.replace('href="/', f'href="{prefix}/')
        html = html.replace('src="/', f'src="{prefix}/')
    path.write_text(html, encoding="utf-8")


def render_view(func, *args, path: str) -> str:
    env = {"SCRIPT_NAME": BASE_URL} if BASE_URL else {}
    with app.test_request_context(path, environ_base=env):
        return func(*args)


def main() -> None:
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Copy static assets
    static_src = Path("app/static")
    static_dst = docs_dir / "static"
    if static_dst.exists():
        shutil.rmtree(static_dst)
    shutil.copytree(static_src, static_dst)

    # Base pages
    write_html(docs_dir / "index.html", render_view(index, path="/"))
    write_html(docs_dir / "about" / "index.html", render_view(about, path="/about/"))
    write_html(docs_dir / "posts" / "index.html", render_view(posts, path="/posts/"))

    # Post pages
    posts_data = posts_list()
    for i in range(len(posts_data)):
        write_html(
            docs_dir / "posts" / str(i) / "index.html",
            render_view(post, i, path=f"/posts/{i}/"),
        )

    # Disable Jekyll processing
    (docs_dir / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
