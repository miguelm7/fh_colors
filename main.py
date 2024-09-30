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
            Button('Subir Imagen', type='submit'),
            hx_post='/upload', enctype='multipart/form-data'
        )
    )

# Ruta para manejar la subida de la imagen
@rt('/upload', methods=['POST'])
async def handle_classify(image:UploadFile):
    # Obtener la información de la imagen subida desde 'request.files'
    # Save the uploaded image
    image_path = f"uploads/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())
    
    
    return Div(
        P(f"Imagen subida con éxito: {image.filename}"),
        Img(src=f"/uploads/{image.filename}", alt="Uploaded image", style="max-width: 300px;")
    )

# Ruta para servir las imágenes subidas
@rt('/uploads/{filename}')
async def serve_upload(filename: str):
    return FileResponse(f"uploads/{filename}")

serve()
