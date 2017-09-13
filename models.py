import peewee as pw

db = pw.Proxy()


def connect_to_db(database, **kwars):
    sqlitedb = pw.SqliteDatabase(database, **kwars)
    db.initialize(sqlitedb)


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

