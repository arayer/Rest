# ============================================
# Restaurant Dashboard - Streamlit Application Template
# ITOM6265 - Database Homework
#
# INSTRUCTIONS:
# 1. Update database credentials in Block 3
# 2. Fill in all TODO sections
# 3. Test each tab individually
# 4. Read the hints and documentation links
# ============================================

# Block 1: Import required libraries (KEEP THIS AS-IS)
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import folium
from streamlit_folium import st_folium

# Block 2: Page configuration (KEEP THIS AS-IS)
st.set_page_config(
    page_title="ITOM6265-HW1",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Block 3: Database connection (UPDATE CREDENTIALS ONLY)
# ===== UPDATE THESE VALUES WITH YOUR DATABASE INFORMATION =====
try:
    connection = mysql.connector.connect(
        host='db-mysql-itom-do-user-28250611-0.j.db.ondigitalocean.com',  # TODO: Update with your host
        port=25060,  # TODO: Update with your port (usually 3306 for local, 25060 for DigitalOcean)
        user='restaurant_readonly',  # TODO: Update with your username
        password='SecurePassword123!',  # TODO: Update with your password
        database='restaurant'  # TODO: Update with your database name
    )
    db_connected = True
    st.success("✅ Database connected successfully!")
except Error as e:
    st.error(f"❌ Error connecting to MySQL Database: {e}")
    st.info("Please check your database credentials in the code (Block 3)")
    db_connected = False
    connection = None

# Block 4: Sidebar navigation (KEEP THIS AS-IS)
st.sidebar.title("🍽️ ITOM6265-HW1")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["HW Summary", "Q1-DB Query", "Q2-Maps"],
    help="Select a page to navigate"
)
st.sidebar.markdown("---")
st.sidebar.info("Restaurant Database Dashboard")

# ============================================
# TAB 1: HW SUMMARY
# ============================================
if page == "HW Summary":
    st.markdown("# 📝 Homework Summary")
    st.markdown("---")

    # TODO: Replace [YOUR NAME] with your actual name
    st.header("This HW was submitted by **Ally Rayer** of ITOM6265")

    # Using columns for better layout (KEEP THIS STRUCTURE)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🎯 Approach and Implementation")

        # TODO: Write 3-4 sentences about your approach
        # HINTS:
        # - How did you connect to the database?
        # - What libraries did you use and why?
        # - What challenges did you face?
        # - How did you test your queries?
        st.write("Using MySQL.Connector, I established a connection to the MySQL database and used the pandas programming library to pull data into DataFrames. I tested SQL Queries to ensure they worked before adding them to my streamlit workflow. I then used Folium for the maps because it works well with Streamlit to create interactive visualizations. "
        TODO: Replace this with your approach description.

        Example topics to cover:
        - I used pandas read_sql to simplify database queries...
        - The most challenging part was...
        - I tested my SQL queries by...
        - I chose Folium for mapping because...
        """)

    with col2:
        st.subheader("🎨 Customizations Made")

        # TODO: Describe your customizations (REQUIRED for 10% of grade)
        # You must customize at least 3 things:
        # 1. Layout (columns, containers, etc.)
        # 2. Map tiles (not default OpenStreetMap)
        # 3. Data display (colors, formatting, etc.)
        st.write("""
        TODO: Replace this with your customizations.

        Required customizations (10% of grade):
        1. **Layout:** [Describe your layout choices]
        2. **Map Tiles:** [Which tiles did you choose and why]
        3. **Data Display:** [How did you format the results]
        4. **Other:** [Any additional customizations]
        """)

    # Technologies section (You can keep this or modify it)
    st.markdown("### 🛠️ Technologies Used")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Frontend:** Streamlit")
    with col2:
        st.info("**Database:** MySQL + Pandas")
    with col3:
        st.info("**Maps:** Folium")

# ============================================
# TAB 2: Q1-DB QUERY
# ============================================
elif page == "Q1-DB Query":
    st.markdown("# 🔍 Database Query")
    st.markdown("---")

    if not db_connected:
        st.error("Database connection not available. Please check your connection settings.")
    else:
        # ===== STUDENT TODO: STEP 1 - Get Min/Max Votes =====
        # TODO: Query the database to get minimum and maximum votes
        #
        # SQL CONCEPTS YOU'LL NEED:
        # - MIN() function: Gets the smallest value in a column
        # - MAX() function: Gets the largest value in a column
        # - AS: Give your results a name (alias) you can reference
        # - WHERE: Filter out NULL values
        #
        # THINK ABOUT:
        # - What table has the votes column?
        # - How do you get both MIN and MAX in one query?
        # - Why should you filter out NULL values?
        #
        # PANDAS HINT:
        # - Use pd.read_sql() to execute your query
        # - The result will be a DataFrame
        # - Access values with: df['column_name'][0]
        #
        # For now, using placeholder values (REPLACE THESE):
        # Query to get the minimum and maximum votes from the database
            vote_query = """
                SELECT 
                    MIN(votes) as min_votes, 
                    MAX(votes) as max_votes 
                FROM restaurant 
                WHERE votes IS NOT NULL
            """
        vote_stats = pd.read_sql(vote_query, connection)
        min_votes = int(vote_stats['min_votes'][0])
        max_votes = int(vote_stats['max_votes'][0])

        # TEST: Display the values to verify they're correct
        st.write(f"DEBUG: Min votes = {min_votes}, Max votes = {max_votes}")  # Remove this after testing

        # Create layout with columns
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### Filter Options")

            # ===== STUDENT TODO: STEP 2 - Create Input Widgets =====

            # TODO: Create a text input for restaurant name pattern
            # DOCUMENTATION: https://docs.streamlit.io/library/api-reference/widgets/st.text_input
            #
            # Requirements:
            # - Label: "Pattern of Name:"
            # - Default value: "" (empty string)
            # - Add a help parameter explaining what it does
            # - Add a placeholder showing an example
            #
            # EXAMPLE:
            # name_pattern = st.text_input(
            #     "Your Label",
            #     value="",
            #     help="Help text here",
            #     placeholder="e.g., Pizza"
            # )

            name_pattern = "name_pattern = st.text_input(
    "Pattern of Name:",
    value="",
    help="Enter part of a restaurant name to search for (e.g., 'Pizza', 'Dishoom')",
    placeholder="e.g., Pizza"
)"  # TODO: Replace with actual text_input widget

            # TODO: Create a slider for vote range
            # DOCUMENTATION: https://docs.streamlit.io/library/api-reference/widgets/st.slider
            #
            # Requirements:
            # - Label: "Range of votes to search for:"
            # - Use min_votes and max_votes from Step 1
            # - Default should show full range
            # - Returns a tuple (min_selected, max_selected)
            #
            # EXAMPLE:
            # vote_range = st.slider(
            #     "Your Label",
            #     min_value=min_votes,
            #     max_value=max_votes,
            #     value=(min_votes, max_votes)
            # )

            vote_range = (min_votes, max_votes)  # TODO: Replace with actual slider widget

            # TODO: Create a search button
            # DOCUMENTATION: https://docs.streamlit.io/library/api-reference/widgets/st.button
            #
            # Requirements:
            # - Text: "🔍 Get results"
            # - Use type="primary" for styling
            # - Use use_container_width=True for full width
            #
            # EXAMPLE:
            # search_button = st.button("Button text", type="primary")

            search_button = False  # TODO: Replace with actual button

        with col2:
            st.markdown("### Search Results")

            # ===== STUDENT TODO: STEP 3 - Query and Display Results =====
            if search_button:  # This runs when button is clicked

                # TODO: Build and execute SQL query
                #
                # REQUIREMENTS:
                # 1. Select these columns: name, votes, city
                # 2. Filter by vote range (user selected range from slider)
                # 3. Filter by name pattern if user entered one
                # 4. Sort results by votes (highest first)
                #
                # SQL CONCEPTS YOU'LL NEED:
                # - SELECT: Choose which columns to retrieve
                # - WHERE: Filter your results
                # - BETWEEN: Check if value is in a range (e.g., BETWEEN 100 AND 500)
                # - LIKE: Pattern matching (use % as wildcard)
                # - AND: Combine multiple conditions
                # - ORDER BY: Sort your results (use DESC for descending)
                #
                # HINT: You need different queries depending on whether name_pattern is empty
                # Think about: if name_pattern:
                #                 # Query with both filters
                #             else:
                #                 # Query with only vote filter
                #
                # PATTERN MATCHING HINT:
                # - '%pizza%' matches anything containing "pizza"
                # - 'pizza%' matches anything starting with "pizza"
                # - '%pizza' matches anything ending with "pizza"

                # TODO: Execute your query using pandas
                # Remember: df = pd.read_sql(your_query_string, connection)

                # TODO: Check if results exist and display them
                # COMMON MISTAKE: Forgetting to check if dataframe is empty
                #
                # if not df.empty:
                #     st.success(f"Found {len(df)} restaurants")
                #
                #     # Display with nice formatting
                #     st.dataframe(
                #         df,
                #         use_container_width=True,
                #         height=400,
                #         hide_index=True,
                #         column_config={
                #             "name": st.column_config.TextColumn("Restaurant Name"),
                #             "votes": st.column_config.NumberColumn("Votes", format="%d"),
                #             "city": st.column_config.TextColumn("City"),
                #         }
                #     )
                # else:
                #     st.warning("No restaurants found matching your criteria.")

                st.info("TODO: Query results will appear here")

            # TEST YOUR CODE:
            # 1. First test with empty name pattern (should show all restaurants)
            # 2. Test with "Dishoom" in name field (should show 2 results)
            # 3. Test with vote range 0-500 (should filter by votes)
            # 4. Test with both filters combined

# ============================================
# TAB 3: Q2-MAPS
# ============================================
elif page == "Q2-Maps":
    st.markdown("# 🗺️ Restaurant Map")
    st.markdown("---")

    if not db_connected:
        st.error("Database connection not available. Please check your connection settings.")
    else:
        # Center the button using columns
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # ===== STUDENT TODO: STEP 1 - Create Map Button =====
            # TODO: Create a button labeled "🗺️ Display map!"
            # Requirements:
            # - Use type="primary"
            # - Use use_container_width=True
            # - Add caption: "Map of restaurants in London. Click on teardrop to check names."
            #
            # EXAMPLE:
            # display_map = st.button("🗺️ Display map!", type="primary", use_container_width=True)
            # st.caption("Your caption here")

            display_map = False  # TODO: Replace with actual button
            st.caption("TODO: Add the required caption here")

        if display_map:  # This runs when button is clicked

            # ===== STUDENT TODO: STEP 2 - Query Location Data =====
            # TODO: Get restaurant locations from database
            #
            # REQUIREMENTS:
            # - You need: restaurant names and their coordinates
            # - Only get restaurants that have valid coordinates
            # - Think about what "valid" means for latitude/longitude
            #
            # SQL CONCEPTS TO USE:
            # - SELECT: Choose the columns you need for mapping
            # - WHERE: Filter your data
            # - IS NOT NULL: Check if a value exists
            # - AND: Combine multiple conditions
            #
            # THINK ABOUT:
            # - What columns do you need for placing markers on a map?
            # - Why is it important to filter NULL coordinates?
            # - What happens if you try to plot a NULL location?
            #
            # PANDAS HINT:
            # - Store your query as a multi-line string using triple quotes
            # - Execute with pd.read_sql()

            # TODO: Execute query and get locations_df

            # ===== STUDENT TODO: STEP 3 - Create Folium Map =====
            # TODO: Initialize a Folium map centered on London
            #
            # DOCUMENTATION: https://python-visualization.github.io/folium/
            #
            # London coordinates: latitude=51.5074, longitude=-0.1278
            #
            # REQUIRED CUSTOMIZATION: Use custom tiles (not default)
            # Options:
            # - 'CartoDB Positron' (light/clean)
            # - 'CartoDB Dark_Matter' (dark theme)
            # - 'Stamen Terrain' (topographic)
            # - 'Stamen Toner' (high contrast)
            #
            # EXAMPLE:
            # london_map = folium.Map(
            #     location=[51.5074, -0.1278],
            #     zoom_start=11,
            #     tiles='CartoDB Positron'  # Choose your tile style
            # )

            # ===== STUDENT TODO: STEP 4 - Add Markers =====
            # TODO: Loop through locations_df and add a marker for each restaurant
            #
            # REQUIREMENTS:
            # - Each marker should show restaurant name in popup
            # - Use blue markers
            # - Add tooltip for hover effect
            #
            # EXAMPLE CODE:
            # for idx, row in locations_df.iterrows():
            #     folium.Marker(
            #         location=[row['latitude'], row['longitude']],
            #         popup=folium.Popup(row['name'], max_width=200),
            #         tooltip=row['name'],  # Shows on hover
            #         icon=folium.Icon(color='blue', icon='cutlery', prefix='fa')
            #     ).add_to(london_map)

            # ===== STUDENT TODO: STEP 5 - Display Map =====
            # TODO: Use st_folium to display the map
            #
            # DOCUMENTATION: https://github.com/randyzwitch/streamlit-folium
            #
            # EXAMPLE:
            # st_folium(
            #     london_map,
            #     width=None,  # Full width
            #     height=600,
            #     use_container_width=True
            # )
            #
            # BONUS: Display count of mapped restaurants
            # st.success(f"Successfully mapped {len(locations_df)} restaurants")

            st.info("TODO: Map will appear here")

            # TEST YOUR MAP:
            # 1. Check that all restaurants with valid coordinates appear
            # 2. Click on markers to see restaurant names
            # 3. Verify custom tile style is applied (not default)
            # 4. Test hover tooltips

# ============================================
# FOOTER (OPTIONAL - You can modify this)
# ============================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7f8c8d; font-size: 0.9em;'>
        ITOM6265 Database Management | Restaurant Dashboard | Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)

# Block 9: Close database connection (KEEP THIS AS-IS)
if connection and connection.is_connected():
    connection.close()

# ============================================
# CHECKLIST BEFORE SUBMISSION:
# ============================================
# □ Updated database credentials
# □ Replaced [YOUR NAME] with actual name
# □ Tab 1: Wrote approach and customizations
# □ Tab 2: Query works with both filters
# □ Tab 2: Results display in formatted table
# □ Tab 3: Map displays with custom tiles
# □ Tab 3: All markers clickable with names
# □ Removed all TODO comments
# □ Removed all DEBUG statements
# □ Tested all functionality
# ============================================
