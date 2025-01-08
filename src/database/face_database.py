import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(
                    dbname="contabil",
                    user="mmss",
                    password="mmssmmnn",
                    host="186.250.185.87",
                    port=5432
                )
                print("Conexão com o banco de dados estabelecida.")
            except psycopg2.Error as e:
                self.conn = None
                raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def ensure_connection(self):
        if self.conn is None or self.conn.closed:
            self.connect()
        if self.conn is None or self.conn.closed:
            raise Exception(
                "Falha ao estabelecer conexão com o banco de dados.")

    def insert_face(self, username, face_encoding):
        self.ensure_connection()
        print(f"Inserindo face para o usuário: {
              username}")  # Verificação de entrada
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
             INSERT INTO faces (username, face_encoding)
             VALUES (%s, %s)
             RETURNING id;
             """,
                (username, face_encoding)
            )
            self.conn.commit()
            print("Face inserida com sucesso.")  # Verificação de sucesso
            return cur.fetchone()[0]
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Erro ao salvar no banco de dados: {e}")  # Exibe o erro
            raise Exception(f"Erro ao salvar no banco de dados: {e}")

    def get_face(self, id):
        """Obtém uma face pelo ID."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM faces WHERE id = %s",
                (id,)
            )
            return cur.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Erro ao buscar face no banco de dados: {e}")

    def update_face(self, id, username, face_encoding):
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                UPDATE faces
                SET username = %s, face_encoding = %s
                WHERE id = %s;
                """,
                (username, face_encoding, id)
            )
            self.conn.commit()
            return cur.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Erro ao atualizar face no banco de dados: {e}")

    def delete_face(self, id):
        """Exclui uma face pelo ID."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                "DELETE FROM faces WHERE id = %s",
                (id,)
            )
            self.conn.commit()
            return cur.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Erro ao excluir face no banco de dados: {e}")

    def get_all_faces(self):
        """Obtém todas as faces cadastradas."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM faces")
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(
                f"Erro ao buscar todas as faces no banco de dados: {e}")

    def get_face_by_username(self, username):
        """Obtém uma face pelo nome de usuário."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM faces WHERE username = %s",
                (username,)
            )
            return cur.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Erro ao buscar face pelo nome de usuário: {e}")
