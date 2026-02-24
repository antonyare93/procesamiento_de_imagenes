# Informe Administrativo del Proyecto: Diferencia de Imágenes

**Fecha de elaboración:** 23 de febrero de 2026
**Elaborado por:** Auxiliar Administrativo - Agente de Documentación
**Ubicación del proyecto:** `"PROYECT_PATH"/01_diferencia_imagenes/`
**Asignatura:** Procesamiento Digital de Imágenes

---

## 1. Resumen Ejecutivo

Este proyecto universitario implementa y compara **cinco métodos distintos** para calcular y visualizar diferencias entre pares de imágenes digitales. El notebook `diferencia_imagenes.ipynb` abarca desde el enfoque más elemental (diferencia absoluta pixel a pixel) hasta técnicas perceptuales avanzadas como el Índice de Similitud Estructural (SSIM), pasando por umbralizacion adaptativa, análisis multicanal de color y detección de regiones de cambio mediante contornos.

El proyecto es completamente autónomo: si no se encuentran imágenes reales en la carpeta, genera automáticamente un par de imágenes sintéticas con diferencias predefinidas, garantizando así su funcionamiento sin dependencias externas de datos. Al concluir, presenta una comparativa cuantitativa con cuatro métricas ampliamente reconocidas en la literatura de visión por computadora (MSE, PSNR, SSIM y porcentaje de píxeles modificados).

---

## 2. Descripción General del Proyecto

### 2.1 Contexto

El proyecto forma parte del curso universitario **Procesamiento Digital de Imágenes** y tiene como propósito didáctico introducir al estudiante en las técnicas fundamentales para detectar y cuantificar cambios entre dos imágenes. La diferencia de imágenes es una operación base utilizada en sistemas de videovigilancia, control de calidad industrial, diagnóstico médico por imágenes y análisis de cambios ambientales mediante satélites.

### 2.2 Objetivos

1. Implementar cinco métodos progresivamente más sofisticados de diferencia de imágenes.
2. Visualizar los resultados de cada método de manera clara y comparativa.
3. Calcular métricas cuantitativas objetivas para evaluar el grado de diferencia entre dos imágenes.
4. Proporcionar guías de uso para seleccionar el método más adecuado según el caso de aplicación.

### 2.3 Alcance

- Procesamiento de imágenes en escala de grises y a color (tres canales BGR).
- Aplicación de técnicas de umbralización automática (método de Otsu) y manual.
- Operaciones morfológicas de limpieza sobre máscaras binarias.
- Localización geográfica de regiones de cambio mediante bounding boxes.
- Cálculo y visualización de métricas: MSE, PSNR, SSIM y porcentaje de cambio.

---

## 3. Estructura del Proyecto

```
Diferencia de imágenes/
├── CLAUDE.md                         # Instrucciones del entorno de desarrollo
├── .venv/                            # Entorno virtual Python 3.14
│   └── lib/python3.14/site-packages/ # Dependencias instaladas
└── 01_diferencia_imagenes/           # Carpeta principal del proyecto
    ├── diferencia_imagenes.ipynb     # Notebook principal (único)
    ├── img1.jpg                      # Imagen de entrada 1 (~81 KB)
    └── img2.jpg                      # Imagen de entrada 2 (~78 KB)
```

### Descripción de los componentes

| Componente | Tipo | Descripción |
|---|---|---|
| `diferencia_imagenes.ipynb` | Jupyter Notebook | Contiene todo el flujo del análisis, desde la carga de imágenes hasta la visualización final |
| `img1.jpg` | Imagen JPEG | Imagen de referencia (estado inicial o imagen base) |
| `img2.jpg` | Imagen JPEG | Imagen modificada o capturada en un momento posterior |
| `.venv/` | Directorio | Entorno virtual de Python con todas las dependencias del proyecto |

---

## 4. Flujo del Proceso

El notebook se organiza en **11 secciones numeradas** que siguen una progresión lógica de menor a mayor complejidad.

### 4.1 Entrada de Datos

**Fuentes de datos soportadas:**

El sistema implementa una estrategia de carga con fallback automático:

1. **Imágenes reales:** Busca archivos `img1` e `img2` en formatos `.png`, `.jpg` o `.jpeg` dentro de la carpeta `/01_diferencia_imagenes/`. En este proyecto, los archivos presentes son `img1.jpg` e `img2.jpg`.

2. **Imágenes sintéticas (respaldo automático):** Si no se encuentran imágenes reales o si la lectura falla, el sistema genera automáticamente un par de imágenes de prueba mediante la función `generar_imagenes_sinteticas()`. Estas imágenes consisten en:
   - **Imagen 1:** Fondo con gradiente azul oscuro, un círculo blanco en el centro-izquierda y un triángulo amarillo.
   - **Imagen 2:** El mismo fondo, pero con el círculo desplazado hacia la derecha, el triángulo reemplazado por un rectángulo verde y un círculo rojo añadido.

**Formato de las imágenes de entrada:**

- Tipo de dato: `uint8` (valores enteros de 0 a 255 por canal)
- Espacio de color en carga: BGR (convención de OpenCV)
- Dimensiones: variables; el preprocesamiento unifica las dimensiones si difieren

### 4.2 Procesamiento

El procesamiento se divide en una etapa de preprocesamiento general y cinco métodos de análisis.

#### 4.2.1 Preprocesamiento (Sección 3 del notebook)

Antes de aplicar cualquier método de diferencia, se ejecutan dos pasos obligatorios:

**Paso 1 - Igualación de dimensiones:**
Si `img1` e `img2` tienen dimensiones distintas, se redimensiona `img2` para que coincida con `img1` usando interpolación `INTER_AREA` (ideal para reducción de tamaño). Si las dimensiones ya coinciden, este paso se omite.

**Paso 2 - Conversión a escala de grises:**
Se convierte cada imagen a un único canal usando la fórmula ponderada que respeta la sensibilidad del ojo humano:

```
Y = 0.299 × R + 0.587 × G + 0.114 × B
```

Esto reduce la complejidad computacional de los métodos siguientes de tres canales a uno.

---

#### 4.2.2 Método 1 - Diferencia Absoluta (Sección 4)

**Descripción:** Es el método más elemental. Para cada píxel en posición (x, y) se calcula el valor absoluto de la diferencia de intensidades entre las dos imágenes en escala de grises.

**Fórmula:**
```
D(x, y) = |I₁(x, y) − I₂(x, y)|
```

**Implementación en código:**
```python
diff_abs = cv2.absdiff(img1_gris, img2_gris)
```

**Por qué `cv2.absdiff` y no una resta directa de NumPy:**
Los arrays de imágenes son de tipo `uint8`. Una resta directa puede causar desbordamiento aritmético (wrap-around), produciendo resultados incorrectos. `cv2.absdiff` maneja correctamente este tipo de dato.

**Interpretación del resultado:**
- Valor **0** (negro): píxeles idénticos en ambas imágenes.
- Valor **255** (blanco): cambio máximo posible entre los dos píxeles.
- Se visualiza con mapa de calor (`hot`) para resaltar la magnitud de los cambios.

**Métricas reportadas:** valor mínimo, máximo y promedio de la diferencia.

---

#### 4.2.3 Método 2 - Diferencia con Umbral / Thresholding (Sección 5)

**Descripción:** Convierte la imagen continua de diferencias en una máscara binaria de decisión: "hay cambio" o "no hay cambio". Se aplica un umbral T sobre la imagen de diferencia absoluta.

**Fórmula:**
```
M(x, y) = 255  si D(x, y) > T
M(x, y) = 0    si D(x, y) ≤ T
```

**Dos modalidades implementadas:**

| Modalidad | Descripción | Parámetro |
|---|---|---|
| Umbral fijo | El usuario define manualmente el valor de corte | `UMBRAL_FIJO = 30` |
| Umbral de Otsu | Se calcula automáticamente el valor óptimo que minimiza la varianza intra-clase | `cv2.THRESH_BINARY + cv2.THRESH_OTSU` |

**El método de Otsu** es el que se utiliza como referencia para los pasos posteriores del análisis, ya que se adapta automáticamente al contenido de cada imagen sin necesidad de ajuste manual.

**Métricas reportadas:** valor del umbral calculado por Otsu, cantidad y porcentaje de píxeles con cambio detectado para ambas modalidades.

---

#### 4.2.4 Método 3 - Diferencia en Color BGR (Sección 6)

**Descripción:** Extiende la diferencia absoluta a las imágenes a color completas (tres canales), permitiendo analizar en cuál de los canales B, G, R se concentran los cambios.

**Implementación:**
```python
diff_color = cv2.absdiff(img1_color, img2_color)
diff_b, diff_g, diff_r = cv2.split(diff_color)
```

**Utilidad específica:**
- Detectar cambios de color que no alteran la luminosidad (no visibles en escala de grises).
- Distinguir entre cambios de iluminación global (afectan los tres canales uniformemente) y cambios de contenido (pueden concentrarse en canales específicos).

**Visualización:** Se genera un panel de cuatro imágenes: diferencia total en color + una imagen por canal (con mapas de color Blues, Greens y Reds respectivamente), cada una con su barra de color asociada.

**Métricas reportadas:** promedio de diferencia por canal (B, G, R) por separado.

---

#### 4.2.5 Método 4 - Diferencia Estructural SSIM (Sección 7)

**Descripción:** El Índice de Similitud Estructural (SSIM, por sus siglas en inglés: Structural Similarity Index Measure) es una métrica perceptual que evalúa la similitud entre imágenes considerando tres componentes simultáneamente: luminancia, contraste y estructura. A diferencia de los métodos anteriores que operan píxel a píxel, SSIM trabaja sobre vecindarios locales, lo que lo hace más robusto al ruido y más correlacionado con la percepción visual humana.

**Implementación:**
```python
from skimage.metrics import structural_similarity as ssim
indice_ssim, mapa_ssim = ssim(img1_gris, img2_gris, full=True)
```

El parámetro `full=True` retorna tanto el índice escalar global como el mapa espacial completo de similitud.

**Interpretación:**
- SSIM = **1.0**: imágenes idénticas.
- SSIM próximo a **0**: imágenes muy diferentes.
- El mapa se invierte (`1 - mapa_ssim`) para que las zonas de mayor diferencia aparezcan con intensidades altas en la visualización.

**Comparativa de métodos:**

| Característica | Diferencia Absoluta | SSIM |
|---|---|---|
| Tipo de comparación | Píxel a píxel | Ventanas locales |
| Sensibilidad al ruido | Alta | Baja |
| Correlación con percepción humana | Baja | Alta |
| Rango de valores | [0, 255] por píxel | [-1, 1] global |
| Costo computacional | Bajo | Moderado |

---

#### 4.2.6 Método 5 - Contornos y Regiones de Cambio (Sección 8)

**Descripción:** A partir de la máscara binaria generada por el Método 2 (umbral de Otsu), se localizan y delimitan las regiones de cambio mediante detección de contornos. Este método responde a la pregunta "¿dónde exactamente ocurrieron los cambios?" y proporciona información cuantitativa por región individual.

**Etapas del procesamiento:**

**Etapa 1 - Limpieza morfológica de la máscara:**
```python
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mascara_limpia = cv2.morphologyEx(mascara_binaria, cv2.MORPH_CLOSE, kernel, iterations=2)
mascara_limpia = cv2.morphologyEx(mascara_limpia, cv2.MORPH_OPEN, kernel, iterations=1)
```
- **Cierre morfológico** (dilatación + erosión): une regiones de cambio cercanas y rellena pequeños agujeros internos.
- **Apertura morfológica** (erosión + dilatación): elimina ruido puntual (pequeñas manchas aisladas).
- Se usa un kernel elíptico de 5×5 píxeles.

**Etapa 2 - Detección de contornos:**
```python
contornos, _ = cv2.findContours(
    mascara_limpia, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
```
- `RETR_EXTERNAL`: recupera únicamente los contornos externos (no los anidados).
- `CHAIN_APPROX_SIMPLE`: comprime los segmentos horizontales, verticales y diagonales, guardando solo sus puntos extremos.

**Etapa 3 - Filtrado por área mínima:**
Se descartan los contornos cuya área sea menor a `AREA_MINIMA = 100` píxeles cuadrados, eliminando así el ruido residual que no fue corregido por la morfología.

**Etapa 4 - Marcado de resultados:**
Sobre una copia de la imagen 1 original, se dibuja un rectángulo verde de bounding box y una etiqueta con el número de región y su área en píxeles para cada contorno significativo.

**Métricas reportadas:** cantidad total de contornos, cantidad de contornos significativos tras el filtrado, área total de cambio en píxeles y porcentaje del área total de la imagen que fue modificada.

### 4.3 Salida y Resultados

El notebook no guarda archivos de salida en disco; todos los resultados se despliegan directamente dentro del entorno Jupyter como figuras inline. Las salidas generadas son:

| Sección | Tipo de salida | Descripción |
|---|---|---|
| Sección 2 | Figura | Dos imágenes de entrada lado a lado (color) |
| Sección 3 | Figura | Imágenes en escala de grises |
| Sección 4 | Figura + texto | Imagen de diferencia absoluta con mapa de calor + estadísticas |
| Sección 5 | Figura + texto | Comparativa umbral fijo vs. Otsu + estadísticas de píxeles |
| Sección 6 | Figura + texto | Diferencia en color + desglose por canal B, G, R |
| Sección 7 | Figura + texto | Mapa SSIM con escala inferno + índice global |
| Sección 8 | Texto | Estadísticas de contornos y área de cambio |
| Sección 9 | Figura | Máscara original, máscara limpia y regiones detectadas con bounding boxes |
| Sección 9 | Texto + figura | Tabla de métricas + histograma de diferencia + gráfico de barras normalizado |
| Sección 10 | Figura | Panel resumen con los 5 métodos y panel de métricas |

---

## 5. Dependencias y Requisitos Técnicos

### 5.1 Entorno de ejecución

| Componente | Versión |
|---|---|
| Sistema operativo | Linux (Fedora, kernel 6.18.10) |
| Python | 3.14.2 |
| Entorno virtual | `.venv/` (ubicado en la raíz del proyecto) |

### 5.2 Bibliotecas de Python instaladas

| Biblioteca | Versión | Función en el proyecto |
|---|---|---|
| `opencv-python` (`cv2`) | 4.13.0.92 | Lectura/escritura de imágenes, operaciones de diferencia, umbralización, operaciones morfológicas, detección de contornos, dibujo de resultados |
| `numpy` | 2.4.2 | Manipulación de arrays multidimensionales, operaciones matriciales sobre píxeles |
| `matplotlib` | 3.10.8 | Visualización de imágenes y gráficos; uso de `GridSpec` para paneles compuestos |
| `Pillow` (`PIL`) | 12.1.1 | Importada en el proyecto como alternativa de I/O de imágenes (disponible pero no usada directamente en el flujo principal) |
| `scikit-image` | 0.26.0 | Cálculo de SSIM (`structural_similarity`), MSE (`mean_squared_error`) y PSNR (`peak_signal_noise_ratio`) |
| `scipy` | 1.17.1 | Dependencia transitiva de scikit-image |

### 5.3 Configuración de matplotlib

El notebook aplica la siguiente configuración global al inicio:

```python
plt.rcParams["figure.figsize"] = (14, 6)
plt.rcParams["figure.dpi"] = 100
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11
```

---

## 6. Descripción Detallada del Notebook

### Estructura de celdas

El notebook `diferencia_imagenes.ipynb` contiene **26 celdas** distribuidas de la siguiente manera:

| Sección | Celdas | Tipo | Contenido |
|---|---|---|---|
| Introducción | 1 | Markdown | Definición de diferencia de imágenes, aplicaciones, descripción del contenido del notebook |
| 1. Instalación e imports | 3 | Código | Instalación automática de dependencias vía `subprocess`; imports; configuración de matplotlib |
| 2. Carga de imágenes | 2 | Markdown + Código | Estrategia de carga con fallback a sintéticas; visualización de las imágenes de entrada |
| 3. Preprocesamiento | 2 | Markdown + Código | Igualación de dimensiones; conversión a escala de grises |
| 4. Método 1 - Diferencia Absoluta | 2 | Markdown + Código | Cálculo con `cv2.absdiff`; visualización con mapa de calor `hot` |
| 5. Método 2 - Umbralización | 2 | Markdown + Código | Umbral de Otsu y umbral fijo; comparación visual; estadísticas de píxeles |
| 6. Método 3 - Diferencia en Color | 2 | Markdown + Código | Diferencia en BGR; separación y visualización por canal |
| 7. Método 4 - SSIM | 2 | Markdown + Código | Cálculo del índice y mapa SSIM; conversión a rango [0,255] para visualización |
| 8. Método 5 - Contornos | 3 | Markdown + 2 Código | Morfología; detección y filtrado de contornos; visualización de regiones |
| 9. Comparativa y métricas | 2 | Markdown + Código | Cálculo de MSE, PSNR, SSIM y porcentaje; histograma + gráfico de barras |
| 10. Visualización final | 2 | Markdown + Código | Panel resumen de 7 subfiguras + recuadro de métricas |
| 11. Conclusiones | 1 | Markdown | Tabla comparativa de métodos; recomendaciones por caso de uso |

### Funciones definidas en el notebook

| Función | Parámetros | Retorna | Propósito |
|---|---|---|---|
| `buscar_imagen(nombre_base)` | `str` | `Path \| None` | Busca una imagen con el nombre dado en extensiones `.png`, `.jpg`, `.jpeg` |
| `generar_imagenes_sinteticas(ancho, alto)` | `int, int` (defaults: 400×300) | `(img1, img2)` como arrays NumPy | Crea un par de imágenes BGR con diferencias geométricas predefinidas |

---

## 7. Métricas Utilizadas

El notebook implementa y reporta cuatro métricas cuantitativas de comparación de imágenes:

### 7.1 MSE - Error Cuadrático Medio

**Significado:** Mide el error promedio cuadrático entre píxeles correspondientes. Es sensible a cambios de gran magnitud.

**Fórmula:**

```
MSE = (1/N) × Σ(I₁(i,j) − I₂(i,j))²
```

**Interpretación:** Un MSE de **0** indica imágenes idénticas. No tiene cota superior; depende del contenido de las imágenes.

**Implementación:** `skimage.metrics.mean_squared_error(img1_gris, img2_gris)`

### 7.2 PSNR - Relación Señal-Ruido Pico

**Significado:** Expresa en decibelios qué tan grande es la señal original en comparación con el error (ruido) introducido. Se basa en el MSE.

**Fórmula:**

```
PSNR = 10 × log₁₀(255² / MSE)
```

**Interpretación:** Valores más altos indican mayor similitud. Por convención, valores superiores a 40 dB se consideran imágenes casi idénticas. Si MSE = 0, el PSNR es infinito.

**Implementación:** `skimage.metrics.peak_signal_noise_ratio(img1_gris, img2_gris)`

### 7.3 SSIM - Índice de Similitud Estructural

**Significado:** Métrica perceptual que compara luminancia, contraste y estructura entre imágenes. Correlaciona mejor con la percepción humana que el MSE o el PSNR.

**Rango:** [-1, 1]; el valor **1.0** indica imágenes idénticas.

**Implementación:** `skimage.metrics.structural_similarity(img1_gris, img2_gris, full=True)`

### 7.4 Porcentaje de Píxeles Diferentes

**Significado:** Proporción del área total de la imagen donde se detectó un cambio significativo, usando la máscara binaria del umbral de Otsu como referencia.

**Fórmula:**

```
% cambio = (pixeles con cambio / total de pixeles) × 100
```

**Implementación:** `np.count_nonzero(mascara_binaria) / mascara_binaria.size * 100`

---

## 8. Instrucciones de Uso

### 8.1 Preparación del entorno

```bash
# Activar el entorno virtual del proyecto
source "os.getenv("PROYECT_PATH", Path.cwd())/.venv/bin/activate"

# Instalar dependencias (solo la primera vez)
pip install opencv-python numpy matplotlib Pillow scikit-image
```

### 8.2 Colocar las imágenes de entrada

Copiar los archivos de imagen en la carpeta del notebook con los nombres esperados:

```
01_diferencia_imagenes/
    img1.jpg   (o img1.png)
    img2.jpg   (o img2.png)
```

Si no se colocan imágenes, el notebook generará automáticamente un par de imágenes sintéticas de demostración (400×300 píxeles).

### 8.3 Ejecutar el notebook

```bash
# Iniciar Jupyter Notebook
jupyter notebook "os.getenv("PROYECT_PATH", Path.cwd())/01_diferencia_imagenes/diferencia_imagenes.ipynb"
```

Dentro de Jupyter, ejecutar todas las celdas en orden secuencial:
- `Kernel > Restart & Run All` para una ejecución limpia completa.
- O ejecutar celda por celda con `Shift + Enter` para seguir el flujo de manera interactiva.

### 8.4 Parametrización disponible

Los siguientes valores pueden ajustarse directamente en las celdas de código:

| Variable | Celda | Valor por defecto | Efecto |
|---|---|---|---|
| `UMBRAL_FIJO` | Sección 5 | `30` | Umbral manual para la segunda modalidad de umbralizacion |
| `AREA_MINIMA` | Sección 8 | `100` píxeles | Área mínima de un contorno para ser considerado significativo |
| Tamaño del kernel morfológico | Sección 8 | `(5, 5)` | Tamaño del elemento estructurante para limpieza de la máscara |
| `iterations` (close/open) | Sección 8 | `2` / `1` | Número de iteraciones de las operaciones morfológicas |

---

## 9. Consideraciones Importantes

### 9.1 Requisito de dimensiones iguales

Los métodos de diferencia píxel a píxel exigen que ambas imágenes tengan exactamente las mismas dimensiones. El preprocesamiento del notebook maneja esto automáticamente redimensionando `img2` al tamaño de `img1`. Sin embargo, si la diferencia de tamaño es muy grande, el redimensionamiento puede introducir artefactos que generen falsas detecciones de cambio.

**Recomendación:** Siempre que sea posible, proporcionar imágenes capturadas con la misma resolución y desde la misma posición de cámara.

### 9.2 Sensibilidad a cambios de iluminación

La diferencia absoluta y la umbralizacion son altamente sensibles a cambios globales de iluminación entre las dos imágenes. Si la escena es la misma pero una imagen fue tomada con luz diferente, estos métodos reportarán cambios en zonas que no cambiaron realmente.

**Alternativa:** El SSIM es más robusto a este problema gracias a su componente de luminancia normalizada.

### 9.3 Elección del umbral en el Método 2

El método de Otsu calcula el umbral óptimo asumiendo que el histograma de diferencias tiene una distribución bimodal (píxeles que cambiaron vs. los que no cambiaron). Si los cambios son muy sutiles o muy extensos, esta distribución puede no ser bimodal y el umbral de Otsu puede no ser el más adecuado.

**Alternativa:** Ajustar manualmente `UMBRAL_FIJO` según el contexto de la aplicación.

### 9.4 Dependencia entre métodos

Los métodos no son completamente independientes entre sí dentro del notebook:
- El **Método 2** depende del resultado del **Método 1** (usa `diff_abs`).
- El **Método 5** depende del resultado del **Método 2** (usa `mascara_binaria`).
- La **sección de métricas** depende de resultados de los **Métodos 1, 2, 4 y 5**.

Por esta razón, las celdas deben ejecutarse **siempre en orden secuencial**.

### 9.5 Conversión de espacio de color

OpenCV carga imágenes en formato BGR (Azul-Verde-Rojo), mientras que Matplotlib las visualiza asumiendo RGB (Rojo-Verde-Azul). El notebook aplica `cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)` en cada llamada a `imshow()` para garantizar que los colores se muestren correctamente. Si se modifica el código omitiendo esta conversión, los canales rojo y azul aparecerán intercambiados en las visualizaciones.

### 9.6 Disponibilidad de scikit-image

La biblioteca `scikit-image` es requerida para los cálculos de SSIM, MSE y PSNR (Secciones 7 y 9). Si no está instalada, esas secciones fallarán con un `ImportError`. El instalador automático de la Sección 1 se encarga de incluirla, pero si se ejecuta el notebook sin conexión a internet y la biblioteca no está presente, deberá instalarse manualmente antes.

---

## 10. Conclusiones

### 10.1 Síntesis del proceso

El notebook implementa una cadena de análisis completa y progresiva para la comparación de imágenes digitales. Parte de la operación más simple (diferencia absoluta) y avanza hacia representaciones cada vez más informativas: una máscara de decisión binaria, el desglose por canal de color, una métrica perceptual sofisticada (SSIM) y finalmente la localización geométrica de las zonas de cambio.

La capacidad de generar imágenes sintéticas como respaldo garantiza que el notebook pueda ejecutarse de forma autónoma en cualquier momento, siendo útil tanto para demostración como para desarrollo y prueba de nuevos métodos.

### 10.2 Guía de selección de método por caso de uso

| Escenario | Método recomendado | Justificación |
|---|---|---|
| Videovigilancia en tiempo real | Diferencia absoluta + umbral fijo | Máxima velocidad de procesamiento |
| Control de calidad industrial | SSIM + detección de contornos | Sensibilidad perceptual + localización precisa |
| Análisis de cambio ambiental (satelital) | Diferencia en color + umbralizacion | Cambios espectrales son relevantes |
| Evaluación de calidad de compresión | MSE + PSNR + SSIM (las tres) | Estándar en la industria de codificación de video |
| Diagnóstico médico por imágenes | SSIM + contornos | Correlación perceptual + localización de anomalías |
| Exploración inicial sin conocimiento previo | Diferencia absoluta + Otsu | Simple, sin parámetros manuales requeridos |

### 10.3 Observaciones finales

La diferencia de imágenes es una herramienta fundamental del procesamiento digital de imágenes, y este notebook provee una base sólida para comprender sus principios. Los cinco métodos implementados cubren el espectro desde el análisis puramente matemático (diferencia absoluta, MSE) hasta el análisis estructural y perceptual (SSIM), lo que lo convierte en un recurso de referencia valioso para la asignatura.

El código está organizado de forma clara y comentado, con separación explícita de etapas, lo que facilita su extensión futura —por ejemplo, incorporando métodos como detección de cambios con redes neuronales o análisis en el espacio de frecuencias (transformada de Fourier).

---

*Fin del informe.*

*Documento generado automáticamente por el Agente de Documentación el 23 de febrero de 2026.*
