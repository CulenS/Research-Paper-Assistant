# Research-Paper-Assistant

The Local Academic Research Paper Assistant is an interactive tool that helps researchers access, summarize, and analyze academic papers from arXiv. Built with Streamlit, it uses NLP models like BERT and BART for summarization and question-answering, making literature review easier and faster.

### Key Features

- **Paper Retrieval**: Fetches relevant research papers from arXiv based on a user-defined topic.
- **Summarization**: Generates concise summaries of papers for quick understanding.
- **Question-Answering (Q&A)**: Users can ask questions about the first paper to get direct answers with highlighted text spans.
- **Key Information Extraction**: Extracts core contributions, methodologies, and conclusions across papers.

### Usage Instructions

1. **Enter Research Topic**: Define a topic to search for relevant academic papers.
2. **Configure Settings**: Choose the number of papers to retrieve (1-10).
3. **Fetch and View Papers**: Click "Fetch Papers" to get titles, authors, publication dates, and summaries.
4. **Ask Questions**: Enter a question related to the first paper’s summary to get an answer and highlighted text.
5. **Extract Key Information**: View summarized contributions, methodologies, and conclusions from multiple papers.

### Requirements

- Python 3.7+
- Libraries: `Streamlit`, `Transformers`, `Requests`, `BeautifulSoup`

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Research-Paper-Assistant.git
