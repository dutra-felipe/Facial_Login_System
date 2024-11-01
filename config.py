import json
import io
import os
from minio import Minio

# Configuração do cliente MinIO
minio_client = Minio(
    "localhost:9000",
    access_key= # "usuario minio definido no docker-compose",
    secret_key= # "senha minio definifo no docker-compose",
    secure=False,
)

bucket_name = "user-data"

# Verifica se o bucket existe e cria se não existir
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

# Caminho para a pasta de imagens
images_path = "./static/images"

# Dados fictícios - Adicionar quantos usuários quiser
#Adicionar as imagens no caminho ./static/images/ com o nome do usuario para a validação (Ex: felipe.jpg)
users = [
    {
        "username": "felipe",
        "email": "felipe@example.com",
        "dateOfBirth": "1995-05-10",
        "cpf": "123.456.789-00",
        "password": "senha321",
        "photo": "/static/images/felipe.jpg"
    },
    {
        "username": "marcos",
        "email": "marcos@example.com",
        "dateOfBirth": "1995-05-15",
        "cpf": "985.654.321-00",
        "password": "senha654",
        "photo": "/static/images/marcos.jpg"  
    },
    {
        "username": "kelwin",
        "email": "kelwin@example.com",
        "dateOfBirth": "1995-05-15",
        "cpf": "987.654.321-00",
        "password": "senha987",
        "photo": "/static/images/kelwin.jpg"  
    },
]

# Armazenar os dados fictícios no MinIO
for user in users:
    user_json = json.dumps(user).encode()
    try:
        # Armazenar os dados do usuário
        minio_client.put_object(
            bucket_name,
            f"{user['username']}.json",
            io.BytesIO(user_json),
            len(user_json)
        )

        # Armazenar a imagem do usuário
        image_path = os.path.join(images_path, f"{user['username']}.jpg")
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                minio_client.put_object(
                    bucket_name,
                    f"images/{user['username']}.jpg",
                    image_file,
                    os.path.getsize(image_path)
                )
        print(f"Usuário {user['username']} registrado com sucesso!")
    except Exception as e:
        print(f"Erro ao armazenar {user['username']}: {e}")
