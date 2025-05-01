import streamlit as st
from datetime import datetime
import pytz
import json
import time  # For potential delays or loading indicators
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)

RATE_DICT = dict()


# --- Function to get live rates ---
@st.cache_data(ttl=60)  # Optional: Cache for 60 seconds to avoid rapid re-fetching
def get_rates():
    """
    Get the live rates of Au and Ag from vickygold.in, handling dynamic content.
    Uses Selenium for fetching the rates.
    """
    # Use the Selenium approach to get rates
    return get_rates_with_selenium()


# Function to get rates with Selenium
def get_rates_with_selenium():
    """
    Selenium-based approach to get rates.
    """
    driver = None  # Initialize driver to None for the finally block
    try:
        # Setup chrome options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")  # Often necessary in headless mode
        options.add_argument(
            "--window-size=1920x1080"
        )  # Can sometimes help with element finding

        # Setup the driver
        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

        # Get the dynamic content from the website
        driver.get("https://vickygold.in/Liverate.html")

        # Wait for the dynamic content to load
        driver.implicitly_wait(10)  # Implicit wait for elements to appear initially

        # Get the current time in IST
        ist = pytz.timezone("Asia/Kolkata")
        ist_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S %Z")

        rates = {"timestamp": ist_time}

        # Unified approach to extract both gold and silver rates at once
        # Wait for the elements to be properly loaded
        time.sleep(3)

        try:
            # Use a single approach to extract all rates at once using global XPaths
            # This avoids refreshing the page between gold and silver extraction

            # Get all rate elements at once
            all_symbols = driver.find_elements(By.XPATH, "//span[@id='GoldSymbol']")
            all_rates = driver.find_elements(By.XPATH, "//span[@id='GoldSell']")

            # Process all rates
            for i in range(min(len(all_symbols), len(all_rates))):
                try:
                    symbol_text = all_symbols[i].text.strip()
                    rate_text = all_rates[i].text.strip()

                    # Skip empty entries
                    if not symbol_text or not rate_text:
                        continue

                    # Add prefix if we can determine if it's gold or silver based on parent container
                    parent_element = all_symbols[i].find_element(
                        By.XPATH, "../../../.."
                    )
                    parent_id = parent_element.get_attribute("id")

                    # Add appropriate prefix for clarity if not already present
                    if parent_id == "silverproduct" and "Silver" not in symbol_text:
                        prefix = "Silver "
                    elif parent_id == "divProduct" and "Gold" not in symbol_text:
                        prefix = "Gold "
                    else:
                        prefix = ""

                    final_symbol = f"{prefix}{symbol_text}"
                    rates[final_symbol] = rate_text

                except Exception as e:
                    print(f"Error extracting rate for item {i}: {e}")
                    continue

        except Exception as e:
            print(f"Error extracting rates: {e}")
            # Continue to fallback methods

        # Check if any rates were found besides the timestamp
        if len(rates) <= 1:
            # Last resort - direct extraction by ID
            print(
                "No rates found with container approach. Trying direct ID extraction..."
            )

            try:
                # Find all elements with ID="GoldSymbol"
                all_symbol_elements = driver.find_elements(
                    By.XPATH, "//*[@id='GoldSymbol']"
                )
                all_rate_elements = driver.find_elements(
                    By.XPATH, "//*[@id='GoldSell']"
                )

                if len(all_symbol_elements) > 0 and len(all_rate_elements) > 0:
                    for i in range(
                        min(len(all_symbol_elements), len(all_rate_elements))
                    ):
                        symbol_text = all_symbol_elements[i].text.strip()
                        rate_text = all_rate_elements[i].text.strip()

                        if symbol_text and rate_text:
                            rates[symbol_text] = rate_text
            except Exception as e:
                print(f"Error in direct extraction: {e}")

            # If still no rates, try parsing the page source using regex
            if len(rates) <= 1:
                try:
                    html_content = driver.page_source
                    # Look for rates using regex pattern matching
                    import re

                    # Simple pattern to find GoldSymbol and GoldSell pairs in HTML
                    pattern = r'id="GoldSymbol"[^>]*>([^<]+)</span>.*?id="GoldSell"[^>]*>([^<]+)</span>'
                    matches = re.findall(pattern, html_content, re.DOTALL)

                    for symbol, rate in matches:
                        if symbol.strip() and rate.strip():
                            rates[symbol.strip()] = rate.strip()

                except Exception as e:
                    print(f"Error during HTML content extraction: {e}")

        # Return the collected rates
        return rates

    except Exception as e:
        error_message = f"An error occurred during scraping: {e}"
        print(error_message)  # Log the error for debugging
        return {"error": error_message}

    finally:
        # Ensure driver is quit even if an error occurs
        if driver:
            try:
                driver.quit()
            except Exception as quit_e:
                print(f"Error quitting WebDriver: {quit_e}")


# Main Streamlit App
st.set_page_config(
    page_title="Gold Calculator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling with dark mode support
st.markdown(
    """
<style>    /* Common styles */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFD700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
      /* Common styles that work with Streamlit's theme */
    .subtitle {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-align: center;
    }    .rate-value {
        font-size: 2rem !important;
        font-weight: 800 !important;
        margin-bottom: 0;
    }
    .rate-label {
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .timestamp-text {
        font-weight: 500;
    }

    /* Add top margin to Streamlit button wrapper */
    div.stButton {
        margin-top: 10px !important;
    }    /* Gold rate styling */
    .gold-rate {
        padding: 10px;
        border: 3px solid var(--gold-border-color);
        border-radius: 8px;
    }
    
    /* Silver rate styling */
    .silver-rate {
        padding: 10px;
        border: 3px solid var(--silver-border-color);
        border-radius: 8px;
    }
    
    /* 916 Gold rate styling */
    .gold-916-rate {
        padding: 10px;
        border: 3px solid #FF0000;
        border-radius: 8px;
        background-color: rgba(255, 0, 0, 0.05);
    }
    
    .gold-916-value {
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        margin-bottom: 0;
    }

    /* Custom variables for borders */
    :root {
        --gold-border-color: #FFD700;
        --silver-border-color: #C0C0C0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header section
st.markdown('<h1 class="main-title">Gold Calculator ✨</h1>', unsafe_allow_html=True)
st.markdown("Your one-stop solution for all your gold purchasing or selling needs")

# --- Live Rates Section ---
st.header("Live Gold & Silver Rates")
st.caption("Source: vickygold.in")

# Initialize session state
if "live_rates" not in st.session_state:
    st.session_state["live_rates"] = None
if "last_fetch_error" not in st.session_state:
    st.session_state["last_fetch_error"] = None

# Create a clean container for the rates display
rates_container = st.container()

# Consistent spacing before Live Rates button
st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

# Create a more compact fetch button layout
col_btn, col_status = st.columns([1, 3])

with col_btn:
    # minimal spacer to slightly nudge button
    st.write("")
    if st.button("📊 Live Rates", use_container_width=True):
        with st.spinner("Fetching live rates...", show_time=True):
            rates_data = get_rates()

            # Check if there was an error fetching the rates
            if "error" in rates_data:
                st.session_state["live_rates"] = None
                st.session_state["last_fetch_error"] = rates_data["error"]
                with col_status:
                    st.error(
                        f"Failed to fetch rates: {st.session_state['last_fetch_error']}"
                    )
            else:
                st.session_state["live_rates"] = rates_data
                st.session_state["last_fetch_error"] = None

                # Reset the user_modified_gold_rate flag when fetching new rates
                # This allows the new rates to be applied to all pages
                if "user_modified_gold_rate" in st.session_state:
                    del st.session_state["user_modified_gold_rate"]

                if "Gold 995 100gms Ready" in rates_data:
                    try:
                        # Extract and clean the rate value
                        rate_str = rates_data["Gold 995 100gms Ready"]
                        # Remove non-numeric characters except decimal point
                        clean_rate = "".join(
                            c for c in rate_str if c.isdigit() or c == "."
                        )
                        rate_value = float(clean_rate)

                        # Store the per gram rate (100gms rate divided by 100)
                        st.session_state["current_gold_rate_per_gram"] = (
                            rate_value / 10
                        )  # Calculate 916 (22k) gold rate
                        # Formula: (Gold 995 rate / 24 * 22) + 500, then ceiling to the next 500
                        rate_916 = (rate_value / 24 * 22) + 500
                        # Ceiling to the next 500
                        import math

                        rate_916 = (
                            math.ceil(rate_916 / 500) * 500
                        )  # Store the 916 gold rate for display and use in calculator pages
                        st.session_state["gold_rate_916"] = rate_916

                        # Reset the user_modified_gold_rate flag when fetching new rates
                        if "user_modified_gold_rate" in st.session_state:
                            del st.session_state["user_modified_gold_rate"]

                        # Update the gold_rate in session state for all calculator pages
                        if "is_22k" in st.session_state and st.session_state.is_22k:
                            st.session_state.gold_rate = float(
                                rate_916 / 10
                            )  # Convert to per gram
                        else:
                            # For 24k, use the direct rate
                            st.session_state.gold_rate = float(
                                st.session_state["current_gold_rate_per_gram"]
                            )

                        # Update the gold_rate session state variable for pages
                        # Only set the per-gram rate if user hasn't manually set it
                        if "is_22k" in st.session_state and st.session_state["is_22k"]:
                            st.session_state.gold_rate = float(
                                rate_916 / 10
                            )  # Convert to per gram
                        else:
                            # For 24k, use the direct rate
                            st.session_state.gold_rate = float(
                                st.session_state["current_gold_rate_per_gram"]
                            )
                    except (ValueError, KeyError) as e:
                        print(f"Error extracting gold rate for calculator: {e}")

# Add extra spacing after the Live Rates button
st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

# Display timestamp as caption right below the Live Rates button
if st.session_state["live_rates"] and "timestamp" in st.session_state["live_rates"]:
    timestamp = st.session_state["live_rates"]["timestamp"]
    st.caption(f"Last updated: {timestamp}")

# Add a success message to let users know rates are synchronized
# This will show whether rates are from fetching or manual entry
if "gold_rate_916" in st.session_state or "gold_rate" in st.session_state:
    st.success("✅ Gold rates are now synchronized across all calculator pages!")

# Display rates in a more aesthetically pleasing card format
with rates_container:
    if st.session_state["last_fetch_error"] and not st.session_state["live_rates"]:
        # Error is already displayed above when the button is clicked
        pass
    elif st.session_state["live_rates"]:
        rates = st.session_state["live_rates"].copy()
        rates.pop("timestamp", None)  # Remove timestamp as we've already displayed it
        num_rates = len(rates)
        if num_rates > 0:
            # Display 916 (22k) gold rate if available
            if "gold_rate_916" in st.session_state:
                st.markdown(
                    f"""
                    <div class="gold-916-rate">
                        <p class="rate-label">Gold 916 (22k) - Today's Rate</p>
                        <p class="gold-916-value">₹{int(st.session_state['gold_rate_916']):,}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Add spacing after 916 gold rate
                st.markdown(
                    "<div style='margin: 20px 0;'></div>", unsafe_allow_html=True
                )

            # Separate gold and silver rates
            gold_rates = [
                (name, rate)
                for name, rate in rates.items()
                if "Gold" in name or "GOLD" in name
            ]
            silver_rates = [
                (name, rate)
                for name, rate in rates.items()
                if "Silver" in name or "SILVER" in name
            ]

            # Display gold rates in the first row (first 2)
            if gold_rates:
                gold_cols = st.columns(
                    min(len(gold_rates), 2)
                )  # Show at most 2 gold rates

                for j, (name, rate) in enumerate(
                    gold_rates[:2]
                ):  # Limit to first 2 gold rates
                    with gold_cols[j]:
                        # Clean rate value for display
                        display_rate = int(rate.split(" ")[-1] if " " in rate else rate)

                        # Format with appropriate gold border styling
                        st.markdown(
                            f"""
                            <div class="gold-rate">
                                <p class="rate-label">{name}</p>
                                <p class="rate-value">₹{display_rate:,}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            # Add spacing between rows
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

            # Display silver rates in the second row (up to 3)
            if silver_rates:
                silver_cols = st.columns(
                    min(len(silver_rates), 3)
                )  # Show at most 3 silver rates

                for j, (name, rate) in enumerate(
                    silver_rates[:3]
                ):  # Limit to first 3 silver rates
                    with silver_cols[j]:
                        # Clean rate value for display
                        display_rate = int(rate.split(" ")[-1] if " " in rate else rate)

                        # Format with silver border styling
                        st.markdown(
                            f"""
                            <div class="silver-rate">
                                <p class="rate-label">{name}</p>
                                <p class="rate-value">₹{display_rate:,}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
        else:
            st.warning("No specific rates (Gold/Silver) were found.")
    elif not st.session_state["last_fetch_error"]:
        st.info(
            "Click the 'Live Rates' button to fetch the latest gold and silver rates."
        )


# --- Rest of the existing Home page content ---
if "mesage_shown" not in st.session_state:
    st.toast(
        "**Please select an option from the sidebar to get started**",
        icon="✨",
    )
    st.toast(
        "**More features coming soon!**",
        icon="✨",
    )
    st.session_state["mesage_shown"] = True

st.markdown("")

st.markdown(
    """
<h3 class="section-title">What can this app do for you?</h3>
""",
    unsafe_allow_html=True,
)

# Create feature cards in a more modern layout
features = [
    {
        "icon": "💰",
        "title": "Transparent Pricing",
        "description": "Understand the complete breakdown of charges and fees for your gold transactions.",
    },
    {
        "icon": "💸",
        "title": "Save Money",
        "description": "Make informed decisions and avoid paying more than you should on your purchases.",
    },
    {
        "icon": "⏱️",
        "title": "Save Time",
        "description": "Eliminate manual calculations and guesswork with our instant calculator tools.",
    },
]

# Display features in a modern card layout
cols = st.columns(3)
for i, feature in enumerate(features):
    with cols[i]:
        st.markdown(
            f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">{feature['icon']}</div>
            <h4 class="feature-title">{feature['title']}</h4>
            <p class="feature-description">{feature['description']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Call-to-action section
st.markdown("")
st.markdown(
    """
<p class="cta-text">
    Start exploring and make your gold purchasing or selling experience smoother and smarter with Gold Calculator!
</p>
<p class="cta-subtext">
    Select an option from the sidebar to get started with your calculations.
</p>
""",
    unsafe_allow_html=True,
)
