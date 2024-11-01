from flask import Flask, render_template, request, url_for, flash, jsonify
from config import minio_client, bucket_name
import io
import face_recognition
import json
import base64
import numpy as np

app = Flask(__name__)
app.secret_key = "minhachavesecreta"


# Recupera os dados do usuário a partir de um arquivo JSON armazenado no MinIO.
def get_user_data(username):
    try:
        response = minio_client.get_object(bucket_name, f"{username}.json")
        user_data = json.loads(response.read())
        print(f"Dados do usuário {username} carregados com sucesso: {user_data}")
        return user_data
    except Exception as e:
        print(f"Erro ao obter dados do usuário {username}: {e}")
        return None


# Recupera a imagem do usuário e calcula sua codificação facial.
def get_user_image(username):
    try:
        response = minio_client.get_object(bucket_name, f"images/{username}.jpg")
        image = face_recognition.load_image_file(io.BytesIO(response.read()))
        user_face_encoding = face_recognition.face_encodings(image)[0]
        print(f"Encoding da imagem do usuário {username} obtido com sucesso.")
        return user_face_encoding
    except Exception as e:
        print(f"Erro ao obter imagem do usuário {username}: {e}")
        return None


# Verifica a similaridade entre duas codificações faciais usando distância euclidiana
def verify_biometrics(input_face_encoding, user_face_encoding, tolerance=0.4):
    distance = np.linalg.norm(input_face_encoding - user_face_encoding)
    return distance <= tolerance


# Processa o login via POST, verificando as credenciais e a biometria.
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        image_data = data.get("photo")

        user_data = get_user_data(username)
        if not user_data or user_data.get("password") != password:
            print("Falha na verificação das credenciais.")
            flash("Nome de usuário ou senha incorretos.", "danger")
            return jsonify({"message": "Credenciais inválidas"}), 401

        if image_data:
            try:
                image_bytes = io.BytesIO(base64.b64decode(image_data.split(",")[1]))
                input_image = face_recognition.load_image_file(image_bytes)
                input_face_encodings = face_recognition.face_encodings(input_image)

                if len(input_face_encodings) > 0:
                    input_face_encoding = input_face_encodings[0]
                    user_face_encoding = get_user_image(username)

                    # Verificação biométrica
                    if user_face_encoding is not None and verify_biometrics(input_face_encoding, user_face_encoding):
                        print("Autenticação biométrica bem-sucedida.")
                        return jsonify({"redirect": url_for("success")}), 200
                    else:
                        print("Falha na autenticação biométrica.")
                        flash("Falha na autenticação biométrica. Tente novamente.", "danger")
                        return jsonify({"message": "Falha na autenticação biométrica"}), 401
                else:
                    print("Rosto não detectado na imagem capturada.")
                    flash("Não foi possível detectar um rosto. Tente novamente.", "danger")
                    return jsonify({"message": "Rosto não detectado"}), 401
            except Exception as e:
                print(f"Erro ao processar a imagem de entrada: {e}")
                flash(f"Erro ao processar a imagem: {e}", "danger")
                return jsonify({"message": "Erro ao processar a imagem"}), 500

        else:
            print("Imagem não enviada.")
            flash("Nenhuma imagem foi enviada.", "danger")
            return jsonify({"message": "Nenhuma imagem enviada"}), 400

    return render_template("index.html")


# Rota para a página de sucesso após o login bem-sucedido.
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
