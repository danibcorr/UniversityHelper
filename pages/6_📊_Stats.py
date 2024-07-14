# %% Libraries

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# %% Parameters for Streamlit

# Set the page configuration for Streamlit
st.set_page_config(page_title="Stats", page_icon="📊", layout="wide")

# Set the title of the page
st.title("📊 Stats")

# Add a logo to the sidebar
st.sidebar.image("./images/logo.png")

# %% Functions

def load_data() -> pd.DataFrame:

    """
    Load a CSV file from a user-input path and convert the 'Date' column to datetime.
    
    Returns:
        pd.DataFrame: The loaded data
    """
    
    data_path = st.text_input("Data path with csv format", "./data/data.csv")
    data = pd.read_csv(data_path)
    data['Date'] = pd.to_datetime(data['Date'])
    
    return data

def score_evolution(data: pd.DataFrame) -> None:
    
    """
    Plot the evolution of scores over time for a selected subject.
    
    Args:
        data (pd.DataFrame): The data to plot
    """

    # Select a subject from the data
    subject = st.selectbox("Select subject", data["Subject"].unique())
    
    # Filter the data for the selected subject and sort by date
    df_subject = data[data['Subject'] == subject].sort_values(by='Date')
    
    # Create a line plot of the score evolution
    fig = px.line(df_subject, x='Date', y='Score', title=f'Evolution score of the {subject}', markers=True)
    fig.update_traces(marker=dict(size=15, color='red'))
    fig.update_layout(xaxis_title='Date', yaxis_title='Score')
    
    # Display the plot
    st.plotly_chart(fig)

def year_comparison(data: pd.DataFrame) -> None:

    """
    Plot a comparison of average scores between different years for each subject.
    
    Args:
        data (pd.DataFrame): The data to plot
    """
    
    # Extract the year from the date column
    data['Year'] = data['Date'].dt.year
    
    # Group the data by subject and year, and calculate the mean score
    subject_years = data.groupby(['Subject', 'Year'])['Score'].mean().unstack().reset_index()
    
    # Create a bar plot of the year comparison
    fig = px.bar(subject_years, x='Subject', y=subject_years.columns[1:], title='Comparison of subjects between different years')
    fig.update_layout(barmode='group', xaxis_title='Subject', yaxis_title='Average Score')
    
    # Display the plot
    st.plotly_chart(fig)

def general_metrics(data: pd.DataFrame, top: int = 3) -> None:

    """
    Display general metrics, including the average score for all subjects and the top subjects by average score.
    
    Args:
        data (pd.DataFrame): The data to calculate metrics from
        top (int, optional): The number of top subjects to display. Defaults to 3.
    """
    
    # Calculate the average score for all subjects
    mean_score = data['Score'].mean()
    st.metric("Average score for all subjects", f"{mean_score:.2f}")
    
    # Calculate the top subjects by average score
    top_subjects_df = data.groupby('Subject')['Score'].mean().nlargest(top).reset_index()
    st.metric("Average score for all subjects", f"{top_subjects_df['Subject'].values}")

def main() -> None:
    
    # Create two columns
    col1, col2 = st.columns(2)

    with col1:

        # File configuration section
        st.subheader("File Configuration")
        
        # Load the data
        data = load_data()
        
        # Display the data
        st.dataframe(data, use_container_width=True, hide_index=True)

    with col2:
        
        # General metrics section
        st.subheader("General Metrics")
        
        # Calculate and display general metrics
        general_metrics(data)

    # Stats section
    st.subheader("Stats")
    score_evolution(data)
    year_comparison(data)

# %% Main

if __name__ == '__main__':
    
    main()