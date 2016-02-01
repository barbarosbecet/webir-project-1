"""
WiSe 15, WebIR, Project-2, Becet, Simmet
Database Module
"""

from init_logging import init_logging
import logging
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table

logger = logging.getLogger(__name__)

Base = declarative_base()

author_entry_association_table = Table("author_entry", Base.metadata,
                                       Column("entry_id", Integer, ForeignKey("entries.id")),
                                       Column("author_id", Integer, ForeignKey("people.id")))

editor_entry_association_table = Table("editor_entry", Base.metadata,
                                       Column("entry_id", Integer, ForeignKey("entries.id")),
                                       Column("editor_id", Integer, ForeignKey("people.id")))


class Type(Base):
    """
    Base class to map publication types
    """
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50))
    entries = relationship("Entry", back_populates="entry_type")

    def __repr__(self):
        return self.name


class Publisher(Base):
    """
    Base class to map publishers
    """
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(200))
    entries = relationship("Entry", back_populates="publisher")

    def __repr__(self):
        return self.name


class Journal(Base):
    """
    Base class to map journals
    """
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(200))
    entries = relationship("Entry", back_populates="journal")

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
    entries_authored = relationship("Entry", secondary=author_entry_association_table, back_populates="authors")
    entries_editored = relationship("Entry", secondary=editor_entry_association_table, back_populates="editors")

    def __repr__(self):
        return """Person(
            first_name='{}',
            last_name='{}',
            asis_name='{}')""".format(
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
    authors = relationship("Person", secondary=author_entry_association_table, back_populates="entries_authored")
    title = Column(String(300))
    booktitle = Column(String(300))
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    publisher = relationship("Publisher", back_populates="entries")
    editors = relationship("Person", secondary=editor_entry_association_table, back_populates="entries_editored")
    year = Column(Integer)
    journal_id = Column(Integer, ForeignKey("journals.id"))
    journal = relationship("Journal", back_populates="entries")
    isbn = Column(String(50))
    volume = Column(String(50))
    doi = Column(String(100))
    link = Column(String(300))
    note = Column(String(300))
    abstract = Column(String(500))

    def __repr__(self):
        return """Entry(
            type='{}',
            id='{}',
            authors='{}'
            title='{}',
            booktitle='{}',
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
            self.booktitle,
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
    (Use constructor parameters to initialize it according to your database settings)
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
            db_name),
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
            session = self.Session()
            for ent in bib_list:
                new_entry = Entry()
                if "ID" in ent:
                    new_entry.entry_id = ent.get("ID").encode("utf-8")
                if "title" in ent:
                    new_entry.title = ent.get("title").encode("utf-8")
                    entry_match = session.query(Entry).filter(Entry.title == new_entry.title).first()
                    if entry_match is not None:
                        continue
                if "year" in ent:
                    try:
                        new_entry.year = int(ent.get("year"))
                    except ValueError:
                        new_entry.year = None
                if "isbn" in ent:
                    new_entry.isbn = ent.get("isbn").encode("utf-8")
                if "volume" in ent:
                    new_entry.volume = ent.get("volume").encode("utf-8")
                if "doi" in ent:
                    new_entry.doi = ent.get("doi").encode("utf-8")
                if "link" in ent:
                    new_entry.link = ent.get("link").encode("utf-8")
                if "note" in ent:
                    new_entry.note = ent.get("note").encode("utf-8")
                if "abstract" in ent:
                    new_entry.abstract = ent.get("abstract").encode("utf-8")
                if "ENTRYTYPE" in ent:
                    match = session.query(Type).filter(Type.name == ent.get("ENTRYTYPE")).first()
                    if match is None:
                        new_entry.entry_type = Type(name=ent.get("ENTRYTYPE").encode("utf-8"))
                    else:
                        new_entry.entry_type = match
                if "publisher" in ent:
                    match = session.query(Publisher).filter(Publisher.name == ent.get("publisher").encode("utf-8")).first()
                    if match is None:
                        new_entry.publisher = Publisher(name=ent.get("publisher").encode("utf-8"))
                    else:
                        new_entry.publisher = match
                if "journal" in ent:
                    match = session.query(Journal).filter(Journal.name == ent.get("journal").encode("utf-8")).first()
                    if match is None:
                        new_entry.journal = Journal(name=ent.get("journal").encode("utf-8"))
                    else:
                        new_entry.journal = match
                if "author" in ent:
                    for name_str in ent["author"]:
                        if "," in name_str:
                            ln, _, fn = name_str.partition(",")
                        else:
                            fn, _, ln = name_str.rpartition(" ")
                        fn = fn.strip().encode("utf-8")
                        ln = ln.strip().encode("utf-8")
                        name_str = name_str.encode("utf-8")

                        if len(fn) > 1 and len(ln) > 1:
                            match_1 = session.query(Person).filter(Person.asis_name == name_str).first()
                            if match_1 is not None:
                                new_author = match_1
                                new_entry.authors.append(new_author)
                                continue
                            match_2 = session.query(Person).filter(Person.first_name == fn)\
                                .filter(Person.last_name == ln).first()
                            if match_2 is not None:
                                new_author = match_2
                                new_entry.authors.append(new_author)
                                continue
                            match_3 = session.query(Person).filter(Person.last_name == ln)
                            if match_3.count() > 0:
                                if "." in str(fn):
                                    match_3_1 = match_3.filter(Person.first_name.like(str(fn[0])+"%")).first()
                                    if match_3_1 is not None:
                                        new_author = match_3_1
                                        new_entry.authors.append(new_author)
                                        continue
                                else:
                                    match_3_2 = match_3.filter(Person.first_name.like("_.%"))
                                    if match_3_2.count() > 0:
                                        match_3_2_1 = match_3_2.filter(Person.first_name == str(fn[0])+".").first()
                                        if match_3_2_1 is not None:
                                            new_author = match_3_2_1
                                            new_entry.authors.append(new_author)
                                            continue
                        new_author = Person(first_name=fn.strip(),
                                            last_name=ln.strip(),
                                            asis_name=name_str)
                        new_entry.authors.append(new_author)
                if "editor" in ent:
                    for name_str in ent["editor"]:
                        if "," in name_str:
                            ln, _, fn = name_str.partition(",")
                        else:
                            fn, _, ln = name_str.rpartition(" ")
                        fn = fn.strip().encode("utf-8")
                        ln = ln.strip().encode("utf-8")
                        name_str = name_str.encode("utf-8")
                        if len(fn) > 1 and len(ln) > 1:
                            match_1 = session.query(Person).filter(Person.asis_name == name_str).first()
                            if match_1 is not None:
                                new_editor = match_1
                                new_entry.editors.append(new_editor)
                                continue
                            match_2 = session.query(Person).filter(Person.first_name == fn)\
                                .filter(Person.last_name == ln).first()
                            if match_2 is not None:
                                new_editor = match_2
                                new_entry.editors.append(new_editor)
                                continue
                            match_3 = session.query(Person).filter(Person.last_name == ln)
                            if match_3.count() > 0:
                                if "." in str(fn):
                                    match_3_1 = match_3.filter(Person.first_name.like(str(fn[0])+"%")).first()
                                    if match_3_1 is not None:
                                        new_editor = match_3_1
                                        new_entry.editors.append(new_editor)
                                        continue
                                else:
                                    match_3_2 = match_3.filter(Person.first_name.like("_.%"))
                                    if match_3_2.count() > 0:
                                        match_3_2_1 = match_3_2.filter(Person.first_name == str(fn[0])+".").first()
                                        if match_3_2_1 is not None:
                                            match_3_2_1.first_name = fn
                                            new_editor = match_3_2_1
                                            new_entry.editors.append(new_editor)
                                            continue
                        new_editor = Person(first_name=fn.strip(),
                                            last_name=ln.strip(),
                                            asis_name=name_str)
                        new_entry.editors.append(new_editor)
                session.add(new_entry)
            session.commit()
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
    init_logging()
    main()
