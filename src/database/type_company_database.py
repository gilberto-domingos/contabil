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

    def get_all_type_companies(self):
        """Obtém todos os tipos de empresas."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM type_companies")
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(
                f"Erro ao buscar tipos de empresa no banco de dados: {e}")

    def get_type_company_by_cod(self, cod_company):
        """Obtém um tipo de empresa pelo código."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM type_companies WHERE cod_company = %s",
                (cod_company,)
            )
            return cur.fetchone()
        except psycopg2.Error as e:
            raise Exception(
                f"Erro ao buscar tipo de empresa pelo código: {e}")

    def get_type_company_by_descr(self, descr_company):
        """Obtém tipos de empresa pela descrição (parcial)."""
        self.ensure_connection()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM type_companies WHERE descr_company ILIKE %s",
                (f"%{descr_company}%",)
            )
            return cur.fetchall()
        except psycopg2.Error as e:
            raise Exception(
                f"Erro ao buscar tipos de empresa pela descrição: {e}")

    def update_type_company(self, id, new_cod, new_descr):
        """Atualiza um tipo de empresa no banco de dados."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                UPDATE type_companies
                SET cod_company = %s, descr_company = %s
                WHERE id = %s
                """,
                (new_cod, new_descr, id)
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(
                f"Erro ao atualizar tipo de empresa no banco de dados: {e}")
        finally:
            cur.close()

    def insert_type_company(self, cod_company, descr_company):
        """Insere um novo tipo de empresa no banco de dados."""
        self.ensure_connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO type_companies (cod_company, descr_company)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (cod_company, descr_company)
            )
            self.conn.commit()
            return cur.fetchone()[0]
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Erro ao salvar no banco de dados: {e}")
        finally:
            cur.close()
