import numpy as np
from scipy.optimize import curve_fit
import streamlit as st
import matplotlib.pyplot as plt

def log_func(x, a, b, c=1):
    return a + b * np.log(x + c)  # Ensure x + c > 0 for log calculation


def get_y_val_for_x(x_val, default_values):
    # Iterate through each tuple in the default_values list
    for x, y in default_values:
        # Check if the current x matches x_val
        if x == x_val:
            # If a match is found, return the corresponding y value
            return y
    # If no match is found, indicate that x_val does not match any default value
    return False

def get_upper_value(x_val, default_values):
    # Iterate through each tuple in the default_values list
    for x, y in default_values:
        # Check if the current x is greater than x_val
        if x >= x_val:
            # If a match is found, return the corresponding y value
            return x, y
    # If no match is found, indicate that x_val does not match any default value
    return False


# Streamlit app setup
st.title("Pricing Function by Number of Apps")

# Initialize default values
default_values = [(1, 15000), (20, 75000), (50, 150000), (100, 250000), (1000, 1000000)]
coordinates = []

col1, col2 = st.columns(2)
with col1:
    st.write("Number of AI apps")
with col2:
    st.write("Price (Eur)")

# Creating input fields for x and y with default values
for i, (default_x, default_y) in enumerate(default_values):
    col3, col4 = st.columns(2)
    with col3:
        x = st.number_input(f"X{i}", value=default_x)
    with col4:
        y = st.number_input(f"Y{i}", value=default_y)
    coordinates.append((x, y))

x_data, y_data = zip(*coordinates)

# Curve fitting
params, _ = curve_fit(log_func, x_data, y_data)

# Slider for selecting # of apps
min_x, max_x = 1, 10000  # Example range for slider
default_x_val = 100  # Example default starting value for slider

x_val = st.number_input("Select # of apps", min_value=min_x, max_value=max_x, value=default_x_val, step=1)

adjusted_xval, adjusted_yval = get_upper_value(x_val, default_values)


# Compute the interpolated y-value using the selected x_val
y_val = log_func(x_val, *params)
# adjusted_xval, adjusted_yval = get_y_val_for_x(adjusted_xval, default_values)


# Display the selected x_val and corresponding y_val
st.write(f"Estimated Pricing: Eur {y_val:,.0f}")

st.markdown(f"### Adjusted # of apps: **{adjusted_xval}**")
st.markdown(f"### Final Pricing: Eur **{adjusted_yval:,.0f}**")


# Plotting
fig, ax = plt.subplots()
ax.scatter(x_data, y_data, color='red', label='Benchmark Points')
ax.plot(np.linspace(min_x, max_x, 400), log_func(np.linspace(min_x, max_x, 400), *params), label='Pricing function', color='green')
ax.scatter([x_val], [y_val], color='blue', zorder=5, s=100, edgecolor='black', label='Selected Pricing Point')

for x in x_data:
    ax.axvline(x=x, color='grey', linestyle='--', linewidth=1)  # Dashed line for each x coordinate

ax.legend()
ax.grid(True)
ax.set_xlabel('# of Apps')
ax.set_ylabel('Pricing (Eur)')
ax.set_title('Pricing Function by Number of Apps')
st.pyplot(fig)
