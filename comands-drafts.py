'''########################## IMPLEMENTAÇÕES A FAZER ###################'''
- solicitações - atendimento online em tempo real - google meet
mensagem para cliente e explicação com link, instalar whatsapp no computado e google meet

Agendamento de atendimento

 - login por reconhecimento facial, e digital


'''#################################################################'''
 ansible ao alterar codigo, atualizar dentro do container
'''############################################'''


############################ TRASFERENCIA DIRETA SEM CONTAINER ################################

'''1. Transferência direta do projeto para o container rodando no servidor
Você pode copiar os arquivos atualizados do projeto diretamente para o container usando o comando docker cp. Isso evita a necessidade de recriar o container ou interromper seu funcionamento. Siga os passos abaixo:

Passos:
Transfira os arquivos do projeto para o servidor: No terminal local:'''

scp - r ~/aMosimann/aContabil/* mosimann@186.250.185.87: / home/mosimann/aContabil/

'''Copie os arquivos para dentro do container: No servidor:'''
docker cp / home/mosimann/aContabil/. mosimann-streamlit-1: / app/

'''Aqui, / app / é o diretório onde o código está localizado dentro do container. Certifique-se de ajustar o caminho conforme necessário.

Reinicie o serviço Streamlit dentro do container(se necessário): No servidor:'''

docker exec - it mosimann-streamlit-1 pkill - f streamlit
docker exec - it mosimann-streamlit-1 streamlit run main.py - -server.port 8501

'''2. Apagar e recriar o container(usando imagem atualizada)
Se você preferir uma abordagem mais limpa ou precisar de uma atualização mais abrangente(como alterações no ambiente Python), pode recriar o container.

Passos:
Atualize o código localmente e gere um novo .tar da imagem: No terminal local:'''

docker commit mosimann-streamlit-1 amosimann-streamlit-updated
docker save - o amosimann-streamlit-updated.tar amosimann-streamlit-updated
scp amosimann-streamlit-updated.tar mosimann@186.250.185.87: / home/mosimann/

'''Recrie o container no servidor: No servidor:'''
docker stop mosimann-streamlit-1
docker rm mosimann-streamlit-1
docker load - i / home/mosimann/amosimann-streamlit-updated.tar
docker run - d - -name mosimann-streamlit-1 - p 8501: 8501 amosimann-streamlit-updated

################################################ Docker ###########################################
# verificar redes existentes
docker network ls

# apagar rede
docker network rm application_application

# verificar qual networks o container está usando
docker inspect application-streamlit - -format '{{json .NetworkSettings.Networks}}'

docker inspect application-database - -format '{{json .NetworkSettings.Networks}}'

# testar containers estão se comunicando (ping)
docker exec application-streamlit ping - c 4 application-database


# instalar ping no container


# Entrar no container Docker do PostgreSQL (no servidor host):
docker exec - it application-database / bin/bash

Conectar ao Banco de Dados como Superusuário
Certifique-se de estar conectado ao banco de dados com o usuário postgres(superusuário) no contêiner do PostgreSQL:

# docker exec -it application-database psql -U mmss -d contabil
# docker exec -it application-database bash


''' Acessar o PostgreSQL dentro do container:'''
# psql
# psql -U postgres

# Verificar bancos disponíveis:
\l

\dt lista apenas tabelas no banco de dados atual.
\d exibe informações sobre objetos no banco de dados.
\d faces;


#verificar existencia da tabela
\dt clients;

'''# verificar nomes tabela faces'''
# SELECT username FROM faces;


'''#Verificar se está no banco de dados correto:'''
\c contabil 

#Criar banco de dados, se necessário:
CREATE DATABASE contabil;

#criar privilegios
GRANT ALL PRIVILEGES ON DATABASE contabil TO mmss;


'''# Acessar banco dados :'''
# psql -U mmss -d contabil
'''
perfeito ! vamos resolver acesso no navegador primeiro, o que deseja saber escreva os comandos para você obter as informações que precisa para me dar orientaçãos para solucionar o problema, não se esqueça o projeto está rodando no servidor a partir desses containers :

Se você ainda estiver tendo problemas de conexão após resolver o problema de espaço em disco, forneça mais detalhes sobre suas configurações de rede e firewall. Se você precisar de mais ajuda para liberar espaço em disco, liste os maiores diretórios usando du -sh * (no diretório raiz /) para que possamos ajudá-lo a identificar candidatos para exclusão. Lembre-se de fazer backups antes de qualquer exclusão importante.

#----------------------------------------------------
Em meu sistena ubuntu 24.04, vamos continuar a conseguir configurar tudo certo o Ansible , para automatizar processos no meu projeto , usando  python, streamlit, docker e postgreSql e Ansible, para quando eu fazer uma alteração no meu projeto ou no código ele já refletir as alterações no servidor mosimann@mosimaxdev:~$, então agora analise o arquivo ansible_logs1.txt anexado e verifique se tem problemas me oriente , escreva os comandos e me explique em detalhes para fazer correções caso tenha erros :  
'''
# ativar ambiente virtual  do servidor 
source /home/mosimann/aContabil/.venv/bin/activate


# Momento certo para executar o comando:
#O comando rsync deve ser executado sempre que houver alterações no código ou arquivos na sua máquina local que precisam ser atualizados no servidor remoto. Esse momento ocorre tipicamente durante as etapas de desenvolvimento ou deploy de um projeto
# Obs : Maquina local 
rsync -avz -e "ssh -p 8622" /home/jr/aMosimann/aContabil/ mosimann@186.250.185.87:/home/mosimann/aContabil/

################################################### ANSIBLE ###################################################
#apos alterar codigo do projeto, comando para efetura a trasferẽncia das alterações para o servidor
# no momento playbook.yml está configurado só para transf. aContabil , bancod de dados 'não'
ansible-playbook -i inventory.ini playbook.yml


# ansible_logs.txt
ansible-playbook -i inventory.ini playbook.yml -vvv | tee ansible_logs.txt

#parar container exemple comando 
docker stop contabil
# apagar 
docker rm contabil 

#apagar todas as imagens
docker rmi $(docker images -q)

# rodar container com senha
docker run -d --name mosimann-database -e POSTGRES_USER=mmss -e POSTGRES_PASSWORD=mmssmmnn -e POSTGRES_DB=contabil -p 5432:5432 postgres

docker run -d --name mosimann-streamlit -p 8501:8501 mosimann-streamlit:latest


# acessando e Usando o psql do Container
docker exec -it mosimann-database bash

# ou se quise só acessar o container
docker exec -it mosimann-database /bin/bash

docker exec -it mosimann-streamlit /bin/bash


#Então, execute o psql:
psql -U mmss -d contabil



#// atualizar ATUALIZAÇÃO DO PROJETO NO SERVIDOR //
git log origin/main --oneline   > verificar se você realmente fez o commit na máquina local

git status     #>para ferificar conflitos

git fetch origin     # > Garante que as referências remotas estão atualizadas no servidor.

git pull origin main

# forçar commit de novo na maquina local, mesmo que não haja mudança no código
git add .

git commit --amend --no-edit  # Isso mantém o commit anterior sem alterar a mensagem



Sempre que for atualizar o projeto no servidor, parar e deletar container no servidor e na maquina local

Agora que você removeu o container 

# Construa a IMAGEM novamente, imagens não precisam ser deletadas elas sobrescrevem
docker-compose up --build

# Exporte a imagem para um arquivo tar
# do banco
docker save postgres > application-database.tar
docker save application-python > application-python.tar

# Transferir a imagem para o servidor do projeto
# do banco 
scp -P 8622 application-database.tar mosimann@186.250.185.87:~/

scp -P 8622 application-python.tar mosimann@186.250.185.87:~/

scp -P 8622 Dockerfile mosimann@186.250.185.87:~/

scp -P 8622 init.sql mosimann@186.250.185.87:~/

scp -P 8622 docker-compose.yml mosimann@186.250.185.87:~/

# comando para saber o ip do container 
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mosimann-database

# Se precisar os arquivos dockerfile e docekr-compose.yml
scp -P 8622  ~/Mosimann/Dockerfile mosimann@186.250.185.87:/home/mosimann/
scp -P 8622  ~/Mosimann/docker-compose.yml mosimann@186.250.185.87:/home/mosimann/
scp -P 8622  ~/Mosimann/aConDockerfile mosimann@186.250.185.87:/home/mosimann/

# DO SERVIDOR PARA LOCAL
Para transferir o Dockerfile do servidor para a máquina local:
bash
Copiar código
scp -P 8622 mosimann@186.250.185.87:/home/mosimann/mosimann-database.tar ~/Mosimann/ 
scp -P 8622 mosimann@186.250.185.87:/home/mosimann/mosimann-streamlit.tar ~/Mosimann/ 
scp -P 8622 mosimann@186.250.185.87:/home/mosimann/Dockerfile ~/Mosimann/


Para transferir o docker-compose.yml do servidor para a máquina local:
bash
Copiar código
scp -P 8622 mosimann@186.250.185.87:/home/mosimann/docker-compose.yml ~/Mosimann/


docker cp mosimann-streamlit:/aContabil/data/relatorio_situationx.xlsx ./relatorio_situationx.xlsx



#Agora, no servidor, você vai importar a imagem que você transferiu e criar um novo container:
# Acesse o servidor via SSH (se ainda não estiver conectado)
ssh mosimann@186.250.185.87 -p 8622

# Pega o conteúdor .tar e recarrega para imagem Docker para o daemon do Docker no servidor
# Banco 
docker load < application-database.tar

docker load < application-python.tar

# Execute o novo container (escolha uma porta que não esteja em uso, como 8623)
# do Banco 
docker-compose up --build

docker run -d --name application-streamlit -p 8501:8501 application-python

docker run -d --name mosimann-database -e POSTGRES_PASSWORD=mmssmmnn -p 5432:5432 postgres
### para criar o banco atuomaticamente se quiser com o arquivo init.sql
docker run -d --name application-database \
  -e POSTGRES_USER=mmss \
  -e POSTGRES_PASSWORD=mmssmmnn \
  -e POSTGRES_DB=contabil \
  -p 5432:5432 \
  -v /home/application/init.sql:/docker-entrypoint-initdb.d/init.sql \
  postgres

#-------------------



docker run -d \
  --name application-database \
  -e POSTGRES_USER=mmss \
  -e POSTGRES_PASSWORD=mmssmmnn \
  -e POSTGRES_DB=contabil \
  -p 5432:5432 \
  postgres

# verificar se foi dada as permissões
docker exec -it mosimann-database psql -U mmss -d contabil
\l    -- Lista todos os bancos
\du   -- Lista todos os usuários e suas permissões

#entrar no psql do container como super usuario 
docker exec -it mosimann-mosiman-database psql -U postgres -d contabil
#liberar privleigios para banco 
GRANT ALL PRIVILEGES ON DATABASE contabil TO mmss;
GRANT ALL PRIVILEGES ON TABLE clients TO mmss;


# entrar no psql do container 
docker exec -it application-database psql -U mmss -d contabil

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL
);

INSERT INTO clients (name, email, phone) VALUES
('João Silva', 'joao.silva@example.com', '47987654321'),
('Maria Oliveira', 'maria.oliveira@example.com', '47987654322'),
('Pedro Souza', 'pedro.souza@example.com', '47987654323'),
('Ana Costa', 'ana.costa@example.com', '47987654324'),
('Carlos Pereira', 'carlos.pereira@example.com', '47987654325'),
('Fernanda Lima', 'fernanda.lima@example.com', '47987654326'),
('Lucas Alves', 'lucas.alves@example.com', '47987654327'),
('Juliana Martins', 'juliana.martins@example.com', '47987654328'),
('Gabriel Rocha', 'gabriel.rocha@example.com', '47987654329'),
('Amanda Santos', 'amanda.santos@example.com', '47987654330');

SELECT * FROM clients;

#verificar se o stremalit se comunica com banco 
docker logs mosimann-streamlit

1. Verificando os Logs do Container Streamlit
O Streamlit geralmente exibe mensagens de erro nos logs se não consegue se conectar ao banco de dados. Use este comando para inspecionar os logs:

bash
Copiar código
docker logs mosimann-streamlit
Procure por mensagens relacionadas a conexões com o banco de dados (por exemplo, falhas ou conexões bem-sucedidas).
2. Testando a Comunicação via Aplicação
Acesse o Streamlit no navegador:

URL: http://<IP_DO_SERVIDOR>:8501
Tente realizar uma operação no Streamlit que dependa do banco de dados, como inserir ou exibir clientes. Se a aplicação funcionar, a comunicação está estabelecida.

3. Inspecionando a Comunicação Diretamente do Streamlit
Se você tiver acesso ao terminal do container Streamlit, pode verificar diretamente no Python se a comunicação está funcionando.

Entre no container:

bash
Copiar código
docker exec -it mosimann-streamlit /bin/bash
Teste a conexão ao banco executando Python:

bash
Copiar código
python
E, dentro do Python:

python
Copiar código
import psycopg2

try:
    conn = psycopg2.connect(
        dbname="contabil",
        user="mmss",
        password="mmssmmnn",
        host="application-database",
        port="5432"
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")
Se o resultado for "Conexão bem-sucedida!", tudo está funcionando.

4. Utilizando pg_isready no Container Database
Verifique se o banco está pronto para conexões:

bash
Copiar código
docker exec -it mosimann-database pg_isready
Se o resultado indicar "accepting connections", o banco está operacional

Verifique a Rede do Docker: Certifique-se de que ambos os contêineres estão na mesma rede. Liste as redes disponíveis:

bash
Copiar código
docker network ls
Verifique se existe uma rede personalizada associada aos contêineres.

Reconstrua com Docker Compose (Recomendado): Se estiver usando o docker-compose.yml, ele já define uma rede comum entre os contêineres. Apenas garanta que ambos os serviços estão corretamente configurados no mesmo arquivo:

Adicione ambos os contêineres no arquivo docker-compose.yml com a mesma rede.
Certifique-se de que o nome da rede seja referenciado corretamente.
Exemplo:

yaml
Copiar código
version: '3.9'
services:
  mosimann-database:
    image: postgres:latest
    container_name: mosimann-database
    environment:
      POSTGRES_USER: mmss
      POSTGRES_PASSWORD: mmssmmnn
      POSTGRES_DB: contabil
    ports:
      - "5432:5432"
    networks:
      - mosimann_network

  mosimann-streamlit:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mosimann-streamlit
    ports:
      - "8501:8501"
    depends_on:
      - mosimann-database
    networks:
      - mosimann_network

networks:
  mosimann_network:
    driver: bridge
Execute novamente:

bash
Copiar código
docker-compose down
docker-compose up --build
Ajuste Manual na Rede: Caso prefira não usar docker-compose, adicione ambos os contêineres manualmente à mesma rede:

Crie uma rede personalizada:

bash
Copiar código
docker network create application
Conecte os contêineres à rede:

bash
Copiar código
# checar se estão na mesma rede
docker inspect mosimann-streamlit | grep -i "Network"
docker inspect mosimann-database | grep -i "Network"

Procure pela parte onde diz Networks, que mostrará a rede à qual cada contêiner está conectado.

2. Verificar a conexão do Streamlit com o banco de dados
Dentro do contêiner do Streamlit, verifique se o contêiner consegue se comunicar com o contêiner do banco de dados usando o comando ping ou nc (Netcat). Isso irá ajudar a garantir que a rede entre eles está funcional.

Primeiro, entre no contêiner do Streamlit:

bash
Copiar código
docker exec -it mosimann-streamlit /bin/bash
Agora, tente se conectar ao banco de dados usando o IP do contêiner do banco, que foi mostrado no docker inspect como 172.17.0.2. Você pode usar um dos seguintes comandos:

Verificar se o banco de dados está respondendo na porta 5432:

bash
Copiar código
nc -zv 172.17.0.2 5432
Ou, se o ping estiver instalado:

bash
Copiar código
ping 172.17.0.2



docker network connect mosimann_network mosimann-database
docker network connect mosimann_network mosimann-streamlit
Reinicie os contêineres:

bash
Copiar código
docker restart mosimann-database
docker restart mosimann-streamlit
Teste a Comunicação: Verifique se o contêiner do Streamlit consegue resolver o nome mosimann-database:

bash
Copiar código
docker exec -it mosimann-streamlit ping mosimann-database
Se o ping funcionar, o problema de rede foi resolvido.

Para verificar as redes disponíveis no Docker, use o comando:
docker network ls

# testa conexão com banco de dados 
psql -h 172.18.0.3 -U mmss -d contabil

### antes de executar o comando aqui debaixo verificar se o sistema está usando o .venv local do projeto e não global

# Não esquça de executar, pode ter dependencias novas :
pip install -r requirements.txt

#Se precisar aleateoriamente entrar no shell container
docker exec -it contabil bash

docker exec -it mosimann-streamlit /bin/bash


# ou então , que cria os containers a e sobe confor declaraçõe feito em arquivo como dockerfile etc... 
docker-compose up -d.  # mas tem que ter o docker instalado no ambiente do servidor , "não é o meu caso"

acessar pelo navegador:
http://186.250.185.87:8501

# Caso queira ordenar que o projeto rode em uma outra porta
docker run -d -p 8503:8501 --name contabil amosimann-streamlit

http://186.250.185.87:8503/

# caso precessa no navegador mas não abre , verifique 
docker logs contabil

######################################### COPIAR CONTAINER DO SERVIDOR PARA MÁQUINA LOCAL #####################
''' Sim, é possível copiar um contêiner Docker completamente configurado do servidor para sua máquina local, e a abordagem sugerida é válida. Aqui estão os passos detalhados: '''

Passo 1: Criar uma Imagem do Contêiner
Para transferir o contêiner, primeiro você precisa criar uma imagem Docker a partir do contêiner em execução no servidor:

bash
Copiar código
docker commit mosimann-mosiman-database-1 mosiman-database-image
Isso cria uma imagem chamada mosiman-database-image a partir do contêiner mosimann-mosiman-database-1.

Passo 2: Exportar a Imagem para um Arquivo .tar
Agora, exporte essa imagem para um arquivo .tar:

bash
Copiar código
docker save -o mosiman-database.tar mosiman-database-image
O arquivo mosiman-database.tar será criado no diretório atual.

Passo 3: Transferir o Arquivo para Sua Máquina Local
Use o comando scp para copiar o arquivo para sua máquina local:

scp -P 8622 mosimann@186.250.185.87:/path/to/mosiman-database.tar /local/path/
Substitua /path/to/ pelo caminho onde o arquivo .tar está salvo no servidor e /local/path/ pelo caminho onde deseja salvar o arquivo na sua máquina local.

Passo 4: Importar a Imagem na Máquina Local
Depois que o arquivo .tar estiver na sua máquina local, você pode importar a imagem no Docker:

bash
Copiar código
docker load -i /local/path/mosiman-database.tar
Isso criará a imagem mosiman-database-image na sua máquina local.

Passo 5: Rodar o Contêiner na Máquina Local
Por fim, você pode criar um novo contêiner a partir da imagem importada:

bash
Copiar código
docker run -d --name mosiman-mosiman-database-1 -p 5432:5432 mosiman-database-image
Isso iniciará o contêiner na sua máquina local, ouvindo na porta 5432
####################################Salva dados direto no banco de dados so servidor #############################################
1. Configurar o Acesso Remoto ao Banco de Dados no Servidor
Verifique se o PostgreSQL aceita conexões remotas:
No servidor, edite o arquivo postgresql.conf:

bash
Copiar código
sudo nano /var/lib/postgresql/data/postgresql.conf
(ou o caminho correto dependendo de onde o PostgreSQL foi configurado no Docker).

Localize a linha listen_addresses e configure para aceitar conexões de qualquer IP:

conf
Copiar código
listen_addresses = '*'
Salve o arquivo e reinicie o PostgreSQL dentro do contêiner:

bash
Copiar código
docker exec -it mosimann-mosiman-database-1 psql -U postgres
ou:

bash
Copiar código
docker restart mosimann-mosiman-database-1
Atualize as regras de acesso no arquivo pg_hba.conf:
Edite o arquivo pg_hba.conf dentro do contêiner:

bash
Copiar código
sudo nano /var/lib/postgresql/data/pg_hba.conf
Adicione a seguinte linha ao final do arquivo para permitir conexões de qualquer IP:

conf
Copiar código
host    all             all             0.0.0.0/0               md5
Salve e reinicie o PostgreSQL no contêiner novamente.

2. Configurar a Máquina Local
Alterar o arquivo de configuração do banco de dados no projeto local:
No código do projeto (provavelmente no arquivo database.py), altere o parâmetro host para apontar para o IP público do servidor onde o banco de dados está rodando.

Exemplo de alteração:

python
Copiar código
conn = psycopg2.connect(
    host="186.250.185.87",  # IP público do servidor
    port="5432",
    database="contabil",
    user="mmss",
    password="mmssmmnn"
)
3. Liberar a Porta no Firewall do Servidor
No servidor, certifique-se de que a porta 5432 está liberada para acesso externo:

bash
Copiar código
sudo ufw allow 5432
sudo ufw reload
Verifique o status do firewall para confirmar:

bash
Copiar código
sudo ufw status
4. Testar a Conexão Local
Você pode usar o arquivo test_db_connection.py para testar se a conexão está funcionando:

bash
Copiar código
python3 test_db_connection.py
Se a conexão for bem-sucedida, o projeto local deve ser capaz de salvar dados diretamente no banco de dados no servidor.

################################## ANSIBLE #############################
/home/jr/aMosimann
├── .venv
├── aContabil
│   ├── .git
│   ├── .gitignore
│   ├── .streamlit
│   ├── .venv
│   ├── backup.sql
│   ├── css
│   ├── data
│   ├── drafts
│   ├── img
│   ├── main.py
│   ├── mosimann-database.tar
│   ├── amosimann-streamlit.tar
│   ├── pagesx
│   ├── README.md
│   ├── requirements.txt
│   └── src
├── aAnsible
│   ├── ansible.cfg
│   ├── inventory.ini
│   ├── playbook.yml
│   └── roles
│       └── deploy_project
│           ├── tasks
│           │   └── main.yml
│           ├── files
│           │   ├── Dockerfile
│           │   ├── docker-compose.yml
│           │   └── database.py
│           └── templates
├── mosiman-comands.py
└── mosimann-database.tar


Estrutura e Conteúdo dos Arquivos Ansible em aAnsible
ansible.cfg
Este arquivo configura o comportamento do Ansible e aponta para o inventário e outras opções.
Conteúdo sugerido:

ini
Copiar código
[defaults]
inventory = inventory.ini
host_key_checking = False
retry_files_enabled = False
inventory.ini
Este arquivo contém os hosts e variáveis dos servidores que você deseja gerenciar.
Conteúdo sugerido:

ini
Copiar código
[web]
186.250.185.87 ansible_port=8622 ansible_user=mosimann ansible_ssh_private_key_file=~/.ssh/id_rsa
playbook.yml
Este é o arquivo principal do Ansible, onde você define as tarefas a serem executadas nos servidores.
Conteúdo sugerido:

yaml
Copiar código
- name: Implantar projeto aContabil
  hosts: web
  become: true
  tasks:
    - name: Copiar arquivos do projeto
      copy:
        src: "{{ item }}"
        dest: "/home/mosimann/aContabil/"
      with_items:
        - roles/deploy_project/files/Dockerfile
        - roles/deploy_project/files/docker-compose.yml
        - roles/deploy_project/files/database.py

    - name: Subir containers com Docker Compose
      command: docker-compose up -d
      args:
        chdir: "/home/mosimann/aContabil"
Arquivos na subpasta roles/deploy_project/files
Esses arquivos são os que você precisa copiar para o servidor. Coloque o Dockerfile, docker-compose.yml, e database.py aqui.

roles/deploy_project/tasks/main.yml
Este arquivo organiza as tarefas relacionadas ao projeto.
Conteúdo sugerido:

yaml
Copiar código
- name: Copiar arquivos do projeto
  copy:
    src: "{{ item }}"
    dest: "/home/mosimann/aContabil/"
  with_items:
    - files/Dockerfile
    - files/docker-compose.yml
    - files/database.py

- name: Subir containers com Docker Compose
  command: docker-compose up -d
  args:
    chdir: "/home/mosimann/aContabil"
Criar os Arquivos no Visual Studio Code
Abra o VS Code e navegue até a pasta aAnsible.

Crie os arquivos acima manualmente ou com os comandos do terminal:

bash
Copiar código
touch ansible.cfg inventory.ini playbook.yml
mkdir -p roles/deploy_project/{tasks,files,templates}
touch roles/deploy_project/tasks/main.yml
Preencha os conteúdos conforme mostrado.

Configurar o Visual Studio Code para Reconhecer Ansible
Instale a extensão Ansible:

No VS Code, abra a aba de extensões (Ctrl+Shift+X).
Pesquise por "Ansible" e instale a extensão oficial da Red Hat.
Configuração do ambiente:

Certifique-se de que o Python e o Ansible estão instalados na máquina local.
Use o comando abaixo para instalar o Ansible no ambiente local (se ainda não tiver):
bash
Copiar código
pip install ansible
No VS Code, configure o interpretador Python correto na barra inferior.
Ative a linting e o autocomplete para Ansible:
A extensão da Red Hat oferece verificação de sintaxe e linting. Com isso, o VS Code irá validar seus arquivos YAML automaticamente.

Como Usar
Depois de configurar tudo, execute o comando para rodar o playbook no terminal:

bash
Copiar código
ansible-playbook -i inventory.ini playbook.yml
Verifique os logs do Ansible para confirmar se as tarefas foram realizadas com sucesso.

Com essa estrutura, alterações feitas nos arquivos locais podem ser facilmente aplicadas no servidor.






Você disse:
comando para verificar se o Ansible está instalado no meu ubuntu 24.04 :
O ChatGPT disse:
ChatGPT
Para verificar se o Ansible está instalado no seu Ubuntu 24.04, você pode usar o seguinte comando no terminal:

bash
Copiar código
ansible --version
Possíveis resultados:
Ansible está instalado:
O comando mostrará a versão instalada e outros detalhes, como o local do arquivo de configuração e as versões das bibliotecas.

Exemplo de saída:

plaintext
Copiar código
ansible [core 2.14.5]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.10/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.10.12 (default, Sep 15 2024, 12:00:00) [GCC 11.3.0]
Ansible não está instalado:
Você verá um erro como este:

plaintext
Copiar código
Command 'ansible' not found, but can be installed with:
sudo apt install ansible
Para instalar o Ansible (se não estiver instalado):
Atualize o gerenciador de pacotes:
bash
Copiar código
sudo apt update
Instale o Ansible:
bash
Copiar código
sudo apt install ansible -y
Após a instalação, repita o comando ansible --version para confirmar.

1. Ansible version
plaintext
Copiar código
ansible [core 2.16.3]
ansible: Indica que o comando Ansible foi detectado e está funcional.
[core 2.16.3]: A versão do núcleo do Ansible instalada no sistema. Neste caso, é a versão 2.16.3.
2. Config file
plaintext
Copiar código
config file = None
Indica que nenhum arquivo de configuração padrão (ansible.cfg) está sendo usado atualmente.
O Ansible geralmente busca este arquivo em locais predefinidos, como:
O diretório atual
/etc/ansible/ansible.cfg
Diretórios específicos definidos em variáveis de ambiente.
Como resolver: Se você precisa de um arquivo ansible.cfg para personalizar sua configuração, você pode criá-lo no diretório atual do seu projeto ou em /etc/ansible/.
3. Configured module search path
plaintext
Copiar código
configured module search path = ['/home/jr/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
Module search path: Lista de diretórios onde o Ansible procura por módulos (pequenos scripts usados para executar tarefas).
No seu caso:

Diretórios específicos do usuário (/home/jr/.ansible/plugins/modules).
Diretórios globais do sistema (/usr/share/ansible/plugins/modules).
Configuração personalizada: Se necessário, você pode adicionar mais caminhos em seu arquivo ansible.cfg na seção [defaults].

4. Ansible Python module location
plaintext
Copiar código
ansible python module location = /usr/lib/python3/dist-packages/ansible
Indica o diretório onde o módulo Python principal do Ansible está instalado no sistema.
Local padrão no Ubuntu: /usr/lib/python3/dist-packages/.
5. Collection location
plaintext
Copiar código
ansible collection location = /home/jr/.ansible/collections:/usr/share/ansible/collections
Coleções: Um conjunto de módulos, plugins e roles agrupados para facilitar o uso.
O Ansible busca coleções nesses diretórios:

Diretório do usuário (/home/jr/.ansible/collections).
Diretório global do sistema (/usr/share/ansible/collections).
Por que importa?
Ao instalar ou criar coleções, elas serão salvas em um desses diretórios.

6. Executable location
plaintext
Copiar código
executable location = /usr/bin/ansible
O caminho completo para o executável ansible.
Isso confirma que o Ansible foi instalado corretamente e está localizado em um diretório no PATH do sistema.
7. Python version
plaintext
Copiar código
python version = 3.12.3 (main, Sep 11 2024, 14:17:37) [GCC 13.2.0] (/usr/bin/python3)
Mostra que o Ansible está usando o Python versão 3.12.3, instalado no sistema.
Detalhes adicionais:
Compilador: GCC 13.2.0.
Caminho do Python: /usr/bin/python3.
8. Jinja version
plaintext
Copiar código
jinja version = 3.1.2
O Ansible usa o Jinja2 como mecanismo de templates.
Essa versão é usada para renderizar arquivos de templates, como YAML e HTML.
9. LibYAML
plaintext
Copiar código
libyaml = True
Indica que a biblioteca LibYAML está habilitada.
Por que é importante? LibYAML melhora o desempenho na leitura e processamento de arquivos YAML. Isso é recomendado para ambientes com grandes playbooks.
Resumo
Sua instalação está configurada corretamente com:

Ansible versão: 2.16.3
Python versão: 3.12.3
Jinja versão: 3.1.2
LibYAML: habilitada, para desempenho melhorado.

###################################### SEGURANÇA DE CÓDIGO ########################################
Proteger o código de um sistema em Python contra acesso e roubo por pessoas com acesso ao servidor é um desafio, pois os scripts Python são interpretados e não compilados, o que os torna mais expostos. No entanto, há várias medidas que você pode tomar para dificultar o acesso ao código ou minimizar o risco de roubo. Aqui estão as melhores práticas:

1. Controle de Acesso ao Servidor
Usuários limitados: Restrinja o acesso ao servidor apenas a pessoas essenciais. Use mecanismos como chaves SSH e nunca compartilhe senhas.
Segregação de funções: Crie usuários diferentes no servidor para cada função (desenvolvimento, administração, execução). O usuário que roda o código, por exemplo, pode ter permissões limitadas de leitura sem acesso aos scripts.
Auditoria de acesso: Ative logs detalhados para rastrear quem acessou o servidor, o que foi feito e quando.
2. Ofuscação do Código
Embora a ofuscação não torne o código impenetrável, dificulta a leitura e a compreensão:

Ferramentas de ofuscação: Use ferramentas como PyArmor ou Cython para converter seus scripts em arquivos binários ou ofuscados.
PyArmor: Ofusca o código e adiciona licenciamento baseado no hardware onde o código é executado.
Cython: Transforma os scripts Python em extensões compiladas (arquivos .so no Linux ou .pyd no Windows).
3. Execute o Código em Containers
Isolamento em Docker: Configure o sistema para rodar dentro de containers Docker. Dessa forma:
Apenas os binários ou os arquivos necessários são incluídos no container.
Configure volumes de forma que o código-fonte não fique diretamente acessível no sistema de arquivos do container.
Imagem de produção enxuta: Crie uma versão "buildada" do sistema, sem incluir o código-fonte original. Use ferramentas como docker build para criar imagens contendo apenas os binários gerados por Cython ou PyArmor.
4. Configure Permissões no Sistema de Arquivos
Permissões restritas: Certifique-se de que os arquivos do código sejam acessíveis apenas pelo usuário que executa o sistema.
bash
Copiar código
chmod -R 700 /caminho/do/codigo
chown -R usuario_aplicacao:grupo_aplicacao /caminho/do/codigo
Impeça root sem senha: Restrinja acesso ao usuário root para evitar que qualquer pessoa com acesso possa escalar permissões.
5. Proteger o Banco de Dados
Não armazene chaves sensíveis no código: Use variáveis de ambiente ou serviços de gerenciamento de segredos (como AWS Secrets Manager ou HashiCorp Vault) para armazenar informações sensíveis.
Restrinja o acesso ao banco de dados: Configure regras de firewall e permissões para que apenas o container ou servidor da aplicação possa acessar o banco.
6. Logs e Auditoria
Monitoramento contínuo: Use ferramentas de monitoramento (como CloudWatch, Splunk, ou Prometheus) para detectar acessos ou alterações não autorizadas.
Logs centralizados: Armazene logs de auditoria fora do servidor de aplicação, garantindo que não sejam apagados.
7. Execute em Servidor Gerenciado ou Ambientes Remotos
Serviços de execução gerenciada: Em vez de hospedar o sistema em servidores tradicionais, considere usar ambientes gerenciados como AWS Lambda, Google Cloud Run ou Azure App Services. Assim, você delega a execução ao provedor e mantém o código fora do alcance direto dos operadores.
Streaming de lógica: Transforme parte da lógica do sistema em APIs gerenciadas externamente e reduza o código sensível no servidor.
8. Licenciamento do Código
Se você planeja distribuir ou permitir acesso remoto ao sistema:

Ative mecanismos de licenciamento: Use ferramentas como PyArmor para limitar o uso do código ao hardware específico ou a um período de tempo.
9. Virtualização Completa do Código
Rode como um serviço remoto: Mantenha o código completo em um servidor ou serviço e disponibilize apenas uma interface para uso (como APIs). Isso elimina a necessidade de expor o código em um servidor de terceiros.
10. Criptografia do Código
Embora raro em Python, você pode criar uma camada extra de proteção criptografando os scripts e implementando um mecanismo de desbloqueio temporário no runtime (dentro do servidor):

Exemplo com PyCrypto ou Cryptography:
Criptografe os scripts no local de desenvolvimento.
Configure o servidor para descriptografá-los dinamicamente na memória durante a execução.
Considerações Finais
Mesmo com todas essas práticas, é importante lembrar que nenhum sistema é 100% invulnerável. O objetivo é aumentar a dificuldade e reduzir o incentivo para que alguém tente roubar ou modificar o código.

Se a segurança do código é crítica, considere combinar várias dessas estratégias. Fique à vontade para implementar e perguntar sobre detalhes técnicos específicos!

############################################### ATUTOMAÇÃO PROFISSIONAL #########################################
agora me responda uma pergunta : quando fizer uma alterção no meu código qual é a forma prática e profissional para atualizar o projeto dentro do container no servidor ?  ou se eu mudar apenas uma linha de codigo do projeto na minha máquina local, tenho reconstruir todo o container e transferir tudo de novo para o servidor ?
O ChatGPT disse:
ChatGPT
A forma prática e profissional de atualizar o código dentro do container no servidor sem precisar reconstruir todo o ambiente e transferir novamente tudo do zero depende do seu fluxo de trabalho e das ferramentas que você utiliza. Aqui estão algumas abordagens que podem ser úteis para seu caso:

1. Usando Volumes no Docker
Uma forma eficiente de manter o código atualizado no container sem reconstruir o ambiente todo é utilizar volumes. Os volumes permitem que você faça modificações no código localmente e veja essas mudanças refletidas diretamente no container sem precisar reconstruir a imagem.

Como funciona: No seu docker-compose.yml, você já tem o seguinte volume configurado:

yaml
Copiar código
volumes:
  - ./aContabil:/aContabil
Esse volume faz com que o diretório ./aContabil da sua máquina local seja sincronizado com o diretório /aContabil dentro do container. Ou seja, sempre que você alterar um arquivo no diretório aContabil da sua máquina local, a mudança será refletida no container automaticamente.

Vantagem: Com isso, você pode atualizar o código no container apenas modificando os arquivos locais, sem precisar reconstruir o container. Isso é rápido e eficiente para alterações pequenas, como mudanças em uma linha de código, alterações em arquivos de configuração, etc.

Quando usar: Ideal para ajustes rápidos no código, como testes e pequenas correções.

2. Usando Git para Deploy no Servidor
Outra abordagem profissional é versionar seu código usando Git e, em seguida, fazer o deploy no servidor quando houver mudanças.

Como funciona:

Inicialize um repositório Git no seu projeto, se ainda não o fez.
Faça um push para o repositório remoto (GitHub, GitLab, etc.).
No servidor, faça o pull do repositório remoto para obter as mudanças mais recentes.
Reinicie o container para que ele utilize o novo código (ou, se estiver utilizando volumes, basta reiniciar o serviço).
Comando básico de Git no servidor:

bash
Copiar código
cd /caminho/do/seu/projeto
git pull origin main  # ou o nome do seu branch
docker-compose restart mosimann-streamlit  # Reinicia o container com o novo código
Vantagem: Esse processo mantém o histórico do seu código e permite um controle maior sobre o que foi alterado e quando. É ideal para mudanças maiores e em ambientes de produção, pois facilita a recuperação de versões anteriores.

3. Reconstruir e Atualizar o Container
Em casos onde você faz alterações significativas no seu ambiente ou nas dependências do projeto (por exemplo, instalação de novos pacotes no requirements.txt), será necessário reconstruir o container.

Como fazer:

Atualize seu código localmente.
Faça qualquer alteração necessária no requirements.txt ou em outros arquivos de configuração.
Reconstrua a imagem com o comando docker-compose up --build.
Reinicie o container.
Comando básico:

bash
Copiar código
docker-compose up --build   # Reconstrua e reinicie todos os containers
Quando usar: Esse método é necessário quando há alterações que impactam o ambiente, como a adição de novas dependências ou a atualização de arquivos de configuração que necessitam de uma nova construção do ambiente.

4. Usando CI/CD para Automação de Deploy
Em um ambiente mais profissional e de produção, é interessante ter um fluxo de Integração Contínua (CI) e Deploy Contínuo (CD). Com isso, quando você faz alterações no código, o deploy no servidor pode ser automatizado, e os containers podem ser atualizados automaticamente.

Como funciona: Configure pipelines no seu serviço de CI/CD (como GitHub Actions, GitLab CI, Jenkins, etc.) para construir e testar o código sempre que você fizer push para o repositório. O pipeline pode incluir a construção de uma nova imagem Docker e o deploy no servidor.

Vantagem: Automatiza todo o processo e elimina a necessidade de intervenção manual para atualizar o código no servidor.

Resumo:
Para pequenas alterações no código (como uma linha de código), o uso de volumes Docker é o método mais eficiente, pois o código será sincronizado automaticamente com o container.
Para alterações mais complexas (como mudanças em dependências ou arquivos de configuração), o ideal é reconstruir o container com docker-compose up --build.
Usar Git no servidor é uma boa prática para controlar versões e garantir que as atualizações sejam consistentes.





Você disse:
você nao citou o Ansible na sua ultima resposta porquê ? não é necessário , ja tem um ferramenta que faz o serviço do Ansible, me explique em detalhes , inclusive também o que é ansible ?
O ChatGPT disse:
ChatGPT
Você está absolutamente certo em mencionar o Ansible! Eu não citei o Ansible diretamente na minha resposta anterior porque a abordagem que sugeri estava focada em um fluxo de trabalho manual (volumes, Git, reconstrução de containers), mas o Ansible é, sem dúvida, uma ferramenta muito útil e poderosa, especialmente em ambientes de produção ou quando há necessidade de automação de tarefas repetitivas e complexas.

O que é o Ansible?
Ansible é uma ferramenta de automação de TI que facilita a configuração de sistemas, o gerenciamento de servidores e o deploy de aplicativos de forma eficiente e segura. O Ansible foi criado para automatizar tarefas como:

Gerenciamento de configuração: definir e aplicar configurações em servidores.
Deploy de aplicativos: automatizar o processo de deploy de código.
Provisionamento de infraestrutura: configurar novos servidores, instalar pacotes, entre outros.
Orquestração de tarefas: coordenar a execução de várias tarefas em diferentes servidores ao mesmo tempo.
Ele é amplamente utilizado para automação de infraestrutura e orquestração de containers, entre outras funções, e possui a vantagem de ser extremamente simples de usar, especialmente por ser baseado em arquivos YAML (em vez de scripts complexos), o que facilita a leitura e a manutenção dos playbooks (conjuntos de tarefas).

Como o Ansible funciona?
Ansible usa playbooks que são arquivos em YAML (Yet Another Markup Language) que descrevem as ações que devem ser realizadas nos servidores. Um playbook do Ansible pode ser usado para:

Instalar pacotes, como python3, git, docker, etc.
Configurar serviços, como o PostgreSQL ou o seu serviço Streamlit.
Fazer deploy de código, como copiar arquivos, reiniciar containers, etc.
Automatizar o gerenciamento de containers Docker.
Principais Componentes do Ansible:
Playbooks: Arquivos em YAML que definem as ações que o Ansible executará.
Hosts: Definem os servidores (ou containers) onde o Ansible executará as ações.
Módulos: Unidades de trabalho do Ansible (por exemplo, o módulo docker_container para interagir com containers Docker).
Inventário: Define os servidores que serão gerenciados, pode ser um arquivo estático ou dinâmico.
Roles: Uma maneira de organizar e compartilhar playbooks e tarefas comuns.
Como o Ansible pode ser usado para o seu caso?
No seu cenário, o Ansible pode ser utilizado para automatizar a configuração e o deploy do seu ambiente no servidor. Por exemplo, ele pode:

Instalar e configurar o Docker no servidor.
Subir os containers usando Docker Compose.
Realizar deploy do código no servidor (fazendo pull de um repositório Git ou copiando os arquivos para o servidor).
Realizar a atualização do código dentro dos containers.
Essa automação pode ser configurada em playbooks, de forma que você não precise se preocupar em manualmente transferir arquivos ou executar comandos no servidor.

Exemplo de Playbook do Ansible para seu caso:
Abaixo está um exemplo básico de como um playbook do Ansible pode ser configurado para automatizar o deploy do seu projeto e o gerenciamento do Docker.

1. Playbook para instalar dependências (Docker, Git, etc.)
yaml
Copiar código
---
- name: Setup Server for Docker and Git
  hosts: all
  become: yes

  tasks:
    - name: Install Docker
      apt:
        name: docker.io
        state: present

    - name: Install Docker Compose
      get_url:
        url: https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)
        dest: /usr/local/bin/docker-compose
        mode: 'u+x'

    - name: Install Git
      apt:
        name: git
        state: present
2. Playbook para Deploy do código
Este playbook pode ser usado para pegar o código do repositório remoto, colocar os arquivos no servidor e reiniciar o container.

yaml
Copiar código
---
- name: Deploy Streamlit Application
  hosts: all
  become: yes
  tasks:
    - name: Pull the latest code from Git repository
      git:
        repo: 'https://github.com/your/repo.git'
        dest: /home/user/aContabil
        version: master

    - name: Build and start Docker containers
      docker_compose:
        project_src: /home/user/aContabil
        restarted: yes
3. Playbook para Gerenciar o Docker
Aqui está um exemplo de como você pode usar o Ansible para gerenciar containers Docker diretamente (parar, reiniciar, etc.):

yaml
Copiar código
---
- name: Manage Docker containers
  hosts: all
  become: yes

  tasks:
    - name: Ensure container is running
      docker_container:
        name: mosimann-streamlit
        image: mosimann-streamlit:latest
        state: started
        restart_policy: unless-stopped
Vantagens de Usar o Ansible:
Automatização: Você pode automatizar todo o processo de configuração e deploy do seu ambiente no servidor. Isso garante que o processo seja repetível e que não haja erros humanos.
Gerenciamento Centralizado: Com o Ansible, você pode gerenciar múltiplos servidores a partir de um único playbook. Isso é útil se você tiver mais de um servidor ou container.
Escalabilidade: Se no futuro você precisar expandir o número de containers ou servidores, o Ansible facilita esse processo, permitindo escalar facilmente a infraestrutura.
Consistência: Ao usar o Ansible, todos os servidores e containers são configurados da mesma maneira, o que ajuda a garantir que o ambiente de produção seja consistente.
Resumo:
Ansible é uma ferramenta extremamente útil para automatizar o deploy e gerenciamento de configurações. Ele pode facilitar o processo de atualizar seu código e gerenciar containers sem precisar de intervenção manual.
Você pode usá-lo para automação de infraestrutura, deploy de código e gerenciamento de containers, poupando tempo e reduzindo erros.
#######################################################################################
Alteração do pg_hba.conf:
#entrar no  container e no psql para acessar o arquivo dentro do container mosimann-database
docker exec -it mosimann-database /bin/bash

#se precisar entar psql
docker exec -it mosimann-database psql -U mmss -d contabil

#Dentro do container, navegue até o diretório onde o arquivo está localizado:
cd /var/lib/postgresql/data

#Certifique-se de que o arquivo existe:
ls -l pg_hba.conf

#editar com nano senão instalar com apt install nano 


#Primeiro, confira as permissões do arquivo pg_hba.conf:
ls -l /var/lib/postgresql/data/pg_hba.conf

#Se as permissões forem restritas, você pode alterá-las temporariamente para edição:
chmod u+w /var/lib/postgresql/data/pg_hba.conf

#acessar o arqueivo
/var/lib/postgresql/data/pg_hba.conf

# dentro do containerv por linha de comando 
echo "host    all             all             0.0.0.0/0            trust" >> /var/lib/postgresql/data/pg_hba.conf

#Recarregue a configuração do PostgreSQL: Depois de editar o arquivo, recarregue as configurações do banco de dados para aplicar as mudanças:

# dentro do containier Adicionamos a seguinte linha ao arquivo para permitir conexões de qualquer IP:
host    all             all             0.0.0.0/0            trust

#Recarregamos as configurações do PostgreSQL:
docker exec -it mosimann-database psql -U mmss -d contabil -c "SELECT pg_reload_conf();"

#Alteração do código no arquivo database.py:
conn = psycopg2.connect(
    host="mosimann-database",
    port="5432",
    database="contabil",
    user="mmss",
    password="mmssmmnn"
)

#Testamos a conectividade manualmente:
#Entramos no container do Streamlit e rodamos um script de teste:
python
import psycopg2
try:
    conn = psycopg2.connect(
        host="mosimann-database",
        port="5432",
        database="contabil",
        user="mmss",
        password="mmssmmnn"
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro: {e}")
    
    
Ajustamos o Docker Network:

Certificamo-nos de que ambos os containers estavam na mesma rede do Docker (mosimann_network):
docker network inspect mosimann_network

#Verifique o pg_hba.conf: Certifique-se de que a linha abaixo está no arquivo:
host    all             all             0.0.0.0/0            trust

#Reinicie o banco de dados para aplicar alterações:
docker restart mosimann-database

#Teste a conectividade do Python:
docker exec -it mosimann-streamlit /bin/bash
# no src testeo a conexao
python3 test_db_connection.py

#Reinicie os containers se necessário:

#4. Certifique-se de que o PostgreSQL está escutando em todas as interfaces

#Edite o arquivo postgresql.conf para confirmar que o PostgreSQL está configurado para aceitar conexões externas:
echo "listen_addresses = '*'" >> /var/lib/postgresql/data/postgresql.conf

#5. Reinicie o container se necessário
Caso as alterações não surtam efeito, reinicie o container:

######################### desconectar e conectar em outra rede networks ###################
Conecte o container application-database à rede application_application:
Desconecte o container da rede atual (mosimann_application):

bash
Copiar código
docker network disconnect mosimann_application application-database
Conecte-o à rede application_application:

bash
Copiar código
docker network connect application_application application-database
2. Conecte o container application-streamlit à rede application_application:
Desconecte o container da rede atual (bridge):

bash
Copiar código
docker network disconnect bridge application-streamlit
Conecte-o à rede application_application:

bash
Copiar código
docker network connect application_application application-streamlit
3. Verifique a configuração de rede dos containers:
Execute os comandos abaixo para confirmar que ambos os containers estão na mesma rede application_application:

bash
Copiar código
docker inspect application-database --format '{{json .NetworkSettings.Networks}}'
docker inspect application-streamlit --format '{{json .NetworkSettings.Networks}}'
Eles devem exibir a rede application_application como parte de suas configurações.

##################################### COMANDOS DOCKER EXEC #########################################################
# Copiar o arquivo de chave SSH para o container
docker_command_1 = """
docker cp /home/mosimann/id_ed25519 mosimann-streamlit:/root/.ssh/id_ed25519
'''
Este comando copia o arquivo de chave SSH (id_ed25519) do diretório local /home/mosimann/ para o diretório /root/.ssh/ dentro do container mosimann-streamlit.
'''
"""

# Alterar as permissões do arquivo de chave SSH dentro do container
docker_command_2 = """
docker exec mosimann-streamlit /bin/bash -c "chmod 600 /root/.ssh/id_ed25519"
'''
Este comando executa o chmod 600 no arquivo de chave SSH dentro do container. A permissão 600 permite apenas leitura e escrita pelo proprietário do arquivo, garantindo segurança para o uso da chave SSH.
'''
"""

# Adicionar a chave pública do GitHub ao arquivo known_hosts
docker_command_3 = """
docker exec mosimann-streamlit /bin/bash -c "ssh-keyscan github.com >> /root/.ssh/known_hosts"
'''
Este comando usa o ssh-keyscan para pegar a chave SSH pública do GitHub e adicioná-la ao arquivo known_hosts. Isso permite que o container confie na conexão SSH com o GitHub, evitando o aviso de chave desconhecida.
'''
"""

# Testar a autenticação SSH com o GitHub
docker_command_4 = """
docker exec mosimann-streamlit /bin/bash -c "ssh -T git@github.com"
'''
Este comando testa a autenticação SSH com o GitHub. A resposta "You've successfully authenticated" indica que a chave SSH foi configurada corretamente.
'''
"""

# Fazer um pull das alterações do repositório Git
docker_command_5 = """
docker exec mosimann-streamlit /bin/bash -c "cd /aContabil && git pull origin main"
'''
Este comando navega até o diretório /aContabil dentro do container e faz um git pull para trazer as últimas alterações do branch main do repositório remoto.
'''
"""

# Adicionar todas as alterações ao índice do Git e realizar um commit
docker_command_6 = """
docker exec mosimann-streamlit /bin/bash -c "cd /aContabil && git add . && git commit -m 'Commit local changes'"
'''
Esse comando adiciona todas as mudanças no diretório /aContabil ao índice do Git e cria um commit com a mensagem 'Commit local changes'.
'''
"""

# Configurar o nome e e-mail do autor do commit no Git dentro do container
docker_command_7 = """
docker exec mosimann-streamlit /bin/bash -c "git config --global user.email 'domingoshot@hotmail.com'"
docker exec mosimann-streamlit /bin/bash -c "git config --global user.name 'gilberto-domingos'"
'''
Esses comandos configuram o nome e o e-mail do usuário globalmente para o Git dentro do container, permitindo que os commits sejam feitos corretamente.
'''
"""

# Habilitar o rebase para resolver divergências entre branches ao puxar alterações
docker_command_8 = """
docker exec mosimann-streamlit /bin/bash -c "git config --global pull.rebase false"
'''
Este comando configura o Git para não usar rebase ao fazer um git pull, forçando-o a usar merge em vez disso, quando houver divergências entre os branches.
'''
"""

# Fazer novamente o pull, agora com a opção de merge habilitada
docker_command_9 = """
docker exec mosimann-streamlit /bin/bash -c "cd /aContabil && git pull origin main"
'''
Este comando faz o git pull novamente, agora com a configuração de merge, resultando em conflitos que precisarão ser resolvidos manualmente.
'''
"""

# Verificar o status do repositório Git após o pull com conflitos
docker_command_10 = """
docker exec mosimann-streamlit /bin/bash -c "cd /aContabil && git status"
'''
Este comando exibe o status do repositório, mostrando que existem arquivos em conflito que precisam ser resolvidos antes de finalizar o merge.
'''
"""

# Entrar no container para editar um arquivo com conflitos
docker_command_11 = """
docker exec -it mosimann-streamlit /bin/bash
nano /aContabil/css/comp.css
'''
Este comando abre um terminal interativo dentro do container e usa o nano para editar o arquivo comp.css, que tem conflitos após o git pull.
'''
"""

# Sair do container após editar o arquivo
docker_command_12 = """
exit
'''
Este comando sai do terminal interativo dentro do container, retornando ao terminal local.
'''
"""


############################ CONFIGURAÇÃO VS CODE ##########################F
code ~/.config/Code/User/settings.json

{
  "security.workspace.trust.untrustedFiles": "open",
  "workbench.iconTheme": "vscode-icons",
  "editor.fontLigatures": true,
  "editor.fontFamily": "Fira Code",
  "workbench.startupEditor": "none",
  "terminal.integrated.fontFamily": "FiraCode Nerd Font Mono",
  "terminal.integrated.gpuAcceleration": "on",
  "vsicons.dontShowNewVersionMessage": true,
  "python.formatting.provider": "autopep8",
  "python.formatting.autopep8Path": "/home/jr/application/.venv/bin/autopep8",
  "editor.formatOnSave": true
}

######################################### IMPORTAÇÃO DOS DADOS .XLSX PARA O POSGRESQL ########################
import pandas as pd
import psycopg2

# Lê o arquivo Excel
df = pd.read_excel('caminho/do/arquivo/empresas.xlsx', sheet_name='Página 1')

# Renomeia as colunas para corresponder à tabela PostgreSQL
df.columns = ['codigo', 'razao_social', 'descricao_natureza_juridica', 
              'forma_tributacao', 'celula', 'email', 'telefone']

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    database="nome_do_banco",
    user="usuario",
    password="senha",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Inserção dos dados na tabela
for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO empresas (codigo, razao_social, descricao_natureza_juridica, "
        "forma_tributacao, celula, email, telefone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (row['codigo'], row['razao_social'], row['descricao_natureza_juridica'],
         row['forma_tributacao'], row['celula'], row['email'], row['telefone'])
    )

# Confirma as alterações e fecha a conexão
conn.commit()
cursor.close()
conn.close()

'''#######################################################################################'''
# -------------------------
import streamlit as st


def apply_light_theme():
    primary_color = "#FF4B4B"
    background_color = "#ffffff"
    secondary_background_color = "#F0F2F6"
    text_color = "#31333F"
    font = "sans serif"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background_color};
        }}
        .stSidebar {{
            background-color: {secondary_background_color};
        }}
        .stButton>button {{
            background-color: {primary_color};
            color: {text_color};
        }}
        body {{
            font-family: {font};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def apply_dark_theme():
    primary_color = "#e31b22"
    background_color = "#0E1117"
    secondary_background_color = "#262730"
    text_color = "#fafafa"
    font = "sans serif"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background_color};
        }}
        .stSidebar {{
            background-color: {secondary_background_color};
        }}
        .stButton>button {{
            background-color: {primary_color};
            color: {text_color};
        }}
        body {{
            font-family: {font};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def show():
    # Inicializar o estado do tema
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Escuro"

    # Alternar o tema quando o toggle for alterado
    on = st.toggle("🌓 Claro/Escuro", key="theme_toggle",
                   value=st.session_state["theme"] == "Claro")

    if on:
        st.session_state["theme"] = "Claro"
    else:
        st.session_state["theme"] = "Escuro"

    # Aplicar o tema atual
    if st.session_state["theme"] == "Claro":
        apply_light_theme()
    else:
        apply_dark_theme()


# Chamar a função show()
if __name__ == "__main__":
    show()


///////////////////////////////////////////////////////////


def apply_light_theme():
    """Aplica o tema claro na página."""
    primary_color = "#FF4B4B"
    background_color = "#ffffff"
    secondary_background_color = "#F0F2F6"
    text_color = "#31333F"
    font = "sans serif"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background_color};
        }}
        .stSidebar {{
            background-color: {secondary_background_color};
        }}
        .stButton>button {{
            background-color: {primary_color};
            color: {text_color};
        }}
        body {{
            font-family: {font};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def apply_dark_theme():
    """Aplica o tema escuro na página."""
    primary_color = "#e31b22"
    background_color = "#0E1117"
    secondary_background_color = "#262730"
    text_color = "#fafafa"
    font = "sans serif"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background_color};
        }}
        .stSidebar {{
            background-color: {secondary_background_color};
        }}
        .stButton>button {{
            background-color: {primary_color};
            color: {text_color};
        }}
        body {{
            font-family: {font};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


[theme]
base = "light"
secondaryBackgroundColor = "#ffffff"

[theme]
base = "dark"
backgroundColor = "#262730"


**/.git
autopep8 - -aggressive - - in -place seu_arquivo.py
