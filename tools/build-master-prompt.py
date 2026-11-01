#!/usr/bin/env python3
"""
Ensamba MASTER-PROMPT-DESDE-CERO.md leyendo los archivos reales del repo,
para que el prompt contenga SIEMPRE el código exacto que hay en disco.

Uso:  python3 tools/build-master-prompt.py [archivo-de-salida]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), "MASTER-PROMPT-DESDE-CERO.md")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


FILES = {
    "index.html": read("index.html"),
    "logo.svg": read("logo.svg"),
    "manifest.json": read("manifest.json"),
    "sw.js": read("sw.js"),
    "make-icons.py": read("tools", "make-icons.py"),
    "gitignore": read(".gitignore"),
    "README.md": read("README.md"),
    "GUIA.md": read("GUIA-INSTALACION.md"),
}
for name, txt in FILES.items():
    assert "```" not in txt, f"{name} contiene ``` y rompería el bloque de código"

DOC = f"""# MASTER PROMPT v3 — Counters, construcción desde cero

**Cómo usarlo:** chat nuevo en Arena Agent Mode **con el conector de GitHub activo** y tu repo seleccionado (vacío). Pega todo lo que está entre `=== INICIO ===` y `=== FIN ===`.

Este prompt no describe el diseño: **lo entrega como código completo**. El agente no tiene que "interpretar" nada, solo escribir los archivos exactamente como vienen y publicarlos.

---

=== INICIO ===

# Rol y objetivo

Eres el ingeniero que va a publicar **Counters** en mi repositorio de GitHub. El repositorio está **vacío**. La app ya está terminada y probada: en este prompt te entrego los archivos **completos y literales**. Tu trabajo **no es diseñar ni mejorar nada**, es:

1. Crear los archivos en la raíz del repo con el contenido exacto que te doy.
2. Generar los 5 íconos PNG a partir del diseño de `logo.svg` (script del bloque 5).
3. Activar GitHub Pages y entregarme la URL.
4. Verificar que se vea igual (lista de comprobación al final).

# Reglas duras (no negociables)

- **Copia literal, byte por byte.** No reformatees, no "mejores", no cambies colores, textos, medidas ni nombres de clases o funciones. No agregues comentarios ni dependencias.
- **Un solo archivo de app**: `index.html` con HTML+CSS+JS embebidos. Sin frameworks, sin CDN, sin build step, sin npm.
- **100% local**: `localStorage`, sin backend, sin cuentas, sin analytics, sin requests externos.
- Los archivos van **en la raíz del repo** (`index.html` en la raíz, no dentro de una carpeta).
- Si crees que algo está mal, **pregúntame antes** de cambiarlo. No tomes la iniciativa.
- Commits en español, descriptivos. Nunca `force push`. Nunca borres archivos que no creaste vos.

# Archivos a crear

| Archivo | Contenido |
|---|---|
| `index.html` | La app completa (bloque 1) |
| `manifest.json` | PWA (bloque 3) |
| `sw.js` | Service worker, cache `counters-v2` (bloque 4) |
| `logo.svg` | Logo clickera con odómetro 001 (bloque 2) |
| `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png`, `favicon.png` | Generar con el script del bloque 5 |
| `.nojekyll` | Archivo vacío (para GitHub Pages) |
| `.gitignore` | Bloque 6 |
| `README.md` | Bloque 7 |
| `GUIA-INSTALACION.md` | Bloque 8 |
| `tools/make-icons.py` | El script del bloque 5, guardado tal cual en el repo |

Si `index.html` es demasiado largo para escribirlo de una sola vez, créalo por partes (escribir y luego anexar) y al final verifica que pese ~76 KB y contenga las cadenas `flipclock`, `collar`, `counters.v2` y `touch-action:manipulation`.

---

## BLOQUE 1 — `index.html` (completo, literal)

```html
{FILES['index.html']}```

---

## BLOQUE 2 — `logo.svg` (completo, literal)

```svg
{FILES['logo.svg']}```

---

## BLOQUE 3 — `manifest.json` (completo, literal)

```json
{FILES['manifest.json']}```

---

## BLOQUE 4 — `sw.js` (completo, literal)

```js
{FILES['sw.js']}```

---

## BLOQUE 5 — Íconos PNG

`manifest.json` e `index.html` referencian estos archivos; hay que generarlos y **committearlos** (no dejarlos solo generados en local).

El script no necesita navegador ni librsvg: dibuja el logo con Pillow (gradientes, círculos, texto monoespaciado) sobre un lienzo 4x y lo reduce con LANCZOS. Guardalo en `tools/make-icons.py` y ejecutalo desde la raíz del repo:

```bash
pip install pillow
python3 tools/make-icons.py .
```

Contenido exacto de `tools/make-icons.py`:

```python
{FILES['make-icons.py']}```

Verificación: los 5 archivos existen, pesan más de 1 KB y `icon-512.png` mide 512×512.

---

## BLOQUE 6 — `.nojekyll` y `.gitignore`

`.nojekyll` va **vacío** (0 bytes). Evita que GitHub Pages procese el sitio con Jekyll y sirva todos los archivos tal cual.

`.gitignore`:

```
{FILES['gitignore']}```

---

## BLOQUE 7 — `README.md`

```md
{FILES['README.md']}```

---

## BLOQUE 8 — `GUIA-INSTALACION.md`

```md
{FILES['GUIA.md']}```

---

# Publicación en GitHub

1. Revisa qué rama es la default (`main`). Si el repo está vacío, crea `main`.
2. Commitea todos los archivos en la raíz. Mensajes sugeridos:
   - `Counters: app completa (contador + ciclo)`
   - `Counters: íconos generados desde el logo`
   - `Counters: PWA publicada en GitHub Pages`
3. Activa Pages: **Settings → Pages → Source: Deploy from a branch → Branch `main`, folder `/ (root)` → Save**. (Si tenés la API con permisos suficientes, podés hacerlo directo; si no, dame la instrucción manual y avisame.)
4. Espera 1–2 minutos. La URL queda `https://USUARIO.github.io/REPO/`.
5. Verifica que `https://USUARIO.github.io/REPO/index.html`, `/manifest.json`, `/sw.js` y `/icon-192.png` devuelvan **200**, no 404.
6. Entrégame al final: la URL, la lista de archivos commiteados, y el resultado de la verificación.

**Importante:** GitHub Pages gratuito **exige repo público**. Si el repo es privado, decime y en vez de Pages usamos Netlify o Vercel (también gratis y con HTTPS). No cambies la visibilidad del repo sin avisarme.

# Verificación antes de dar por terminado

Abre la URL publicada (o sírvela en local) y comprueba:

**Flujo**
- [ ] Al abrir **no** pide PIN: se ve solo el contador de 3 dígitos y el botón.
- [ ] Bloqueada: no hay barra inferior, ni botones de periodo/ovulación, ni etiquetas de texto.
- [ ] El botón grande registra: los dígitos cambian con animación de solapa, vibra y aparece el sello `+1`.
- [ ] Aparece la barra **DESHACER** 5 s; al tocarla el contador vuelve atrás.
- [ ] El candado (arriba a la derecha) pide PIN; con un PIN erróneo dice `PIN incorrecto`; con `1234` entra.
- [ ] Desbloqueada aparecen: etiqueta `encuentros hoy`, tira semanal, los 4 botones (Inicio/Fin × Periodo/Ovulación) y la barra inferior de 5 pestañas.
- [ ] Calendario: el día de hoy muestra el punto bordó y el total; se puede marcar Inicio/Fin de periodo y de ovulación en cualquier día.
- [ ] Tocar la hora de un registro abre `Editar hora` con −5/+5 min y guarda el cambio.
- [ ] Ajustes: cambiar PIN, exportar respaldo, borrar todo.

**Visual**
- [ ] Los 3 dígitos tienen el corte a la mitad con bisagras metálicas y tipografía condensada pesada.
- [ ] El botón **no tiene texto, ni `+`, ni ícono**: solo el domo grafito mate dentro del bisel bordó.
- [ ] Colores: encuentro bordó, periodo rosado apagado, ovulación púrpura. Todo con degradado.
- [ ] En el calendario el superíndice con la cantidad aparece **solo cuando hay más de 1** registro en el día.
- [ ] Ningún emoji en la interfaz.

**Técnico**
- [ ] Sin errores en consola ni `pageerror`.
- [ ] Los datos persisten al cerrar y reabrir.
- [ ] Con la app ya cargada una vez, abrirla sin internet funciona (service worker).
- [ ] Sin scroll horizontal a 360, 390 y 430 px de ancho.
- [ ] Dos toques rápidos seguidos en el botón registran **dos** veces (el zoom por doble tap está desactivado con `touch-action:manipulation`, no con `preventDefault`).

Si algún punto falla, avísame con el detalle en vez de reescribir el archivo por tu cuenta.

=== FIN ===
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(DOC)
print("escrito", OUT, os.path.getsize(OUT), "bytes")
