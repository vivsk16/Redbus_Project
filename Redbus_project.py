import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu

# 📌 Read CSV files safely with exception handling
def read_csv_safe(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        slt.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

# 🚌 Load bus route data
df_k = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_k.csv")
df_ap = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_ap.csv")
df_ts = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_ts.csv")
df_wb = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_wb.csv")
df_bh = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_bh.csv")
df_rj = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_rj.csv")
df_as = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_as.csv")
df_ch = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_ch.csv")
df_pb = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_pb.csv")
df_ml = read_csv_safe(r"C:\Users\vivsk\Redbus_Project\df_ml.csv")

# Convert route names into lists (Handle missing columns)
def get_route_list(df):
    return df["Route_name"].tolist() if "Route_name" in df.columns else []

lists_k = get_route_list(df_k)
lists_ap = get_route_list(df_ap)
lists_ts = get_route_list(df_ts)
lists_wb = get_route_list(df_wb)
lists_bh = get_route_list(df_bh)
lists_rj = get_route_list(df_rj)
lists_as = get_route_list(df_as)
lists_ch = get_route_list(df_ch)
lists_pb = get_route_list(df_pb)
lists_ml = get_route_list(df_ml)

# 🎨 Streamlit Page Configuration
slt.set_page_config(layout="wide")

# 🔹 Navigation Menu
web = option_menu(
    menu_title="🚌OnlineBus",
    options=["Home", "📍States and Routes"],
    icons=["house", "info-circle"],
    orientation="horizontal"
)

# 🏠 **Home Page**
if web == "Home":
   #slt.image("t_500x300.jpg", width=200)
    slt.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    
    slt.subheader(":blue[Domain:]  Transportation")
    slt.subheader(":blue[Objective:] ")
    slt.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data.")
    
    slt.markdown("### Technologies Used:")
    slt.markdown("- **Selenium**: Automates web scraping from Redbus.")
    slt.markdown("- **Pandas**: Manages data in structured format.")
    slt.markdown("- **MySQL**: Stores bus data for querying.")
    slt.markdown("- **Streamlit**: Creates an interactive dashboard.")
    
    slt.subheader(":blue[Developed by:]  Vivek")

# 📍 **States and Routes Page**
if web == "📍States and Routes":
    # Select a state
    S = slt.selectbox(
        "Lists of States", 
        ["Kerala", "Andhra Pradesh", "Telangana", "West Bengal", "Bihar", 
         "Rajasthan", "Assam", "Chandigarh", "Punjab", "Meghalaya"]
    )

    col1, col2 = slt.columns(2)

    with col1:
        select_type = slt.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))

    with col2:
        select_fare = slt.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))

    TIME = slt.time_input("Select the time")

    # Function to filter data based on bus type, fare range, and time
    def filter_bus_data(state_name, route_list):
        selected_route = slt.selectbox("List of routes", route_list)

        def get_filtered_data(bus_type, fare_range):
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="vivek",  # Change to your actual MySQL password
                    database="RED_BUS_DETAILS"
                )
                my_cursor = conn.cursor()

                # Define fare range conditions
                if fare_range == "50-1000":
                    fare_min, fare_max = 50, 1000
                elif fare_range == "1000-2000":
                    fare_min, fare_max = 1000, 2000
                else:
                    fare_min, fare_max = 2000, 100000

                # Define bus type conditions
                if bus_type == "sleeper":
                    bus_type_condition = "Bus_type LIKE '%Sleeper%'"
                elif bus_type == "semi-sleeper":
                    bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper%'"
                else:
                    bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

                # SQL Query
                query = f'''
                    SELECT * FROM bus_details 
                    WHERE Price BETWEEN {fare_min} AND {fare_max}
                    AND Route_name = "{selected_route}"
                    AND {bus_type_condition}
                    AND Start_time >= "{TIME}"
                    ORDER BY Price, Start_time DESC
                '''
                
                my_cursor.execute(query)
                out = my_cursor.fetchall()
                conn.close()

                # Convert result to DataFrame
                df = pd.DataFrame(out, columns=[
                    "ID", "Bus_name", "Bus_type", "Start_time", "End_time", 
                    "Total_duration", "Price", "Seats_Available", "Ratings", 
                    "Route_link", "Route_name"
                ])
                return df

            except Exception as e:
                slt.error(f"Database error: {e}")
                return pd.DataFrame()

        # Get filtered data
        df_result = get_filtered_data(select_type, select_fare)

        # Display DataFrame in Streamlit
        if not df_result.empty:
            slt.dataframe(df_result)
        else:
            slt.warning("No matching bus data found.")

    # 🔥 Handle selection for each state
    if S == "Kerala":
        filter_bus_data("Kerala", lists_k)
    elif S == "Andhra Pradesh":
        filter_bus_data("Andhra Pradesh", lists_ap)
    elif S == "Telangana":
        filter_bus_data("Telangana", lists_ts)
    elif S == "West Bengal":
        filter_bus_data("West Bengal", lists_wb)
    elif S == "Bihar":
        filter_bus_data("Bihar", lists_bh)
    elif S == "Rajasthan":
        filter_bus_data("Rajasthan", lists_rj)
    elif S == "Assam":
        filter_bus_data("Assam", lists_as)
    elif S == "Chandigarh":
        filter_bus_data("Chandigarh", lists_ch)
    elif S == "Punjab":
        filter_bus_data("Punjab", lists_pb)
    elif S == "Meghalaya":
        filter_bus_data("Meghalaya", lists_ml)
