"""
SpaceX Falcon 9 First Stage Landing Prediction
Web scraping Falcon 9 and Falcon Heavy Launches Records from Wikipedia

Source: https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches
Snapshot date: 9th June 2021

This script extracts launch data including flight numbers, dates, booster versions,
launch sites, payloads, and landing outcomes from a static Wikipedia page snapshot.
"""

import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def date_time(table_cells) -> List[str]:
    """
    Extract date and time from an HTML table cell.
    
    Args:
        table_cells: BeautifulSoup table cell element
        
    Returns:
        List containing [date, time]
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]


def booster_version(table_cells) -> str:
    """
    Extract booster version from an HTML table cell.
    
    Args:
        table_cells: BeautifulSoup table cell element
        
    Returns:
        Booster version string
    """
    return ''.join(
        [version for i, version in enumerate(table_cells.strings) if i % 2 == 0][0:-1]
    )


def landing_status(table_cells) -> str:
    """
    Extract landing status from an HTML table cell.
    
    Args:
        table_cells: BeautifulSoup table cell element
        
    Returns:
        Landing status string
    """
    try:
        return [i for i in table_cells.strings][0]
    except IndexError:
        return "Unknown"


def get_mass(table_cells) -> str:
    """
    Extract payload mass from an HTML table cell.
    
    Args:
        table_cells: BeautifulSoup table cell element
        
    Returns:
        Payload mass string with 'kg' suffix, or '0' if not found
    """
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        kg_index = mass.find("kg")
        if kg_index != -1:
            return mass[0:kg_index + 2]
    return "0"


def extract_column_from_header(row) -> str:
    """
    Extract and clean column name from a table header element.
    
    Args:
        row: BeautifulSoup table header element
        
    Returns:
        Cleaned column name string, or None if invalid
    """
    # Remove nested tags
    for tag in ['br', 'a', 'sup']:
        if getattr(row, tag, None):
            getattr(row, tag).extract()
    
    column_name = ' '.join(row.contents)
    
    # Filter out digit-only and empty names
    if column_name.strip() and not column_name.strip().isdigit():
        return column_name.strip()
    return None


# ---------------------------------------------------------------------------
# Main scraping functions
# ---------------------------------------------------------------------------

def fetch_wikipedia_page(url: str) -> BeautifulSoup:
    """
    Fetch and parse Wikipedia page.
    
    Args:
        url: Wikipedia page URL
        
    Returns:
        BeautifulSoup object of parsed HTML
        
    Raises:
        requests.RequestException: If page fetch fails
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    
    logger.info(f"Fetching page: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    logger.info(f"Page title: {soup.title.string if soup.title else 'No title'}")
    
    return soup


def extract_column_names(table) -> List[str]:
    """
    Extract column names from table header.
    
    Args:
        table: BeautifulSoup table element
        
    Returns:
        List of column names
    """
    column_names = []
    th_elements = table.find_all("th")
    
    for th in th_elements:
        name = extract_column_from_header(th)
        if name:
            column_names.append(name)
    
    logger.info(f"Extracted {len(column_names)} columns: {column_names}")
    return column_names


def initialize_launch_dict(column_names: List[str]) -> Dict[str, List]:
    """
    Initialize dictionary for storing launch data.
    
    Args:
        column_names: List of column names from table
        
    Returns:
        Dictionary with all required keys initialized to empty lists
    """
    launch_dict = {col: [] for col in column_names}
    
    # Remove irrelevant column if it exists
    launch_dict.pop('Date and time ( )', None)
    
    # Ensure all required columns exist
    required_columns = [
        'Flight No.', 'Launch site', 'Payload', 'Payload mass',
        'Orbit', 'Customer', 'Launch outcome', 'Version Booster',
        'Booster landing', 'Date', 'Time'
    ]
    
    for col in required_columns:
        if col not in launch_dict:
            launch_dict[col] = []
    
    return launch_dict


def parse_launch_tables(soup: BeautifulSoup, launch_dict: Dict[str, List]) -> int:
    """
    Parse all launch tables and populate launch dictionary.
    
    Args:
        soup: BeautifulSoup object of the page
        launch_dict: Dictionary to populate with launch data
        
    Returns:
        Number of rows extracted
    """
    extracted_row = 0
    
    # Find all launch tables
    tables = soup.find_all('table', "wikitable plainrowheaders collapsible")
    logger.info(f"Found {len(tables)} launch tables to process")
    
    for table_number, table in enumerate(tables):
        for rows in table.find_all("tr"):
            # Check if the first heading is a flight number
            flight_number = None
            if rows.th and rows.th.string:
                flight_number = rows.th.string.strip()
                is_valid_flight = flight_number.isdigit()
            else:
                is_valid_flight = False
            
            if not is_valid_flight:
                continue
            
            row = rows.find_all('td')
            if len(row) < 9:  # Ensure row has enough columns
                logger.warning(f"Skipping incomplete row for flight {flight_number}")
                continue
            
            try:
                extracted_row += 1
                
                # Flight Number
                launch_dict['Flight No.'].append(flight_number)
                
                # Date and Time
                datatimelist = date_time(row[0])
                date = datatimelist[0].strip(',') if datatimelist else ""
                time = datatimelist[1] if len(datatimelist) > 1 else ""
                launch_dict['Date'].append(date)
                launch_dict['Time'].append(time)
                
                # Booster version
                bv = booster_version(row[1])
                if not bv and row[1].a:
                    bv = row[1].a.string
                launch_dict['Version Booster'].append(bv if bv else "Unknown")
                
                # Launch Site
                launch_site = row[2].a.string if row[2].a else row[2].get_text(strip=True)
                launch_dict['Launch site'].append(launch_site)
                
                # Payload
                payload = row[3].a.string if row[3].a else row[3].get_text(strip=True)
                launch_dict['Payload'].append(payload)
                
                # Payload Mass
                payload_mass = get_mass(row[4])
                launch_dict['Payload mass'].append(payload_mass)
                
                # Orbit
                orbit = row[5].a.string if row[5].a else row[5].get_text(strip=True)
                launch_dict['Orbit'].append(orbit)
                
                # Customer
                customer = row[6].get_text(" ", strip=True)
                launch_dict['Customer'].append(customer)
                
                # Launch outcome
                launch_outcome = list(row[7].strings)[0] if row[7].strings else "Unknown"
                launch_dict['Launch outcome'].append(launch_outcome)
                
                # Booster landing
                booster_landing = landing_status(row[8])
                launch_dict['Booster landing'].append(booster_landing)
                
            except Exception as e:
                logger.error(f"Error processing flight {flight_number}: {e}")
                # Remove the partially added data for this row
                for key in launch_dict:
                    if len(launch_dict[key]) == extracted_row:
                        launch_dict[key].pop()
                extracted_row -= 1
    
    return extracted_row


def create_dataframe(launch_dict: Dict[str, List]) -> pd.DataFrame:
    """
    Create pandas DataFrame from launch dictionary.
    
    Args:
        launch_dict: Dictionary containing launch data
        
    Returns:
        pandas DataFrame
    """
    df = pd.DataFrame(launch_dict)
    logger.info(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
    return df


def save_to_csv(df: pd.DataFrame, output_file: str) -> None:
    """
    Save DataFrame to CSV file.
    
    Args:
        df: pandas DataFrame to save
        output_file: Output file path
    """
    df.to_csv(output_file, index=False)
    logger.info(f"Data saved to: {output_file}")


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def main():
    """Main execution function."""
    # Wikipedia snapshot URL
    static_url = (
        "https://en.wikipedia.org/w/index.php"
        "?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
    )
    
    try:
        # Fetch and parse the page
        soup = fetch_wikipedia_page(static_url)
        
        # Find all tables
        html_tables = soup.find_all("table")
        if len(html_tables) < 3:
            raise ValueError("Expected at least 3 tables on the page")
        
        # The third table (index 2) is the first launch records table
        first_launch_table = html_tables[2]
        
        # Extract column names
        column_names = extract_column_names(first_launch_table)
        
        # Initialize launch dictionary
        launch_dict = initialize_launch_dict(column_names)
        
        # Parse all launch tables
        extracted_rows = parse_launch_tables(soup, launch_dict)
        logger.info(f"Successfully extracted {extracted_rows} launch records")
        
        # Create DataFrame
        df = create_dataframe(launch_dict)
        
        # Display summary
        print("\n" + "="*80)
        print("SPACEX LAUNCH DATA EXTRACTION SUMMARY")
        print("="*80)
        print(f"\nTotal records extracted: {len(df)}")
        print(f"Columns: {', '.join(df.columns)}")
        print("\nFirst 5 records:")
        print(df.head().to_string())
        print("\nData types:")
        print(df.dtypes)
        print("\nMissing values:")
        print(df.isnull().sum())
        
        # Save to CSV
        output_file = "spacex_launches.csv"
        save_to_csv(df, output_file)
        
        print(f"\n{'='*80}")
        print(f"✓ Data successfully saved to: {output_file}")
        print(f"{'='*80}\n")
        
        return df
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    df = main()
