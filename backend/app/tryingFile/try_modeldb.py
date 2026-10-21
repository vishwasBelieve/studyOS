# from sentence_transformers import SentenceTransformer
# from app.models.document_text import DocumentText
# from sqlalchemy import select
# from app.db.database import SessionLocal
# import asyncio
# model = SentenceTransformer("BAAI/bge-small-en-v1.5",local_files_only=True)


# sentences = ["""Distributed transactions, especially those implemented with two-phase commit, have
# a mixed reputation. On the one hand, they are seen as providing an important safety
# guarantee that would be hard to achieve otherwise; on the other hand, they are criti‐
# cized  for  causing  operational  problems,  killing  performance,  and  promising  more
# than  they  can  deliver  [81,  82,  83,  84].  Many  cloud  services  choose  not  to  implement
# distributed transactions due to the operational problems they engender [85, 86]."""
# ,"""Synchronous versus asynchronous conflict detection
# In  a  single-leader  database,  the  second  writer  will  either  block  and  wait  for  the  first
# write to complete, or abort the second write transaction, forcing the user to retry the
# write. On the other hand, in a multi-leader setup, both writes are successful, and the
# conflict  is  only  detected  asynchronously  at  some  later  point  in  time.  At  that  time,  it
# may be too late to ask the user to resolve the conflict.""",
# """Derived  views  allow  gradual  evolution.  If  you  want  to  restructure  a  dataset,  you  do
# not need to perform the migration as a sudden switch. Instead, you can maintain the
# old schema and the new schema side by side as two independently derived views onto
# the same underlying data. You can then start shifting a small number of users to the
# new  view  in  order  to  test  its  performance  and  find  any  bugs,  while  most  users  con‐
# tinue  to  be  routed  to  the  old  view.  Gradually,  you  can  increase  the  proportion  of
# users accessing the new view, and eventually you can drop the old view [10].""",
# """MPP databases are monolithic, tightly integrated pieces of software that take care of
# storage  layout  on  disk,  query  planning,  scheduling,  and  execution.  Since  these  com‐
# ponents can all be tuned and optimized for the specific needs of the database, the sys‐
# tem as a whole can achieve very good performance on the types of queries for which
# it  is  designed.  Moreover,  the  SQL  query  language  allows  expressive  queries  and  ele‐
# gant semantics without the need to write code, making it accessible to graphical tools
# used by business analysts (such as Tableau).""",
# """There is a gradient between fully automatic rebalancing (the system decides automat‐
# ically when to move partitions from one node to another, without any administrator
# interaction) and fully manual (the assignment of partitions to nodes is explicitly con‐
# figured  by  an  administrator,  and  only  changes  when  the  administrator  explicitly
# reconfigures it). For example, Couchbase, Riak, and Voldemort generate a suggested
# partition assignment automatically, but require an administrator to commit it before
# it takes effect""",
# "what is gradual evalution in derived views?"
# ]

# db = SessionLocal()

# def someFunction():

#     document_id = '97d04c49-c4ec-4dd5-bbd3-61e78a153775'
#     stmt = select(DocumentText).where(DocumentText.document_id == document_id,DocumentText.embedding.is_(None))
#     result = db.execute(stmt)
#     rows = result.scalars().all()

#     texts = [row.text for row in rows]

#     embeddings = model.encode(texts)

#     for row,embedding in zip(rows,embeddings):
#         row.embedding = embedding.tolist()

#     db.commit()
