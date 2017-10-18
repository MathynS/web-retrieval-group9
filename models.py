import inspect
import sys
import peewee as pw

db = pw.Proxy()


def connect_to_db(database, **kwars):
    sqlitedb = pw.SqliteDatabase(database, **kwars)
    db.initialize(sqlitedb)
    initialize_tables()


def initialize_tables():
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    clsmembers = [c for c in clsmembers if c[0] != 'BaseModel' and not c[1].table_exists()]
    for clsmember in clsmembers:
        clsmember[1].create_table(True)
        print("Created table: {table_name}".format(table_name=clsmember[0].lower()))


class BaseModel(pw.Model):
    class Meta:
        database = db


class Papers(BaseModel):
    id = pw.PrimaryKeyField()
    year = pw.IntegerField()
    title = pw.TextField()
    event_type = pw.TextField()
    pdf_name = pw.TextField()
    abstract = pw.TextField()
    paper_text = pw.TextField()
    citations = pw.IntegerField()

    
class Authors(BaseModel):
    id = pw.PrimaryKeyField()
    name = pw.TextField()
    pagerank = pw.FloatField()


class Paper_authors(BaseModel):
    id = pw.PrimaryKeyField()
    paper = pw.ForeignKeyField(Papers)
    author = pw.ForeignKeyField(Authors) 


class Citations(BaseModel):
    id = pw.PrimaryKeyField()
    source_paper = pw.ForeignKeyField(Papers, related_name='source')
    cited_paper = pw.ForeignKeyField(Papers, related_name='cited')


class Labels(BaseModel):
    id = pw.PrimaryKeyField()
    name = pw.TextField()


class Papers_labels(BaseModel):
    id = pw.PrimaryKeyField()
    paper = pw.ForeignKeyField(Papers)
    label = pw.ForeignKeyField(Labels)


if __name__ == '__main__':
    connect_to_db('nips-papers.db')
