"""
WiSe 15, WebIR, Project-1, Becet, Simmet
Database Module
"""

from init_logging import init_logging
import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    init_logging()
logger = logging.getLogger(__name__)

Base = declarative_base()


class Entry(Base):
    """
    Base class to map .bib "entries"
    """
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    entry_type = Column(String(50))
    entry_id = Column(String(50))
    title = Column(String(200))
    publisher = Column(String(100))
    editor = Column(String(100))
    year = Column(Integer)
    journal = Column(String(100))
    isbn = Column(String(50))
    volume = Column(String(50))
    doi = Column(String(100))
    link = Column(String(200))
    note = Column(String(200))

    def __repr__(self):
        return """Entry(
            entry_type='{}',
            entry_id='{}',
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
    Database wrapper class
    ASSIGN DATABASE SETTINGS BELOW ACCORDING TO YOUR OWN CONFIGURATION!
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
            except Exception as e:
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

