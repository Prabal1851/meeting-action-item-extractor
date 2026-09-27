import streamlit as st
from datetime import date
from extractor import extract_action_items
from logic.validators import flag_issues, dedupe_action_items

st.set_page_config(page_title="Meeting Action Item Extractor", layout="wide")
st.title("Meeting Action Item Extractor")

uploaded_file = st.file_uploader("Upload a transcript (.txt)", type=["txt"])
meeting_date = st.date_input("Meeting date", value=date.today())

if uploaded_file is not None:
    transcript = uploaded_file.read().decode("utf-8")

    with st.expander("View raw transcript"):
        st.text(transcript)

    if st.button("Extract action items"):
        with st.spinner("Extracting..."):
            try:
                result = extract_action_items(transcript, str(meeting_date))
                result = dedupe_action_items(result)
                issues = flag_issues(result)

                st.success(f"Found {len(result.action_items)} action item(s)")

                rows = [item.model_dump() for item in result.action_items]
                st.dataframe(rows, use_container_width=True)

                if issues:
                    st.warning("Review flags:")
                    for issue in issues:
                        st.write(f"- {issue}")

            except ValueError as e:
                st.error(str(e))
                