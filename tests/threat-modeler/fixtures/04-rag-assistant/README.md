# HR policy assistant (SYNTHETIC TEST SYSTEM)

Employees ask questions about HR policies in a chat widget on the intranet. The assistant retrieves passages from the policy corpus (vector store) and answers with an LLM. It can also call one tool, `create_hr_ticket`, which opens a ticket in the HR system on the employee's behalf.

Any employee can upload documents to the corpus through the "Suggest a policy update" form; uploads are indexed automatically every hour.
