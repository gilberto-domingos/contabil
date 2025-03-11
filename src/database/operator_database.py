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

    def insert_operator(self, cod_operator, cnpj_operator, name_operator):
        """Insere uma nova operadora no banco de dados."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO operadoras (cod_operator, cnpj_operator, name_operator)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (cod_operator, cnpj_operator, name_operator)
            )
            self.conn.commit()
            return cur.fetchone()[0]
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Erro ao salvar no banco de dados: {e}")

    def get_operator(self, operator_id):
        """Obtém uma operadora pelo ID."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM operadoras WHERE id = %s",
                (operator_id,)
            )
            return cur.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Erro ao buscar operadora no banco de dados: {e}")

    def update_operator(self, operator_id, cod_operator, cnpj_operator, name_operator):
        """Atualiza os dados de uma operadora."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                UPDATE operadoras
                SET cod_operator = %s, cnpj_operator = %s, name_operator = %s
                WHERE id = %s;
                """,
                (cod_operator, cnpj_operator, name_operator, operator_id)
            )
            self.conn.commit()
            return cur.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(
                f"Erro ao atualizar operadora no banco de dados: {e}")

    def delete_operator(self, operator_id):
        """Exclui uma operadora pelo ID."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                "DELETE FROM operadoras WHERE id = %s",
                (operator_id,)
            )
            self.conn.commit()
            return cur.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(
                f"Erro ao excluir operadora no banco de dados: {e}")

    def get_all_operators(self):
        """Obtém todas as operadoras do banco de dados."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM operadoras")
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(
                f"Erro ao buscar todas as operadoras no banco de dados: {e}")

    def get_operator_by_cod(self, cod_operator):
        """Obtém uma operadora pelo código."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM operadoras WHERE cod_operator = %s",
                (cod_operator,)
            )
            return cur.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Erro ao buscar operadora pelo código: {e}")

    def get_operator_by_name(self, name_operator):
        """Obtém operadoras pelo nome (parcial)."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM operadoras WHERE name_operator ILIKE %s",
                (f"%{name_operator}%",)
            )
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Erro ao buscar operadoras pelo nome: {e}")
