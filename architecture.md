                           +-------------------------------+
                           |     🚀 FastAPI Entry Point     |
                           |-------------------------------|
                           | /query (POST)                 |
                           | Handles text/voice queries    |
                           +---------------+---------------+
                                           |
                                           v
                    +----------------------+----------------------+
                    |         🧠 Intent Classifier (ML Model)      |
                    |---------------------------------------------|
                    | Classifies query into:                      |
                    | - document_query                           |
                    | - appointment_query                        |
                    +--------+------------------+----------------+
                             |                  |
                document_query|                  |appointment_query
                             v                  v
         +--------------------+        +-----------------------------+
         |   📄 Document Agent |        |  📅 Appointment Agent        |
         |--------------------|        |-----------------------------|
         | - Embed Query      |        | - Parse Appointment Intent  |
         | - Search Vector DB |        | - Check Availability        |
         | - Retrieve Chunks  |        | - Book Appointment          |
         | - Prompt GPT-4     |        | - Summarize/Confirm         |
         +--------+-----------+        +--------------+--------------+
                  |                                 |
         +--------v-----------+           +---------v------------+
         | 🧠 GPT-4 via OpenAI |           |   GPT-4 via OpenAI    |
         |--------------------|           |-----------------------|
         | - Final Response   |           | - Natural Language    |
         | - Markdown format  |           | - Confirmation Output |
         +--------+-----------+           +-----------+-----------+
                  |                                   |
                  +-------------+---------------------+
                                |
                      +---------v----------+
                      | Return JSON Response|
                      | { type, content }   |
                      +---------------------+
