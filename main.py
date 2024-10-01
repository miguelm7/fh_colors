from fasthtml.common import *
import os

app, rt = fast_app()

# Directorio donde se guardarán las imágenes subidas
UPLOAD_DIR = 'uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Ruta principal que muestra el formulario para cargar la imagen
@rt('/')
def get():
    return Div(
        H1('Sube una imagen'),
        Form(
            Input(type='file', name='image', accept='image/*'),
            Label("Selecciona un número: "),
            Select(
                Option("3", value="3"),
                Option("4", value="4"),
                Option("5", value="5"),
                Option("6", value="6"),
                Option("7", value="7"),
                Option("8", value="8"),
                Option("9", value="9"),
                Option("10", value="10"),
                name="number"
            ),
            Button('Subir Imagen', type='submit'),
            hx_post='/upload', enctype='multipart/form-data'
        ),
        Button('Acción por Terminar', onclick="window.location.href='/unfinished'")
    )

# Ruta para manejar la subida de la imagen
@rt('/upload', methods=['POST'])
async def handle_classify(image: UploadFile, number: str):
    # Guardar la imagen subida
    image_path = f"uploads/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())

    return Div(
        P(f"Imagen subida con éxito: {image.filename}, Número seleccionado: {number}"),
        Img(src=f"/uploads/{image.filename}", alt="Uploaded image", style="max-width: 300px;"),
        Button('Volver', onclick="window.location.href='/delete_and_restart'")
    )

# Ruta para servir las imágenes subidas
@rt('/uploads/{filename}')
async def serve_upload(filename: str):
    return FileResponse(f"uploads/{filename}")

# Ruta para manejar la acción de "Por Terminar"
@rt('/unfinished')
def unfinished():
    print("Funcionalidad por terminar.")
    return P('Esta funcionalidad está en proceso.')

# Ruta para eliminar la imagen y volver al estado inicial de la página
@rt('/delete_and_restart')
def delete_and_restart():
    # Eliminar todas las imágenes en el directorio 'uploads'
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Redirigir al estado inicial
    return Div(
        P('Imagen eliminada con éxito. Volviendo al inicio...'),
        Script("window.location.href='/'")  # Redirigir automáticamente al inicio
    )

serve()
