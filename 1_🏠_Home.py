# %% Libraries

import streamlit as st

# %% Parameters for Streamlit

# Set the page configuration for Streamlit
st.set_page_config(page_title = "Home", page_icon = "🏠")
st.title("🏠 Home")
st.sidebar.image("./images/logo.png")

# %% Functions

def text_home() -> None:

    """
    Display the home page content.
    """

    # Text related to the project summary
    title_abstract = "# Abstract"
    abstract_paragraph = """
        This application offers several features to enhance document management. It includes a **Metadata** page to edit document metadata and add customized cover pages. 
        Additionally, the **PDF to Markdown** page provides a tool to convert PDF documents into Markdown format, facilitating easier content 
        editing and management. These features combine to provide a comprehensive solution for handling and analyzing various types 
        of documents and data.
    """
    
    # Text related to the metadata section
    title_metadata = "# Metadata"
    metadata_paragraph = """
        There is a "**Metadata**" page that allows users to modify the metadata of documents and add a cover page with the document's name. 
        This feature provides users with the ability to customize and organize their documents more effectively, ensuring that each document 
        contains all the necessary information and a professional appearance.
    """

    # Text related to the PDF to Markdown section
    title_pdf_to_md = "# PDF to Markdown"
    pdf_to_md_paragraph = """
        Another feature is the "**PDF to Markdown**" page, which enables users to analyze a PDF document and convert it to Markdown (MD) format. 
        This functionality is particularly useful for users who need to extract and edit content from PDF files, providing a seamless way to 
        transform static documents into editable Markdown text.
    """

    # Display the content
    st.markdown(title_abstract)
    st.markdown(abstract_paragraph)

    st.markdown(title_metadata)
    st.markdown(metadata_paragraph)

    st.markdown(title_pdf_to_md)
    st.markdown(pdf_to_md_paragraph)

def main() -> None:

    """
    Main entry point of the application.
    """

    text_home()

# %% Main

if __name__ == '__main__':

    main()