from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.util import has_identity

engine = create_engine('sqlite:///atividade.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Arquivos(Base):
    __tablename__='arquivos'
    nome = Column(String(40), primary_key=True)
    img_origem = Column(BLOB)
    img_limpa = Column(BLOB)
    caminho = Column(String(60))

    def __repr__(self):
        return '<Imagem {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()

