import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

@st.cache_data
def setup(): 
    #file_paths = ['table1.csv', 'table2.csv', 'table3.csv', 'table4.csv', 'table5.csv', 'table6.csv', 'table7.csv']
    file_paths = ['table1.zip', 'table2.zip', 'table3.zip', 'table4.zip', 'table5.zip', 'table6.zip', 'table7.zip']
    # Function to process each chunk
    #def process_chunk(chunk):
    #    # Your processing logic goes here
    #    return chunk

    # Read and process each file in chunks
    dfs = []  # List to store DataFrame chunks
    for file_path in file_paths:
        chunks = pd.read_csv(file_path, chunksize=1000)  # Adjust chunksize as needed
        for chunk in chunks:
    #        processed_chunk = process_chunk(chunk)
            dfs.append(chunk)

    # Concatenate all processed chunks into a single DataFrame
    bus_data = pd.concat(dfs, ignore_index=True)


    bus_data['OPD_DATE'] = pd.to_datetime(bus_data['OPD_DATE']).dt.date
    bus_data['STOP_ARR_ACT'] = pd.to_datetime(bus_data['STOP_ARR_ACT']).dt.time
    bus_data['STOP_DEP_ACT'] = pd.to_datetime(bus_data['STOP_DEP_ACT']).dt.time
    bus_data['STOP_DEP_SCHED'] = pd.to_datetime(bus_data['STOP_DEP_SCHED'], errors='coerce')
    
    bus_data.dropna()
    
    bus_data['STOP_DEP_SCHED'] = bus_data['STOP_DEP_SCHED'].dt.time
    return bus_data

bus_data = setup()

#print(type(bus_data.iloc[0]['STOP_DEP_ACT']), "\n", type(bus_data.iloc[0]['STOP_DEP_SCHED']) )
#bus_data['DELAY'] = bus_data['STOP_DEP_ACT'] - bus_data['STOP_DEP_SCHED'].dt.time




# Function to add markers for a specific date
def add_markers_for_date(m, data, selected_date, direction):
    filtered_data = data[(data['OPD_DATE'] == selected_date) & (data['DIRECTION'] == direction)]
    for _, row in filtered_data.iterrows():
        #delay = row['STOP_DEP_ACT'] - row['STOP_DEP_SCHED']

        popup1 = folium.Popup(f"Stop: {row['LONG_NAME']} <br> Direction: {row['DIRECTION']} <br> Arrival Time: {row['STOP_ARR_ACT']} <br> Departure Time: {row['STOP_DEP_ACT']} <br> Onboardings: {row['PSNGR_IN']} <br> Offboardings: {row['PSNGR_OUT']} <br> Load: {row['PSNGR_LOAD']}", min_width=200, max_width=500)
        folium.Marker([row['GPS_LATITUDE'], row['GPS_LONGITUDE']],  popup=popup1, icon=folium.Icon(color='blue')).add_to(m)



# Create a Streamlit app
st.title('Bus Data Visualization')

## Iterate over each file path and display its data on a separate page
#for file_path in file_paths:
#    # Load the data
#    bus_d = pd.read_csv(file_path)
#    
#    # Display the bus data table
#    st.write(f'## Bus Data - {file_path}')
#    st.write(bus_d)


st.write('## Map Visualization')

selected_date = st.date_input("Select Date", value=None, min_value=min(bus_data['OPD_DATE']), max_value=max(bus_data['OPD_DATE']))
direction = st.selectbox("Direction", ['East', 'West'])


# Get center of the map
center_lat = bus_data['GPS_LATITUDE'].mean()
center_lon = bus_data['GPS_LONGITUDE'].mean()



# Load markers for the selected date
if st.button('Load Bus Data'):
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)  # Clear the map
    st.write(bus_data[bus_data['OPD_DATE'] == selected_date])
    add_markers_for_date(m, bus_data, selected_date, direction)
    folium_static(m)





# Create a folium map centered at the mean latitude and longitude
#m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
#folium_static(m)

# Add markers for each bus stop
#for i, row in bus_data.iterrows():
#    folium.Marker([row['GPS_LATITUDE'], row['GPS_LONGITUDE']],
#                  popup=f"Stop: {row['LONG_NAME']}Arrival Time: {row['STOP_ARR_ACT']} \n Departure Time: {row['STOP_DEP_ACT']} \n Onboardings: {row['PSNGR_IN']} \n Offboardings: {row['PSNGR_OUT']}",
#                  icon=folium.Icon(color='blue')).add_to(m)

# Display the map
#folium_static(m)





























