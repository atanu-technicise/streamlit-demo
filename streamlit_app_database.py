import streamlit as st



st.title('Streamlit Demo for connecting postgresql Database')


# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM hfj_resource;', ttl="10m")

# Print results.
for row in df.itertuples():
    st.write(f"{row.res_type} has resource type id :{row.res_type_id}")