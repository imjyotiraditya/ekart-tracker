import requests
import datetime
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
API_URL = "https://ekartlogistics.com/ws/getTrackingDetails"

# Text formatting constants
UBOLD = "\033[4;1m"
RESET = "\033[0m"


def get_shipment_details(tracking_id):
    """Fetch shipment details from the API."""
    payload = {"trackingId": tracking_id}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Will raise an exception for HTTP error codes
        return response.json()
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    return None


def format_timestamp(ts):
    """Convert epoch timestamp to human-readable format."""
    return (
        datetime.datetime.fromtimestamp(ts / 1000.0).strftime("%Y-%m-%d %I:%M:%S %p")
        if ts
        else "N/A"
    )


def display_details(tracking_id):
    """Display shipment details."""
    details = get_shipment_details(tracking_id)
    if not details:
        print("Failed to retrieve data. Please check the tracking ID and try again.")
        return

    print(f"\n{UBOLD}Shipment Overview for {tracking_id}:{RESET}")
    print(f"  Type: {details.get('shipmentType', 'N/A')}")
    print(
        f"  Expected Delivery: {format_timestamp(details.get('expectedDeliveryDate'))}"
    )
    print(
        f"  Route: From {details.get('sourceCity', 'N/A').title()} to {details.get('destinationCity', 'N/A').title()}"
    )
    print(f"  Receiver: {details.get('receiverName', 'N/A')}")

    print(f"\n{UBOLD}Tracking Progress:{RESET}")
    max_city_len = max(
        (
            len(event.get("city", "N/A"))
            for event in details.get("shipmentTrackingDetails", [])
        ),
        default=3,
    )
    for event in details.get("shipmentTrackingDetails", []):
        date = format_timestamp(event.get("date"))
        city = (
            event.get("city", "N/A").strip().title()
            if event.get("city", None)
            else "N/A"
        )
        status = event.get("statusDetails", "N/A").strip()
        print(f"  - {date:20} | {city:{max_city_len}} | {status}")


def main():
    """Main function to drive the script execution."""
    try:
        while True:
            tracking_id = input("\nEnter Tracking ID or type 'exit' to quit: ")
            if tracking_id.lower() == "exit":
                print("\nThank you for using our tracker. Goodbye!")
                break
            if not tracking_id.strip():
                print("Invalid input. Please enter a valid tracking ID.")
                continue
            display_details(tracking_id)
    except KeyboardInterrupt:
        print("\nOperation cancelled. Exiting...")
    finally:
        print("Performing cleanup operations...")


if __name__ == "__main__":
    main()
