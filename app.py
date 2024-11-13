# app.py
import streamlit as st
import model  # Importing our backend functions from model.py

# Streamlit UI Components
st.title("Local Academic Research Paper Assistant")
st.sidebar.header("Configure Your Search")

# Text input for research topic
topic = st.text_input("Enter Research Topic", "machine learning and healthcare")

# Slider to select number of research papers to fetch
max_papers = st.sidebar.slider("Select Number of Papers to Fetch", 1, 10, 5)

# Fetch and display papers
if st.button("Fetch Papers"):
    st.write(f"Fetching {max_papers} papers on the topic: **{topic}**")
    papers = model.fetch_papers(topic, max_results=max_papers)

    if papers:
        for idx, paper in enumerate(papers):
            st.subheader(f"Paper {idx + 1}: {paper['title']}")
            st.write(f"**Authors**: {', '.join(paper['authors'])}")
            st.write(f"**Published**: {paper['published']}")
            st.write(f"**Summary**: {paper['summary'][:500]}...")  # Display part of the summary
            with st.expander("View Full Summary"):
                full_summary = model.summarize_paper(paper["summary"])
                st.write(full_summary)

        # Interactive Q&A for the first paper
        if len(papers) > 0:
            st.write("\n## Ask Questions about the First Paper")
            user_question = st.text_area("Enter your question (related to the first paper summary)")
            if st.button("Get Answer"):
                if user_question:
                    result = model.answer_question_with_span(user_question, papers[0]["summary"])
                    st.write("**Answer**:", result["answer"])
                    st.write("**Exact Part of the Paper**:", result["exact_part"])
                else:
                    st.warning("Please enter a question.")

        # Extract key information from multiple papers
        st.write("\n## Extract Key Information from All Papers")
        if st.button("Extract Key Information"):
            key_info = model.extract_key_information(papers)
            if key_info:
                st.write("### Contributions:")
                for contribution in key_info["contributions"]:
                    st.write("- ", contribution)

                st.write("\n### Methodologies:")
                for methodology in key_info["methodologies"]:
                    st.write("- ", methodology)

                st.write("\n### Conclusions:")
                for conclusion in key_info["conclusions"]:
                    st.write("- ", conclusion)

