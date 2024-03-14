import numpy as np
from scipy.optimize import curve_fit
import streamlit as st
import matplotlib.pyplot as plt


def log_func(x, a, b, c=1):
    return a + b * np.log(x + c)  # Adding a small constant to ensure x + c > 0


# Streamlit app setup
st.title("Pricing function by number of apps")

# Initialize default values
default_values = [(1, 15000, 1), (20, 75000, 1),
                  (50, 150000, 1), (100, 250000, 1), (1000, 1000000, 1)]
coordinates = []
steps = []

# Creating input fields for x, y, and step with default values
for i, (default_x, default_y, default_step) in enumerate(default_values):
    col1, col2, col3 = st.columns(3)
    with col1:
        x = st.number_input(f"X{i}", value=default_x)
    with col2:
        y = st.number_input(f"Y{i}", value=default_y)
    with col3:
        if i < 4:
            step = st.number_input(
                f"Step Size for X{i}", value=default_step, min_value=1)
    coordinates.append((x, y))
    steps.append((x, step))

x_data, y_data = zip(*coordinates)

# Curve fitting
params, _ = curve_fit(log_func, x_data, y_data)

# Corrected function to find the step size based on the current x_val


def find_step_size(x_val, steps):
    current_step = 1  # Default step if x_val is less than any defined intervals
    for interval, step in sorted(steps, key=lambda x: x[0]):
        if x_val >= interval:
            current_step = step
    return current_step


# Slider for selecting # of apps
min_x, max_x = min(x_data), max(x_data)

# Assuming min_x, max_x, and a default value for x_val have been defined
min_x, max_x = 1, 10000  # Example range
default_x_val = 500  # Example default starting value

# Create buttons for decrementing/incrementing
col1, col2, col3 = st.columns([1, 1, 10])
with col1:
    decrement = st.button('--')
with col2:
    increment = st.button('++')

# Session state to store and update the current value
if 'x_val' not in st.session_state:
    st.session_state.x_val = default_x_val

# Adjust the value based on button presses
if decrement:
    st.session_state.x_val = max(min_x, st.session_state.x_val - 1)
if increment:
    st.session_state.x_val = min(max_x, st.session_state.x_val + 1)

# Display the slider
x_val = st.slider("Select # of apps", min_value=min_x, max_value=max_x,
                  value=st.session_state.x_val, step=1, key='slider')

# Ensure the slider updates the session state (to stay in sync if manually adjusted)
st.session_state.x_val = x_val



# Find the step size for the current x_val
current_step = find_step_size(x_val, steps)

# Adjust x_val to align with the nearest higher multiple of the current step size

adjusted_x_val = x_val + (current_step - x_val % current_step) % current_step

# Compute the interpolated y-value
if x_val == 1:
    y_val = y_data[0]
else:
    y_val = log_func(adjusted_x_val, *params)

# Display the adjusted x_val and corresponding y_val
st.write(f"Adjusted # of apps: {adjusted_x_val}")
st.write(f"Pricing: Eur {y_val:,.0f}")

# Plotting
fig, ax = plt.subplots()
ax.scatter(x_data, y_data, color='red', label='Benchmark Points')
ax.plot(np.linspace(min_x, max_x, 400), log_func(np.linspace(
    min_x, max_x, 400), *params), label='Pricing function', color='green')
ax.scatter([adjusted_x_val], [y_val], color='blue', zorder=5,
           s=100, edgecolor='black', label='Pricing Point = f(# apps)')

# Add dashed lines for each x coordinate
for x in x_data:
    # Dashed line for each x coordinate
    ax.axvline(x=x, color='grey', linestyle='--', linewidth=1)

ax.annotate(f"({adjusted_x_val}, {int(y_val)})", (adjusted_x_val, y_val), textcoords="offset points", xytext=(
    10, -15), ha='center', arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
ax.legend()
ax.grid(True)
ax.set_xlabel('# of Apps')
ax.set_ylabel('Pricing (Eur)')
ax.set_title('Pricing Function by Number of Apps')
st.pyplot(fig)
