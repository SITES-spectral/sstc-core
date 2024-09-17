import pandas as pd
import altair as alt


import pandas as pd
import altair as alt

def plot_time_series_by_doy(df: pd.DataFrame, 
                     columns_to_plot: list, 
                     plot_options: dict = None, 
                     title: str = 'Time Series Plot', 
                     width: int = 600, 
                     height: int = 400, 
                     interactive: bool = True):
    """
    Plots a time series using Altair from a pandas DataFrame, focusing on the range of `day_of_year` (doy)
    where data exists, with optional plot customizations and general properties.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    columns_to_plot (list): List of column names to plot on the y-axis.
    plot_options (dict): Optional dictionary with customization for each column. The keys are the column names, 
                         and the values are dictionaries with Altair properties like:
                         - 'mark_type' (str): Mark type for the chart (e.g., 'line', 'point', 'bar').
                         - 'color' (str): Color of the line or points.
                         - 'axis' (str): Either 'left' or 'right' to specify which y-axis to use.
                         - 'size' (float): Size of the points (if using points).
                         - 'opacity' (float): Opacity level for the mark.
                         - 'strokeWidth' (float): Width of the line if using line marks.
    title (str): Title of the chart. Defaults to 'Time Series Plot'.
    width (int): Width of the chart. Defaults to 600.
    height (int): Height of the chart. Defaults to 400.
    interactive (bool): Whether the chart should be interactive (zoomable, scrollable). Defaults to True.

    Returns:
    alt.Chart: The Altair chart object.
    """
    # Ensure that 'day_of_year' is in the DataFrame
    if 'day_of_year' not in df.columns:
        raise ValueError("'day_of_year' column is required in the DataFrame")

    # Filter out rows where all selected columns are NaN
    df_filtered = df.dropna(subset=columns_to_plot, how='all')

    # Focus only on the range of day_of_year where data exists
    min_day = df_filtered['day_of_year'].min()
    max_day = df_filtered['day_of_year'].max()

    df_filtered = df_filtered[(df_filtered['day_of_year'] >= min_day) & (df_filtered['day_of_year'] <= max_day)]

    # Melt the dataframe to long format for Altair plotting
    df_melted = df_filtered.melt(id_vars=['day_of_year'], value_vars=columns_to_plot, 
                                 var_name='variable', value_name='value')

    # Initialize the base chart
    base = alt.Chart(df_melted).encode(
        x='day_of_year:Q'
    )

    # Container for layers
    layers = []

    # Add each column with custom options (if provided)
    for column in columns_to_plot:
        # Default options
        mark_type = 'line'  # Default to line
        color = 'variable:N'  # Default to Altair's color scheme
        y_axis = alt.Y('value:Q')  # Default to single y-axis
        size = None
        opacity = 1.0
        strokeWidth = 2.0  # Default line width for line marks

        # Apply custom options if available
        if plot_options and column in plot_options:
            # Set mark_type (e.g., line, point, bar)
            if 'mark_type' in plot_options[column]:
                mark_type = plot_options[column]['mark_type']

            # Set color
            if 'color' in plot_options[column]:
                color = alt.value(plot_options[column]['color'])
            
            # Set y-axis (left or right)
            if plot_options[column]['axis'] == 'right':
               y_axis = alt.Y('value:Q', axis=alt.Axis(title=column, orient='right'))
            else:
               y_axis = alt.Y('value:Q', axis=alt.Axis(title=column, orient='left'))
            
            # Set size (for point marks)
            if 'size' in plot_options[column]:
                size = plot_options[column]['size']

            # Set opacity
            if 'opacity' in plot_options[column]:
                opacity = plot_options[column]['opacity']
            
            # Set stroke width (for line marks)
            if 'strokeWidth' in plot_options[column]:
                strokeWidth = plot_options[column]['strokeWidth']

        # Create the chart for the current column based on mark_type
        if mark_type == 'line':
            layer = base.mark_line(strokeWidth=strokeWidth, opacity=opacity).encode(
                y=y_axis,
                color=color
            ).transform_filter(
                alt.datum.variable == column
            )
        elif mark_type == 'point':
            layer = base.mark_point(size=size, opacity=opacity).encode(
                y=y_axis,
                color=color
            ).transform_filter(
                alt.datum.variable == column
            )
        else:  # Fallback to line for unsupported mark types
            layer = base.mark_line().encode(
                y=y_axis,
                color=color
            ).transform_filter(
                alt.datum.variable == column
            )
        
        layers.append(layer)

    # Combine all layers into one chart
    chart = alt.layer(*layers).properties(
        width=width,
        height=height,
        title=title
    )

    # Add interactivity if specified
    if interactive:
        chart = chart.interactive()

    return chart
