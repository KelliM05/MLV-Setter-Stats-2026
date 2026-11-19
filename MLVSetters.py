
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from pathlib import Path
import re

# --------------------------------------------------
# 1. Locate project folders
# --------------------------------------------------

base_folder = Path(__file__).parent

players_folder = base_folder / "players"
output_folder = base_folder / "output"

output_folder.mkdir(exist_ok=True)

# --------------------------------------------------
# 2. Function to extract one player's statistics
# --------------------------------------------------

def extract_player_stats(file_path):

    print(f"\nProcessing: {file_path.name}")

    # Extract player and team names from filename
    filename_parts = file_path.stem.split(" - ")

    player_name = filename_parts[0].strip()
    team_name = filename_parts[1].strip() if len(filename_parts) > 1 else "Unknown"

    # Read HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()

    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Store statistics
    player_stats = {
        "Player": player_name,
        "Team": team_name
    }

    # --------------------------------------------------
    # 3. Extract every statistical category
    # --------------------------------------------------

    for table in soup.find_all("table"):

        # Find the heading associated with the table
        parent = table
        title = None

        for _ in range(5):
            parent = parent.parent

            if parent is None:
                break

            title = parent.find("h2")

            if title:
                break

        if title:

            category = title.get_text(strip=True)

            # Convert HTML table into DataFrame
            df = pd.read_html(StringIO(str(table)))[0]

            if df.empty:
                continue

            # Create category prefix
            category_name = re.sub(
                r"[^a-z0-9]+", "_", category.lower()
            ).strip("_")

            # Get the player's statistics
            stats = df.iloc[0]

            for column, value in stats.items():

                column_name = re.sub(
                    r"[^a-z0-9]+", "_", str(column).lower()
                ).strip("_")

                # Combine category and statistic names
                new_column = f"{category_name}_{column_name}"

                player_stats[new_column] = value

    return player_stats


# --------------------------------------------------
# 4. Process every player HTML file
# --------------------------------------------------

all_players = []

html_files = sorted(players_folder.glob("*.html"))

if not html_files:
    print("No HTML files found in the players folder.")

else:

    for file_path in html_files:

        try:
            player_data = extract_player_stats(file_path)

            all_players.append(player_data)

        except Exception as error:
            print(f"Could not process {file_path.name}: {error}")


# --------------------------------------------------
# 5. Combine all players into one DataFrame
# --------------------------------------------------

if all_players:

    combined_df = pd.DataFrame(all_players)

    # --------------------------------------------------
    # 6. Export all players into one CSV
    # --------------------------------------------------

    #output_file = output_folder / "MLV_Setter_Statistics.csv"

    combined_df.to_csv("MLV_Setter_Statistics.csv", index=False)

    # --------------------------------------------------
    # 7. Display results
    # --------------------------------------------------

    print("\nMLV SETTER STATISTICS")
    print("--------------------")

    print(combined_df.to_string(index=False))

    print(f"\nTotal players processed: {len(combined_df)}")
    #print(f"CSV saved to: {output_file}")

else:
    print("No player statistics were collected.")
