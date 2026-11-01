# Counters

Contador privado de encuentros + seguimiento del ciclo. Estilo **clickera analógica** (odómetro de 3 dígitos, botón mecánico bordó). Offline, sin cuentas, sin servidores: todo queda en el teléfono.

## Flujo (importante)

| Antes del PIN | Después del PIN |
|---|---|
| **Pantalla muda**: solo el contador de 3 dígitos (estilo flip clock) y el botón mecánico. Sin textos. | Todo lo demás: etiqueta del día, tira semanal, panel de periodo/ovulación, calendario, edición, datos y ajustes |

- Al abrir, la app entra directo y **solo se puede registrar**. No hay barra de navegación.
- El candado (arriba a la derecha) pide el PIN. **PIN inicial `1234`** → cámbialo en Ajustes.
- Después del PIN aparecen: barra inferior (Contador · Calendario · Ciclo · Datos · Ajustes) y los 4 botones de ciclo en el contador.
- Ver, registrar o editar cualquier otra cosa **exige PIN**. Al salir de la app más de 60 s se vuelve a bloquear (configurable). Botón de candado en cada pantalla para bloquear al instante.

## Colores

| Elemento | Color | Dónde |
|---|---|---|
| Encuentro | **rojo profundo / bordó** (gradiente `#c33a55 → #6b1024`) | botón, odómetro, puntos y superíndices del calendario |
| Inicio y fin de **periodo** | **rosado apagado** (gradiente `#d98ba0 → #8a3d52`) | botones "Inicio / Fin", días del calendario |
| Inicio y fin de **ovulación** | **púrpura** (gradiente `#a984d6 → #553077`) | botones "Inicio / Fin", días del calendario, ventana fértil |

Los nombres de botones son exactamente **Inicio** y **Fin**, agrupados por *Periodo* y *Ovulación*.

## Instalación en Android

1. Sube la carpeta a un hosting con **HTTPS** (Netlify drop, GitHub Pages, Vercel, Cloudflare Pages — gratis).
2. Ábrela en **Chrome** → menú ⋮ → **Instalar aplicación**.
3. Queda con ícono propio, pantalla completa y funciona sin internet.

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` | La app completa (HTML+CSS+JS, un solo archivo). Contador con flip clock de 3 dígitos y botón con bisel estriado + domo mate |
| `logo.svg` | Logo vectorial: clickera con odómetro **001** (también embebido en la app) |
| `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png`, `favicon.png` | Íconos derivados del logo (generados con `tools/make-icons.py`) |
| `manifest.json` / `sw.js` | PWA + funcionamiento offline |

## Detalles de uso

- **Registrar**: un toque = un registro con fecha y hora (segundos incluidos). Vibración + "clic" opcional + sello `+1`.
- **Deshacer**: barra inferior durante 5 s tras cada registro.
- **Editar hora**: en el calendario, el día tocado lista cada registro como un chip `15:57 ✎`. Al tocarlo se abre el editor con hora/minutos y botones −5 / +5 min. También desde **Datos → Día por día**.
- **Calendario**: punto bordó si hubo encuentro; **superíndice con la cantidad solo si es mayor que 1**. Día tocado → lista de horas, borrar registros sueltos, o marcar encuentro/periodo/ovulación en fechas pasadas.
- **Ciclo**: la app aprende el largo real del ciclo (promedio de los últimos 6), el sangrado y el día de ovulación. Proyecta el próximo periodo y la ventana fértil con nivel de confianza.
- **Datos**: totales por semana/mes/todo, racha, intervalo medio, día más frecuente, gráfico de 14 días y cruce con el ciclo.
- **Ajustes**: PIN, auto-bloqueo, vibración, sonido, *ocultar cifras antes del PIN*, exportar/importar respaldo JSON, borrar todo.

## Íconos

`python3 tools/make-icons.py` regenera los 5 PNG desde el diseño del logo (solo necesita Pillow: `pip install pillow`). No requiere navegador ni librsvg.

## Pendiente: widget de pantalla de inicio

Un widget real no se puede hacer desde una app web. Requiere app nativa (Kotlin + Glance en Android, WidgetKit en iOS). Mientras tanto, un acceso directo del launcher deja el registro a ~2 toques.

**Aviso**: la predicción es estadística, no un método anticonceptivo ni diagnóstico.
