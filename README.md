# Sistema de Login com Autenticação Facial

Um sistema de login com autenticação facial desenvolvido em Flask e MinIO. Este projeto permite que os usuários façam login verificando a imagem de seu rosto com uma imagem armazenada e dados de usuário.

## Funcionalidades
- **Autenticação com Reconhecimento Facial**: Verifica a identidade do usuário comparando uma imagem capturada ao vivo com uma imagem armazenada.
- **Armazenamento em MinIO**: Armazena dados de usuário (arquivos JSON) e imagens no MinIO, uma solução de armazenamento de objetos de alta performance.
- **Privacidade de Dados**: Os dados dos usuários (como CPF, e-mail e senha) são armazenados com segurança e utilizados apenas para fins de autenticação.

## Estrutura do Projeto
```
├── static/ 
│ └── images/ 
│    ├── user1.jpg # Imagens de usuários pré-armazenadas para autenticação 
|
├── templates/ 
│   ├── index.html # Página de login 
│   ├── camera.html # Interface da câmera para capturar imagens ao vivo 
│   ├── success.html # Página de redirecionamento para login bem-sucedido 
|
├── config.py # Arquivo de configuração com setup do cliente MinIO e dados de usuário 
├── app.py # Lógica principal da aplicação 
├── docker-compose.yml # Configuração do Docker 
└── requirements.txt # Requisitos para rodar o projeto
```

## Configuração

### Pré-requisitos
- Python 3.8+
- Flask
- MinIO
- Docker (para executar o MinIO localmente)

### Instalação

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/dutra-felipe/Facial_Login_System.git
    cd Facial_Login_System
    ```

2. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Execute o MinIO com Docker:**
    ```bash
    docker-compose up -d
    ```

4. **Configure o MinIO:**
   - Certifique-se de que o MinIO está rodando em `localhost:9000` (ou atualize a URL em `config.py` se for diferente).
   - Use as chaves de acesso e segredo padrão configuradas no `config.py`.

   ```bash

    # No docker-compose.yml, colocar um usuário e senha

    MINIO_ROOT_USER: #colocar um usuário (Ex: user)
    MINIO_ROOT_PASSWORD: #definir uma senha (Ex: password123)
   ```

5. **Configure os dados de usuário:**
   - No `config.py`, defina usuários com seus dados.

   ```bash

   # Config.py:

   access_key= # "usuario minio definido no docker-compose",
   secret_key= # "senha minio definifo no docker-compose",
   ```
6. **Adicione as imagens em static/images/ :**
    - Defina o usuário em config.py e adicione a imagem na pasta images com o nome do próprio.

    ```bash
    
    # Exemplo:

    {
        "username": "felipe",
        "email": "felipe@example.com",
        "dateOfBirth": "1995-05-10",
        "cpf": "123.456.789-00",
        "password": "senhanaoexiste",
        "photo": "/static/images/felipe.jpg"
    }
    ```
7. **Execute a aplicação Flask:**
    ```bash
    python app.py
    ```

8. **Acesse a aplicação:**
   - Abra `http://localhost:5000` no navegador.

## Uso

1. Abra a página de login e insira os dados do usuário.
2. Capture uma imagem ao vivo usando a câmera.
3. O sistema comparará a imagem capturada com a imagem armazenada no MinIO.
4. Se a autenticação for bem-sucedida, o usuário terá acesso permitido.

## Considerações de Segurança

- Certifique-se de que o `config.py` não seja exposto em repositórios públicos, pois ele contém informações sensíveis.
- Considere mover configurações sensíveis para variáveis de ambiente para uso em produção.

## Melhorias Futuras

- Implementar um sistema de notificação ao usuário por e-mail e SMS ao realizar login.
- Adicionar um painel administrativo para gerenciar dados e imagens dos usuários.
- Integrar autenticação multifatorial para maior segurança.

