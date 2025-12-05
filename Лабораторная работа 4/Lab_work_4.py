from sqlalchemy import create_engine, select, ForeignKey, Integer
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from Create_tables import Base, Products
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as UUIDType


class RestockList(Base):
    __tablename__ = "restock_list"
    product_id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    order_quantity: Mapped[int] = mapped_column(Integer, nullable=False)


class DataBaseManager:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    def analysis_stock_residue(self, class_table):
        RestockList.__table__.create(self.engine, checkfirst=True)
        with self.session_scope() as session:
            statement = select(class_table).where(class_table.current_stock <= class_table.min_stock)
            results = session.scalars(statement).all()
            for product in results:
                order_quantity = product.min_stock * 2 - product.current_stock
                new_order = RestockList(
                    product_id=product.id,
                    order_quantity=order_quantity
                )
                session.add(new_order)

    def drop_table(self, class_table):
        class_table.__table__.drop(self.engine, checkfirst=True)

if __name__ == "__main__":
    db_manager = DataBaseManager("sqlite:///company_data.db")
    db_manager.drop_table(RestockList)
    db_manager.analysis_stock_residue(Products)