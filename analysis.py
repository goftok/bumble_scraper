import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
from db_bot.models import MainInformationModel, get_session  # adjust the import according to your file structure


# Replace with your actual database paths
image_path = "/Users/goftok/github/db_bot/data/thailand/9Dec23_40k_thailand_image_043.db"
main_path = "/Users/goftok/github/db_bot/data/thailand/9Dec23_10k_thailand_main_043.db"

# Obtain sessions using the get_session function
main_session, _ = get_session(main_path, image_path)

# Query data using the main session
query = main_session.query(MainInformationModel).all()

# Convert query results to a pandas DataFrame
df = pd.DataFrame([row.__dict__ for row in query])
main_session.close()

# Remove the internal SQLAlchemy attribute
df = df.drop("_sa_instance_state", axis=1)

fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 20))  # Adjust as needed

# Top 10 most popular names
top_names = df["name"].value_counts().head(10)
sns.barplot(x=top_names.values, y=top_names.index, ax=axes[0, 0])
axes[0, 0].set_title("Top 10 Most Popular Names")
axes[0, 0].set_xlabel("Count")
axes[0, 0].set_ylabel("Name")

# Age distribution
sns.histplot(df["age"], kde=True, ax=axes[0, 1])
axes[0, 1].set_title("Age Distribution")
axes[0, 1].set_xlabel("Age")
axes[0, 1].set_ylabel("Count")
axes[0, 1].set_xlim(18, 60)

# Count by City
city_counts = df["city"].value_counts().head(10)
city_counts.plot(kind="bar", ax=axes[1, 0])
axes[1, 0].set_title("Counts by City")
axes[1, 0].set_xlabel("City")
axes[1, 0].set_ylabel("Count")
axes[1, 0].tick_params(axis="x", rotation=45)

# From Distribution
from_counts = df["from_"].value_counts().head(10)
from_counts.plot(kind="bar", ax=axes[1, 1])
axes[1, 1].set_title("From city Distribution")
axes[1, 1].set_xlabel("From")
axes[1, 1].set_ylabel("Count")
axes[1, 1].tick_params(axis="x", rotation=45)

# Lives In Distribution
lives_in_counts = df["lives_in"].value_counts().head(10)
lives_in_counts.plot(kind="bar", ax=axes[2, 0])
axes[2, 0].set_title("Lives In Distribution")
axes[2, 0].set_xlabel("Lives In")
axes[2, 0].set_ylabel("Count")
axes[2, 0].tick_params(axis="x", rotation=45)

# Gender Distribution
gender_counts = df["gender_badge"].value_counts()
gender_counts.plot(kind="bar", ax=axes[2, 1])
axes[2, 1].set_title("Gender Distribution")
axes[2, 1].set_xlabel("Gender")
axes[2, 1].set_ylabel("Count")

# Verification Distribution
verification_counts = df["verification"].value_counts()
verification_counts.plot(kind="bar", ax=axes[3, 0])
axes[3, 0].set_title("Verification Distribution")
axes[3, 0].set_xlabel("Verification Status")
axes[3, 0].set_ylabel("Count")

# Height Distribution
df["height_numeric"] = (
    df["height_badge"].str.replace(" cm", "").replace("<91", "91").replace(">220", "220").astype(float)
)
sns.histplot(df["height_numeric"], kde=True, ax=axes[3, 1])
axes[3, 1].set_title("Height Distribution")
axes[3, 1].set_xlabel("Height (cm)")
axes[3, 1].set_ylabel("Count")
axes[3, 1].set_xlim(140, 190)

plt.tight_layout()
plt.savefig("/Users/goftok/github/db_bot/summary.png")

badges = [
    "exercise_badges",
    "drinking_badge",
    "smoking_badge",
    "family_plans_badge",
    "political_badge",
    "religion_badge",
    # "cannabis_badge",
    "star_sign_badge",
    "intentions_badge",
]

# Set up the subplot grid
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 20))  # Adjust nrows and ncols based on the number of badges
axes = axes.flatten()  # Flatten the axes array for easy iteration

# Loop through the badges and create a bar plot for each
for i, badge in enumerate(badges):
    badge_counts = df[badge].value_counts()
    axes[i].bar(badge_counts.index, badge_counts.values)
    axes[i].set_title(f"{badge} Distribution")
    axes[i].set_xlabel(badge)
    axes[i].set_ylabel("Count")
    axes[i].tick_params(axis="x", rotation=45)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.savefig("/Users/goftok/github/db_bot/badges.png")
