"""Photograph every page of docs/book-source.html into docs/assets/pages/pNN.webp.

python build/render_pages.py            (after python build/build_site.py)

Needs Google Chrome and Pillow. Set CHROME=<path to chrome> if it is not in the
default Windows location. Each page is shot alone (?render=N) at 3x device scale;
a shot whose edge comes out white (a rare headless layout race) is retaken.
"""
import os, pathlib, re, shutil, subprocess, sys, time
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(DOCS, "assets", "pages")
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
SCALE, W, H = 3, 560, 780

def page_count():
    html = open(os.path.join(DOCS, "book-source.html"), encoding="utf-8").read()
    return len(re.findall(r'<div class="page ', html))

def shoot(i, png, profile):
    """Chrome's launcher can return before the screenshot is written, so wait for the file."""
    if os.path.exists(png):
        os.remove(png)
    url = pathlib.Path(DOCS, "book-source.html").as_uri() + f"?render={i}"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
                    f"--force-device-scale-factor={SCALE}", f"--window-size={W},{H}", f"--user-data-dir={profile}",
                    f"--screenshot={png}", url], check=True, capture_output=True)
    last = -1
    for _ in range(120):                      # up to 30 s
        time.sleep(.25)
        if os.path.exists(png):
            size = os.path.getsize(png)
            if size > 0 and size == last:
                return
            last = size
    raise RuntimeError(f"page {i}: Chrome wrote no screenshot")

def clean(png):
    im = Image.open(png).convert("RGB")
    w, h = im.size
    if (w, h) != (W * SCALE, H * SCALE):
        return None
    for x, y in ((w - 4, h // 2), (w - 4, h - 6), (4, h // 2), (w // 2, h - 4)):
        if im.getpixel((x, y)) == (255, 255, 255):
            return None
    return im

def main():
    os.makedirs(OUT, exist_ok=True)
    n = page_count()
    # scratch folder inside the project (ignored by git), removed when done
    tmp = os.path.join(ROOT, "build", ".render_tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    for i in range(n):
        png = os.path.join(tmp, f"p{i:02d}.png")
        for attempt in range(5):
            shoot(i, png, os.path.join(tmp, f"profile{attempt}"))
            im = clean(png)
            if im:
                break
        else:
            sys.exit(f"page {i}: could not get a clean shot")
        im.save(os.path.join(OUT, f"p{i:02d}.webp"), "WEBP", quality=84, method=6)
        print(f"page {i:02d} ok" + (f" (retake {attempt})" if attempt else ""))
    shutil.rmtree(tmp, ignore_errors=True)
    for f in os.listdir(OUT):
        m = re.match(r"p(\d+)\.webp$", f)
        if m and int(m.group(1)) >= n:
            os.remove(os.path.join(OUT, f))
    print(n, "pages written to", OUT)

if __name__ == "__main__":
    main()
