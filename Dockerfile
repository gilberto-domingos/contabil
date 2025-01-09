# Usar a imagem base do Python Slim
FROM python:3.12-slim

# Atualizar repositórios e instalar dependências do sistema operacional
RUN apt-get update && apt-get install -y \
    iputils-ping \
    build-essential \
    cmake \
    libpq-dev \
    python3-dev \
    gcc \
    g++ \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /application

# Copiar o arquivo de requisitos para o container
COPY requirements.txt /application/

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que será usada pela aplicação
EXPOSE 8501

# Copiar todo o código da aplicação para o container
COPY . /application/

# Definir uma variável de ambiente
ENV ENVIRONMENT=production

# Comando para iniciar a aplicação Streamlit
CMD ["streamlit", "run", "src/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
