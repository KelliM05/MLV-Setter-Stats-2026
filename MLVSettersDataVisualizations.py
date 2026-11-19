import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# 1. Load MLV setter statistics
# --------------------------------------------------

base_folder = Path(__file__).parent

file_path = base_folder / "MLV_Setter_Statistics.csv"

setters = pd.read_csv(file_path)

# --------------------------------------------------
# 2. Extract player statistics
# --------------------------------------------------

plot_data = setters[
    [
        "Player",
        "Team",
        "assists_sp",
        "assists_ast",
        "assists_ast_s"
    ]
].copy()

# Rename columns for visualization
plot_data = plot_data.rename(columns={
    "assists_sp": "Sets Played",
    "assists_ast": "Total Assists",
    "assists_ast_s": "Assists Per Set"
})

# Remove missing values
plot_data = plot_data.dropna()

# --------------------------------------------------
# 3. Create interactive scatter plot
# --------------------------------------------------

fig = px.scatter(
    plot_data,

    # X and Y axes
    x="Sets Played",
    y="Assists Per Set",

    # Color based on team
    color="Player",

    # Dot size based on sets played
    size="Total Assists",
    size_max=40,

    # Player identification
    hover_name="Player",

    # Information displayed when hovering
    hover_data={
        "Team": True,
        "Sets Played": True,
        "Total Assists": True,
        "Assists Per Set": ":.2f"
    },

    title="MLV Setters: Efficiency",

    labels={
        "Sets Played": "Total Sets Played (Volume)",
        "Assists Per Set": "Assists per Set (Efficiency)"
    },

    template="plotly_dark"
)

# --------------------------------------------------
# 4. Customize graph
# --------------------------------------------------

fig.update_traces(
    marker=dict(
        opacity=0.85,
        line=dict(width=1, color="white")
    )
)

fig.update_layout(
    title=dict(
        text="MLV Setters: Efficiency",
        x=0.02
    ),

    width=1200,
    height=700,

    legend_title_text="Team",

    xaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.12)"
    ),

    yaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.12)"
    )
)

# --------------------------------------------------
# 5. Export interactive HTML
# --------------------------------------------------

output_file = base_folder / "MLV_Setters_Efficiency.html"

fig.write_html(
    output_file,
    include_plotlyjs=True
)

print(f"Interactive graph saved to: {output_file}")

# Display graph
fig.show()
