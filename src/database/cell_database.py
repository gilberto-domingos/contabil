import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Estabelece conexão com o banco de dados se não estiver conectado."""
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
        """Garante que a conexão está ativa, tentando reconectar se necessário."""
        if self.conn is None or self.conn.closed:
            self.connect()
        if self.conn is None or self.conn.closed:
            raise Exception(
                "Falha ao estabelecer conexão com o banco de dados.")

    def insert_cell(self, cod_cell, name_cell, email_cell):
        """Insere uma nova célula no banco de dados."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO cells (cod_cell, name_cell, email_cell)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (cod_cell, name_cell, email_cell)
            )
            self.conn.commit()
            return cur.fetchone()[0]
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Erro ao salvar no banco de dados: {e}")

    def get_cell(self, cell_id):
        """Obtém uma célula pelo ID."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM cells WHERE id = %s",
                (cell_id,)
            )
            return cur.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Erro ao buscar célula no banco de dados: {e}")

    def update_cell(self, cell_id, cod_cell, name_cell, email_cell):
        """Atualiza os dados de uma célula."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                UPDATE cells
                SET cod_cell = %s, name_cell = %s, email_cell = %s
                WHERE id = %s;
                """,
                (cod_cell, name_cell, email_cell, cell_id)
            )
            self.conn.commit()
            return cur.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(
                f"Erro ao atualizar célula no banco de dados: {e}")

    def delete_cell(self, cell_id):
        """Exclui uma célula pelo ID."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                "DELETE FROM cells WHERE id = %s",
                (cell_id,)
            )
            self.conn.commit()
            return cur.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Erro ao excluir célula no banco de dados: {e}")

    def get_all_cells(self):
        """Obtém todas as células do banco de dados."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM cells")
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(
                f"Erro ao buscar todas as células no banco de dados: {e}")

    def get_cell_by_cod(self, cod_cell):
        """Obtém uma célula pelo código."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM cells WHERE cod_cell = %s",
                (cod_cell,)
            )
            return cur.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Erro ao buscar célula pelo código: {e}")

    def get_cell_by_name(self, name_cell):
        """Obtém células pelo nome (parcial)."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM cells WHERE name_cell ILIKE %s",
                (f"%{name_cell}%",)
            )
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Erro ao buscar células pelo nome: {e}")
