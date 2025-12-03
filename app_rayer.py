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
    # DEBUG: Test what tables and columns exist
    try:
        tables_df = pd.read_sql("SHOW TABLES", connection)
        st.write("Available tables:", tables_df)
        
        columns_df = pd.read_sql("SHOW COLUMNS FROM restaurant", connection)
        st.write("Columns in restaurant table:", columns_df)
    except Exception as e:
        st.error(f"Debug error: {e}")

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

    st.header("This HW was submitted by **Ally Rayer** of ITOM6265")

    # Using columns for better layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🎯 Approach and Implementation")

        st.write("""
        I connected to the MySQL database using the mysql.connector library with credentials provided 
        for DigitalOcean. I used pandas read_sql function to execute queries and automatically convert 
        results into DataFrames, which made data manipulation much easier. The most challenging part 
        was understanding SQL pattern matching with LIKE and properly handling NULL values in coordinates. 
        I tested my SQL queries first in a database client before implementing them in Streamlit to ensure 
        they returned correct results. I chose Folium for mapping because it integrates well with Streamlit 
        and provides interactive maps with customizable tile layers.
        """)

    with col2:
        st.subheader("🎨 Customizations Made")

        st.write("""
        I made several customizations to enhance the user experience:
        
        1. Layout: Used Streamlit's column system to create a two-column layout in the query tab, 
           placing filters on the left and results on the right for better visual organization.
        
        2. Map Tiles: Changed from the default OpenStreetMap to CartoDB Positron tiles, which 
           provides a cleaner, lighter aesthetic that makes restaurant markers more visible.
        
        3. Data Display: Configured the results table with custom column headers, number formatting 
           for votes, and increased height for better readability. Added success/warning messages with 
           result counts.
        
        4. Other: Added blue cutlery icons for map markers, hover tooltips showing restaurant names, 
           and captions explaining map functionality to users.
        """)

    # Technologies section
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
        # Get min/max votes with better error handling
        min_votes = 0
        max_votes = 1000
        
        try:
            vote_query = "SELECT MIN(votes) as min_votes, MAX(votes) as max_votes FROM business_location WHERE votes IS NOT NULL"
            vote_stats = pd.read_sql(vote_query, connection)
            
            if not vote_stats.empty and vote_stats['min_votes'][0] is not None:
                min_votes = int(vote_stats['min_votes'][0])
                max_votes = int(vote_stats['max_votes'][0])
        except Exception as e:
            st.warning(f"Using default vote range. Database message: {e}")

        # Create layout with columns
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### Filter Options")

            name_pattern = st.text_input(
                "Pattern of Name:",
                value="",
                help="Enter part of a restaurant name to search for (e.g., 'Pizza', 'Dishoom')",
                placeholder="e.g., Pizza"
            )

            vote_range = st.slider(
                "Range of votes to search for:",
                min_value=min_votes,
                max_value=max_votes,
                value=(min_votes, max_votes),
                help="Drag the handles to filter restaurants by vote count"
            )

            search_button = st.button(
                "🔍 Get results", 
                type="primary",
                use_container_width=True
            )

        with col2:
            st.markdown("### Search Results")

            if search_button:
                try:
                    # Build the SQL query
                    if name_pattern:
                        query = f"""
                            SELECT name, votes, city
                            FROM business_location
                            WHERE votes BETWEEN {vote_range[0]} AND {vote_range[1]}
                                AND name LIKE '%{name_pattern}%'
                            ORDER BY votes DESC
                        """
                    else:
                        query = f"""
                            SELECT name, votes, city
                            FROM business_location
                            WHERE votes BETWEEN {vote_range[0]} AND {vote_range[1]}
                            ORDER BY votes DESC
                        """
                    
                    # Execute query
                    df = pd.read_sql(query, connection)
                    
                    if not df.empty:
                        st.success(f"✅ Found {len(df)} restaurant(s) matching your criteria")
                        
                        st.dataframe(
                            df,
                            use_container_width=True,
                            height=400,
                            hide_index=True,
                            column_config={
                                "name": st.column_config.TextColumn("Restaurant Name", width="large"),
                                "votes": st.column_config.NumberColumn("Votes", format="%d"),
                                "city": st.column_config.TextColumn("City", width="medium"),
                            }
                        )
                    else:
                        st.warning("⚠️ No restaurants found matching your criteria. Try adjusting your filters.")
                        
                except Exception as e:
                    st.error(f"❌ Query error: {e}")
                    st.info("Try adjusting your search criteria or check the database structure.")
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
            display_map = st.button(
                "🗺️ Display map!", 
                type="primary", 
                use_container_width=True
            )
            st.caption("Map of restaurants in London. Click on teardrop to check names.")

        if display_map:
            
            with st.spinner("Loading restaurant locations..."):
                
                # Query: Get all restaurants with valid coordinates
                location_query = """
                    SELECT name, latitude, longitude
                    FROM business_location
                    WHERE latitude IS NOT NULL 
                        AND longitude IS NOT NULL
                """
                
                try:
                    # Execute query
                    locations_df = pd.read_sql(location_query, connection)
                    
                    # Check if we got results
                    if locations_df.empty:
                        st.warning("No restaurant locations found in the database.")
                    else:
                        # Create the map centered on London
                        london_map = folium.Map(
                            location=[51.5074, -0.1278],
                            zoom_start=11,
                            tiles='CartoDB Positron'
                        )
                        
                        # Add a marker for each restaurant
                        for idx, row in locations_df.iterrows():
                            folium.Marker(
                                location=[row['latitude'], row['longitude']],
                                popup=folium.Popup(row['name'], max_width=200),
                                tooltip=row['name'],
                                icon=folium.Icon(color='blue', icon='cutlery', prefix='fa')
                            ).add_to(london_map)
                        
                        # Display the map
                        st_folium(
                            london_map,
                            width=None,
                            height=600,
                            use_container_width=True
                        )
                        
                        # Show success message with count
                        st.success(f"✅ Successfully mapped {len(locations_df)} restaurants")
                        
                except Error as e:
                    st.error(f"❌ Database error: {e}")
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
