"""
WiSe 15, WebIR, Project-1, Becet, Simmet
Database Module
"""

from init_logging import init_logging
import logging
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table

if __name__ == "__main__":
    init_logging()
logger = logging.getLogger(__name__)

Base = declarative_base()

author_entry_association_table = Table("author_entry", Base.metadata,
                                       Column("entry_id", Integer, ForeignKey("entries.id")),
                                       Column("author_id", Integer, ForeignKey("people.id")))

editor_entry_association_table = Table("editor_entry", Base.metadata,
                                       Column("entry_id", Integer, ForeignKey("entries.id")),
                                       Column("editor_id", Integer, ForeignKey("people.id")))


class Publisher(Base):
    """
    Base class to map publishers
    """
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(100))

    def __repr__(self):
        return self.name


class Type(Base):
    """
    Base class to map publication types
    """
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50))

    def __repr__(self):
        return self.name


class Journal(Base):
    """
    Base class to map journals
    """
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(100))

    def __repr__(self):
        return self.name


class Person(Base):
    """
    Base class to map authors
    """
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    asis_name = Column(String(100))

    def __repr__(self):
        return """Person(
            first_name='{}',
            last_name='{}',
            asis_name='{}'""".format(
            self.first_name,
            self.last_name,
            self.asis_name
        )


class Entry(Base):
    """
    Base class to map .bib entries
    """
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    entry_type_id = Column(Integer, ForeignKey("types.id"))
    entry_type = relationship("Type", back_populates="entries")
    entry_id = Column(String(50))
    authors = relationship("Person", secondary=author_entry_association_table)
    title = Column(String(200))
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    publisher = relationship("Publisher", back_populates="entries")
    editors = relationship("Person", secondary=editor_entry_association_table)
    year = Column(Integer)
    journal = Column(String(100))
    isbn = Column(String(50))
    volume = Column(String(50))
    doi = Column(String(100))
    link = Column(String(200))
    note = Column(String(200))

    def __repr__(self):
        return """Entry(
            type='{}',
            id='{}',
            authors='{}'
            title='{}',
            publisher='{}',
            editor='{}',
            year='{}',
            journal='{}',
            isbn='{}',
            volume ='{}',
            doi ='{}',
            link ='{}',
            note ='{}')""".format(
            self.entry_type,
            self.entry_id,
            self.authors,
            self.title,
            self.publisher,
            self.editor,
            self.year,
            self.journal,
            self.isbn,
            self.volume,
            self.doi,
            self.link,
            self.note
        )


class BibDB:
    """
    MySQL Database wrapper class - (Use constructor parameters to initialize it according to your database settings)
    """
    Engine = None
    Session = None

    def __init__(self,
                 db_user_name="root",
                 db_password="WebIR2015",
                 db_address="localhost",
                 db_name="bib_db",
                 verbose=False):

        self.Engine = sqlalchemy.create_engine("mysql+pymysql://{}:{}@{}/{}".format(
            db_user_name,
            db_password,
            db_address,
            db_name
        ),
            echo=verbose)
        self.Session = sessionmaker(bind=self.Engine)

    def create_tables(self):
        """
        Create non-existent tables from the orm mappings
        """
        if self.Engine is not None:
            Base.metadata.create_all(self.Engine)
        else:
            logger.error("Engine is NOT initialized!")

    def fill_entries(self, bib_list):
        """
        Fill the database with parsed .bib entries
        """
        if self.Engine is not None:
            try:
                items = []
                for ent in bib_list:
                    new_entry = Entry(
                        entry_type=ent.get("ENTRYTYPE", "").encode("utf-8"),
                        entry_id=ent.get("ID", "").encode("utf-8"),
                        title=ent.get("title", "").encode("utf-8"),
                        publisher=ent.get("publisher", "").encode("utf-8"),
                        editor=ent.get("editor", "").encode("utf-8"),
                        year=int(ent.get("year", "").encode("utf-8")),
                        journal=ent.get("journal", "").encode("utf-8"),
                        isbn=ent.get("isbn", "").encode("utf-8"),
                        volume=ent.get("volume", "").encode("utf-8"),
                        doi=ent.get("doi", "").encode("utf-8"),
                        link=ent.get("link", "").encode("utf-8"),
                        note=ent.get("note", "").encode("utf-8")
                    )
                    items.append(new_entry)
                session = self.Session()
                session.add_all(items)
                session.commit()
            except:
                logger.error("Error at writing to database!")
        else:
            logger.error("Engine is NOT initialized!")


def main():
    """
    This is a main procedure only for testing! It shouldn't normally run!
    """
    logger.warning("This is a main procedure only for testing this module! It shouldn't normally run!")
    my_db = BibDB()
    my_db.create_tables()


if __name__ == "__main__":
    main()
