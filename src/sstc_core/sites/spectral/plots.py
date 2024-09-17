import pandas as pd
import altair as alt


def plot_time_series(df: pd.DataFrame, columns_to_plot: list, title: str ):
    """
    Plots a time series using Altair from a pandas DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    columns_to_plot (list): List of column names to plot on the y-axis.
    
    Returns:
    alt.Chart: The Altair chart object.
    """
    # Ensure that 'day_of_year' is in the DataFrame
    if 'day_of_year' not in df.columns:
        raise ValueError("'day_of_year' column is required in the DataFrame")
    
    # Melt the dataframe to long format for Altair plotting
    df_melted = df.melt(id_vars=['day_of_year'], value_vars=columns_to_plot, 
                        var_name='variable', value_name='value')
    
    # Create the Altair chart
    chart = alt.Chart(df_melted).mark_line().encode(
        x='day_of_year:Q',
        y='value:Q',
        color='variable:N'
    ).properties(
        width=600,
        height=400,
        title=title,
    ).interactive()

    return chart
