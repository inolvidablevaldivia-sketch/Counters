# Cómo tener Counters en tu teléfono

La app ya está lista. Solo falta "publicarla" en una URL con HTTPS para que Chrome la pueda instalar como app. Son 5 minutos y no cuesta nada.

---

## Ruta A — Netlify Drop (la más rápida, recomendada)

**En el computador:**

1. Descarga la carpeta del repo (o el archivo `counters.zip` y descomprímelo).
2. Entra a **https://app.netlify.com/drop**
3. **Arrastra la carpeta completa** a la zona que dice "Drag and drop your site folder here".
   - Arrastra la **carpeta**, no el archivo `.zip`.
   - Si te pide crear cuenta, entra con Google o email (es gratis y toma 20 segundos).
4. Espera 10–20 segundos. Te va a dar una URL tipo:
   `https://counters-abc123.netlify.app`
   Cópiala. Esa es tu app.

**En el teléfono:**

5. Abre esa URL en **Chrome** (no en el navegador de Samsung, no en Instagram).
6. Menú **⋮** (arriba a la derecha) → **Instalar aplicación** (o "Añadir a pantalla principal").
7. Confirma. Aparece el ícono de la clickera en tu pantalla de inicio.
8. Ábrela desde el ícono: se abre a pantalla completa, sin barra del navegador, y **funciona sin internet**.

> La primera vez que la abras necesita internet (para guardar la app en caché). Después ya no.

---

## Ruta B — GitHub Pages (si prefieres algo permanente y con tu cuenta)

1. Crea un repositorio nuevo (puede ser privado) en github.com.
2. Sube todos los archivos del repo a la raíz (que `index.html` quede en la raíz, no dentro de una carpeta).
3. **Settings → Pages → Source: Deploy from a branch → Branch: `main` / carpeta `/ (root)` → Save**.
4. En 1–2 minutos queda en `https://TU-USUARIO.github.io/TU-REPO/`
5. Sigue desde el paso 5 de la Ruta A (abrir en Chrome e instalar).

---

## Ruta C — Sin hosting (no la recomiendo)

Puedes copiar la carpeta al teléfono y abrir `index.html` con Chrome. Funciona, pero:
- No se instala: no hay ícono propio ni pantalla completa.
- Los datos quedan guardados de forma frágil y se pueden perder al limpiar el navegador.
- No funciona sin internet de forma confiable.

Úsala solo para probar. Para el día a día, Ruta A o B.

---

## Al instalarla: 4 cosas que debes hacer

1. **Cambiar el PIN.** Ajustes → PIN → actual `1234` → nuevo de 4 dígitos.
2. **Probar el flujo.** Registrar con el botón (debe caer la solapa y vibrar) → DESHACER → tocar el candado → entrar con el PIN → marcar *Inicio* de periodo → revisar el Calendario.
3. **Exportar un respaldo.** Ajustes → Exportar respaldo. Guarda ese archivo en Drive/WhatsApp. Sirve para restaurar si cambias de teléfono.
4. **Decidir si ocultas las cifras.** Ajustes → *Ocultar cifras antes del PIN* → "Ocultas", si te molesta que los 3 dígitos se vean sin PIN.

---

## Cosas importantes que debes saber

- **Los datos viven en el navegador del teléfono.** Si borras "datos del sitio" de Chrome, o desinstalas la app borrando sus datos, se pierde el historial. Por eso el respaldo.
- **No sincroniza entre teléfonos.** Es 100% local (eso es lo que la hace privada).
- **El PIN es un candado de la app, no cifrado.** Alguien con acceso técnico a los archivos del navegador podría leer la base de datos.
- **Actualizaciones:** si te paso una versión nueva, hay que volver a subir los archivos al mismo hosting y abrir la app con internet; se actualiza sola.
- **El widget de pantalla de inicio no es posible** con una app web. Alternativa: un acceso directo del launcher (mantener presionado el ícono → "Añadir a pantalla de inicio") que abre directo al contador. Para widget real hay que compilar una app Android nativa (Kotlin + Glance).

---

## Checklist de lo que ya está probado

- [x] Pantalla inicial muda: solo 3 dígitos + botón, sin textos
- [x] Registro con un toque, animación de solapa y sello `+1`
- [x] Deshacer 5 s
- [x] PIN solo para ver/editar; registrar siempre libre
- [x] Auto-bloqueo a los 60 s fuera de la app
- [x] Calendario con punto bordó y superíndice cuando hay más de 1
- [x] Editar hora de un registro (−5 / +5 min) desde Calendario y desde Datos
- [x] Marcas de periodo (rosado) y ovulación (púrpura) con predicción
- [x] Exportar / importar respaldo JSON
- [x] Funciona offline una vez instalada

---

## Si algo no funciona

| Problema | Causa / solución |
|---|---|
| No aparece "Instalar aplicación" | La URL no es HTTPS, o estás en el navegador de Samsung/Instagram. Abre la URL en Chrome. |
| El ícono no aparece | Es "Añadir a pantalla principal" en vez de instalar; busca en el menú ⋮. |
| Los datos desaparecieron | Se borraron los datos del sitio o cambiaste de navegador. Restaura el respaldo JSON. |
| No registra el toque | Verifica que no estés en modo "ver calendario" con el PIN abierto sin querer; el botón siempre registra. |
| Quiero empezar de cero | Ajustes → Borrar todo. |
