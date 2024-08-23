import os
import streamlit as st
import google.generativeai as genai

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyBXApPu7Jq_4NULvcAX2VB2ujB2oVoPvVk'  
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Text Summarization Tool")

    # User input for text to summarize
    user_input = st.text_area(
        "Please enter the text you want to summarize below:",
        height=300
    )

    # Button to generate summary
    if st.button("Generate Summary"):
        if user_input.strip():
            # Create a prompt for generating the summary
            prompt = f"""
            Please summarize the following text in a concise manner:

            "{user_input}"

            The summary should capture the main points of the text in a few sentences.
            """

            try:
                # Use the Gemini generative model to generate the summary
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                summary = response.text

                # Store the generated summary in the session state to keep it persistent
                st.session_state.generated_summary = summary
                st.session_state.copy_status = "Copy Summary to Clipboard"  # Reset the copy button text

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("We couldn't generate the summary. Please try again later.")
        else:
            st.warning("Please provide the text to summarize.")

    # Check if the generated summary is in session state
    if 'generated_summary' in st.session_state:
        st.subheader("Your Generated Summary:")
        summary_text_area = st.text_area("Generated Summary:", st.session_state.generated_summary, height=200, key="summary_content")

        # Button to copy summary to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Summary to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var summaryContent = document.querySelector('#summary_content');
                    var range = document.createRange();
                    range.selectNode(summaryContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
