import inspect
import sys
import peewee as pw

db = pw.Proxy()


def connect_to_db(database, **kwars):
    sqlitedb = pw.SqliteDatabase(database, **kwars)
    db.initialize(sqlitedb)
    initialize_tables()

def close_connection():
    db.close()


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

    
class Authors(BaseModel):
    id = pw.PrimaryKeyField()
    name = pw.TextField()


class Paper_authors(BaseModel):
    id = pw.PrimaryKeyField()
    paper_id = pw.ForeignKeyField(Papers)
    author_id = pw.ForeignKeyField(Authors) 

class Citations(BaseModel):
    id = pw.PrimaryKeyField()
    source_paper = pw.ForeignKeyField(Papers, related_name='sorce')
    cited_paper = pw.ForeignKeyField(Papers, related_name='cited')

# table for papers without reference content
class Papers_NR(BaseModel):
    id = pw.PrimaryKeyField()
    pdf_name = pw.TextField()
    paper_text = pw.TextField()

# tables for papers without reference content and without stopwords
class Papers_NR_NSW(BaseModel):
    id = pw.PrimaryKeyField()
    pdf_name = pw.TextField()
    paper_text = pw.TextField()

# tables for papers without reference content and without stopwords
# and with a stemming process applied
class Papers_NR_NSW_STE(BaseModel):
    id = pw.PrimaryKeyField()
    pdf_name = pw.TextField()
    paper_text = pw.TextField()
    
DATABASE_FILENAME = "../data/database.sqlite"
if __name__ == '__main__':
    connect_to_db(DATABASE_FILENAME)

