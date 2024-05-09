from sqlmodel import Session, select
from src.api.common.dependency_container import DependencyContainer

class SQL_Utils():
    
    def __init__(self) -> None:
        DC = DependencyContainer()
        DC.initialize()
        self.DC = DC
    
    def sql_session(self):
        return Session(self.DC._database_engine)

    def select_table(self,type_class):
        with self.sql_session() as session:
            statement = select(type_class)
            results = session.exec(statement)
            return results.all()
                
    def insert_data(self, data):
        with self.sql_session() as session:
            session.add(data)
            session.commit()
            
    def insert_by_session(self, data, session):
        session.add(data)
        session.commit()