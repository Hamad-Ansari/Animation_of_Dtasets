import streamlit as st
import plotly.express as px
import pandas as pd

# App title
st.title(" Interactive Plotly Animations")
st.write("Explore various datasets with interactive animations using Plotly and Streamlit.")
st.subheader("  This app made by **Hammad zahid** ")
# Dataset selection
dataset = st.selectbox(
    "Choose a dataset:",
    ("Gapminder", "Iris", "Tips", "Stocks", "Custom Upload")
)

# Initialize empty figure
fig = None

# Load and plot selected dataset
if dataset == "Gapminder":
    df = px.data.gapminder()
    st.write("### Gapminder Data: Life Expectancy vs GDP")
    fig = px.scatter(
        df, x="gdpPercap", y="lifeExp", 
        size="pop", color="continent", 
        hover_name="country", animation_frame="year",
        log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90]
    )
    
elif dataset == "Iris":
    df = px.data.iris()
    st.write("### Iris Data: Sepal Dimensions")
    fig = px.scatter(
        df, x="sepal_width", y="sepal_length", 
        color="species", animation_frame="species_id",
        hover_name="species"
    )
    
elif dataset == "Tips":
    df = px.data.tips()
    st.write("### Restaurant Tips Data")
    fig = px.scatter(
        df, x="total_bill", y="tip", 
        color="sex", animation_frame="time",
        hover_name="day", facet_col="smoker"
    )
    
elif dataset == "Stocks":
    df = px.data.stocks()
    st.write("### Stock Prices Over Time")
    fig = px.line(
        df, x="date", y=[col for col in df.columns if col != "date"],
        animation_frame="date"
    )
    
elif dataset == "Custom Upload":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Preview of Uploaded Data")
        st.dataframe(df.head())
        
        # Let user select columns for animation
        cols = df.columns.tolist()
        x_axis = st.selectbox("Select X-axis column", cols)
        y_axis = st.selectbox("Select Y-axis column", cols)
        color_col = st.selectbox("Select color column (optional)", [None] + cols)
        size_col = st.selectbox("Select size column (optional)", [None] + cols)
        animation_col = st.selectbox("Select animation frame column", cols)
        
        # Create plot
        fig = px.scatter(
            df, x=x_axis, y=y_axis, 
            color=color_col, size=size_col,
            animation_frame=animation_col,
            hover_name=df.columns[0]  # Use first column as hover name
        )

# Display the plot if created
if fig:
    st.plotly_chart(fig, use_container_width=True)
    
    # Add some customization options
    with st.expander("Animation Controls"):
        st.write("Use the play button and slider below the chart to control the animation.")
        st.write("Hover over points to see details.")
        
    # Show raw data if desired
    if st.checkbox("Show raw data"):
        st.dataframe(df)

# Add these options after the main plot code

if fig and dataset != "Custom Upload":
    with st.expander("Advanced Customization"):
        # Animation speed control
        speed = st.slider("Animation speed", 50, 500, 200)
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = speed
        
        # Add trendlines for gapminder data
        if dataset == "Gapminder":
            add_trend = st.checkbox("Add trendlines")
            if add_trend:
                fig.update_traces(mode="markers+lines")
        
        # Download button for the animation
        st.download_button(
            label="Download Animation as HTML",
            data=fig.to_html(),
            file_name=f"{dataset}_animation.html",
            mime="text/html"
        )        