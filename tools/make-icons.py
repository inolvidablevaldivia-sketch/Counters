#!/usr/bin/env python3
"""
Genera los íconos PNG de Counters a partir del diseño de logo.svg.

No necesita navegador ni librsvg: dibuja cada pieza con Pillow (gradientes,
círculos, texto) sobre un lienzo 4x y lo reduce con LANCZOS para antialiasing.

Uso:
    pip install pillow
    python3 tools/make-icons.py [carpeta-de-salida]

Salida: icon-192.png, icon-512.png, icon-maskable-512.png,
        apple-touch-icon.png, favicon.png
"""
import sys
import os
from PIL import Image, ImageDraw, ImageFont

SRC = 128.0                      # viewBox de logo.svg
SS = 4                           # supermuestreo
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
BG = (10, 11, 13, 255)           # #0a0b0d


def hexs(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def at(stops, t):
    """Color en la posición t (0..1) de una lista de (posición, color)."""
    if t <= stops[0][0]:
        return stops[0][1]
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if t <= p1:
            u = (t - p0) / (p1 - p0) if p1 > p0 else 0.0
            return mix(c0, c1, u)
    return stops[-1][1]


def gradient(size, stops, diagonal=True, alpha=None, tile=256):
    """Imagen RGBA con gradiente lineal (o radial si alpha es función de r)."""
    img = Image.new("RGBA", (tile, tile))
    px = img.load()
    for y in range(tile):
        for x in range(tile):
            t = ((x + y) / (2 * (tile - 1))) if diagonal else (y / (tile - 1))
            c = at(stops, t)
            a = 255
            if alpha:
                if diagonal:
                    a = alpha(t)
                else:
                    dx, dy = (x - tile / 2) / (tile / 2), (y - tile / 2) / (tile / 2)
                    a = alpha(min(1.0, (dx * dx + dy * dy) ** 0.5))
            px[x, y] = (c[0], c[1], c[2], a)
    return img.resize((size, size), Image.BICUBIC)


def shape_mask(size, draw_fn):
    m = Image.new("L", (size, size), 0)
    draw_fn(ImageDraw.Draw(m))
    return m


def paste_grad(canvas, grad, mask):
    canvas.paste(grad.resize(canvas.size, Image.BICUBIC), (0, 0), mask)


def draw_logo(size):
    """Devuelve el arte del logo (RGBA, fondo transparente) de `size` px."""
    W = int(size * SS)
    P = W / SRC                       # px por unidad del viewBox
    art = Image.new("RGBA", (W, W), (0, 0, 0, 0))

    def u(v):
        return v * P

    # --- cuerpo (gradiente diagonal + borde metálico) ---
    body_stops = [(0.0, hexs("#31363e")), (0.45, hexs("#1b1e24")), (1.0, hexs("#0d0f12"))]
    rim_stops = [(0.0, hexs("#5b626d")), (0.5, hexs("#2a2f36")), (1.0, hexs("#454b55"))]
    body_box = [u(15), u(16), u(15 + 98), u(16 + 96)]
    paste_grad(art, gradient(W, body_stops, diagonal=True),
               shape_mask(W, lambda d: d.rounded_rectangle(body_box, radius=u(22), fill=255)))
    d = ImageDraw.Draw(art)
    d.rounded_rectangle(body_box, radius=u(22), outline=hexs("#2a2f36") + (255,), width=max(2, int(u(2))))

    # --- brillo superior (radial blanco, alfa 0.16 -> 0), recortado al cuerpo ---
    gimg = gradient(W, [(0.0, (255, 255, 255)), (1.0, (255, 255, 255))],
                    diagonal=False, alpha=lambda r: int(255 * 0.16 * max(0.0, 1 - r / 0.85)))
    gmask = shape_mask(W, lambda dd: dd.rounded_rectangle([u(19), u(20), u(19 + 90), u(20 + 88)],
                                                         radius=u(19), fill=255))
    cx, cy = u(19) + 0.34 * u(90), u(20) + 0.22 * u(88)     # centro del radial
    gimg = gimg.transform((W, W), Image.AFFINE, (1, 0, W / 2 - cx, 0, 1, W / 2 - cy))
    gimg.putalpha(Image.composite(gimg.split()[3], Image.new("L", (W, W), 0), gmask))
    art = Image.alpha_composite(art, gimg)

    d = ImageDraw.Draw(art)

    # --- tornillos ---
    for cx, cy in ((26, 27), (102, 27), (26, 101), (102, 101)):
        r = u(3.1)
        box = [u(cx) - r, u(cy) - r, u(cx) + r, u(cy) + r]
        d.ellipse(box, fill=hexs("#2b3037") + (255,), outline=hexs("#4d535d") + (255,), width=max(1, int(u(1.2))))
        d.line([u(cx) - u(2.3), u(cy), u(cx) + u(2.3), u(cy)], fill=hexs("#161a1f") + (255,), width=max(1, int(u(1.1))))

    # --- sombra del botón ---
    r = u(25)
    d.ellipse([u(64) - r, u(55) - r, u(64) + r, u(55) + r], fill=(8, 9, 11, int(255 * 0.55)))

    # --- botón bordó (gradiente diagonal) ---
    enc_stops = [(0.0, hexs("#b02038")), (0.55, hexs("#8a1327")), (1.0, hexs("#5d0a18"))]
    r = u(24)
    box = [u(64) - r, u(53) - r, u(64) + r, u(53) + r]
    tmp = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    paste_grad(tmp, gradient(W, enc_stops, diagonal=True), shape_mask(W, lambda dd: dd.ellipse(box, fill=255)))
    art = Image.alpha_composite(art, tmp)
    d = ImageDraw.Draw(art)
    d.ellipse(box, outline=(211, 64, 92, int(255 * 0.5)), width=max(1, int(u(1.4))))

    # --- domo interior (gradiente vertical) ---
    btn_stops = [(0.0, hexs("#4a505a")), (0.55, hexs("#23272d")), (1.0, hexs("#12151a"))]
    r = u(17)
    box2 = [u(64) - r, u(53) - r, u(64) + r, u(53) + r]
    tmp = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    paste_grad(tmp, gradient(W, btn_stops, diagonal=False), shape_mask(W, lambda dd: dd.ellipse(box2, fill=255)))
    art = Image.alpha_composite(art, tmp)
    d = ImageDraw.Draw(art)
    d.ellipse(box2, outline=(11, 13, 16, int(255 * 0.8)), width=max(1, int(u(1.0))))

    # --- reflejo superior del domo ---
    d.ellipse([u(58) - u(9), u(45) - u(6), u(58) + u(9), u(45) + u(6)], fill=(255, 255, 255, int(255 * 0.10)))

    # --- ventana de 3 dígitos ---
    win_stops = [(0.0, hexs("#05070a")), (1.0, hexs("#0f1319"))]
    wbox = [u(33), u(82), u(33 + 62), u(82 + 21)]
    tmp = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    paste_grad(tmp, gradient(W, win_stops, diagonal=False), shape_mask(W, lambda dd: dd.rounded_rectangle(wbox, radius=u(6), fill=255)))
    art = Image.alpha_composite(art, tmp)
    d = ImageDraw.Draw(art)
    d.rounded_rectangle(wbox, radius=u(6), outline=hexs("#3c424b") + (255,), width=max(1, int(u(1.4))))
    d.line([u(33), u(92.5), u(95), u(92.5)], fill=(0, 0, 0, int(255 * 0.55)), width=max(1, int(u(1.0))))

    # --- texto "001" ---
    txt = "001"
    fsize = max(8, int(round(u(15))))  # font-size del SVG, en px del lienzo
    spacing = u(3.2)
    try:
        font = ImageFont.truetype(FONT, fsize)
    except Exception:
        font = ImageFont.load_default()
    widths = [d.textlength(c, font=font) for c in txt]
    total = sum(widths) + spacing * (len(txt) - 1)
    x = u(64) - total / 2
    # el SVG usa baseline en y=102.5; PIL con anchor "la" dibuja desde el ascender
    ascent = font.getmetrics()[0] if hasattr(font, "getmetrics") else fsize
    y = u(102.5) - ascent
    for c, wch in zip(txt, widths):
        d.text((x, y), c, font=font, fill=hexs("#f3f1ee") + (255,))
        x += wch + spacing

    return art.resize((size, size), Image.LANCZOS)


def rounded_bg(size, radius_ratio=0.22, inner_ratio=0.94, art=None):
    art = art or draw_logo(size)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(canvas).rounded_rectangle([0, 0, size - 1, size - 1],
                                             radius=int(size * radius_ratio), fill=BG)
    inner = int(size * inner_ratio)
    a = art.resize((inner, inner), Image.LANCZOS)
    off = (size - inner) // 2
    canvas.alpha_composite(a, (off, off))
    return canvas.convert("RGB")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    art = draw_logo(512)                                   # master (se dibuja a 4x y se reduce)

    for name, size in (("icon-512.png", 512), ("icon-192.png", 192),
                       ("apple-touch-icon.png", 180), ("favicon.png", 64)):
        rounded_bg(size, art=art).save(os.path.join(out, name))

    # maskable: lienzo completo (sin esquinas redondeadas), arte al 78% (zona segura Android)
    m = Image.new("RGBA", (512, 512), BG)
    a = art.resize((int(512 * 0.78),) * 2, Image.LANCZOS)
    m.alpha_composite(a, ((512 - a.width) // 2, (512 - a.height) // 2))
    m.convert("RGB").save(os.path.join(out, "icon-maskable-512.png"))

    print("íconos generados en", out)


if __name__ == "__main__":
    main()
