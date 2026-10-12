def promptMaker(question,chunks):
    context_blocks = "\n\n".join(
    f"[Page {item['page_number']}]\n {item['text']}" 
    for item in chunks)

    final_prompt = f"""Answer the user's question using only the information explicitly supported by the provided context.

Rules:

Do not use your general knowledge to answer the question.

If the context does not contain enough information to answer the question, clearly state that the answer cannot be determined from the provided document.

Do not provide additional explanations, facts, or assumptions that are not supported by the context.

Cite the page number for each answer when available.

If the context is irrelevant to the question, say so direct 
Context:
    {context_blocks}
    \nQuestion: {question}
    \nInstructions:
    Explain the concept clearly using the provided context.
    Mention the relevant page numbers when useful.
    If the context doesn't contain enough information, say so."""

    return final_prompt

# context = [
#   {
#     "id": "cf595861-0bf7-4713-a080-832ed43723f6",
#     "page_number": 96,
#     "text": "The downside of a normalized representation is that every time you want to display arecord containing an ID, you have to do an additional lookup to resolve the ID intosomething human-readable. In a relational data model, this is done using a join. Forexample:",
#     "distance": 0.31882739067077637
#   },
#   {
#     "id": "76820bf8-b4dc-42d5-8aba-fb0e7fc8f0f9",
#     "page_number": 97,
#     "text": "Document databases can store both normalized and denormalized data, but theyare often associated with denormalization—partly because the JSON data modelmakes it easy to store additional denormalized fields, and partly because the weaksupport for joins in many document databases makes normalization inconvenient.Some document databases don’t support joins at all, so you have to perform them inapplication code—that is, you first fetch a document containing an ID, then performa second query to resolve that ID into another document. In MongoDB, it is alsopossible to perform a join using the $lookup operator in an aggregation pipeline:",
#     "distance": 0.3332979083061218
#   },
#   {
#     "id": "75e5ed2a-335b-4765-acb2-b5a9c7957ffa",
#     "page_number": 98,
#     "text": "As a general principle, normalized data is usually faster to write (since there is onlyone copy) but slower to query (since it requires joins); denormalized data is usuallyfaster to read (fewer joins) but more expensive to write (more copies to update, moredisk space used). You might find it helpful to view denormalization as a form ofderived data (see “Systems of Record and Derived Data” on page 10), since you needto set up a process for updating the redundant copies of the data.",
#     "distance": 0.2991355300980124
#   },
#   {
#     "id": "ef00bd0a-ba36-45a3-96b6-a4259081710f",
#     "page_number": 98,
#     "text": "Normalization tends to be better for OLTP systems, where both reads and updatesneed to be fast; analytical systems often fare better with denormalized data, since theyperform updates in bulk and the performance of read-only queries is the dominantconcern. In systems of small to moderate scale, a normalized data model is often bestbecause you don’t have to worry about keeping multiple copies of the data consistentwith one another, and the cost of performing joins is acceptable. However, in verylarge-scale systems, the cost of joins can become problematic.",
#     "distance": 0.30038169921582014
#   },
#   {
#     "id": "f5cd2e9f-7a2d-4dd3-a6c6-ecc2e1299299",
#     "page_number": 634,
#     "text": "comparison to transaction processing, 5data normalization, 74data warehousing (see data warehousing)predictive (see predictive analytics)",
#     "distance": 0.3214377164840698
#   }
# ]
# print(promptMaker("what is normalizaton?",chunks=context))





# Context:

# [Page 96]
# The downside of a normalized representation...

# [Page 97]
# Document databases can store both normalized and denormalized data...

# [Page 98]
# As a general principle, normalized data is usually faster to write...

# [Page 98]
# Normalization tends to be better for OLTP systems...

# Question:
# What is normalization?

# Instructions:
# Explain the concept clearly using the provided context.
# Mention the relevant page numbers when useful.
# If the context doesn't contain enough information, say so.