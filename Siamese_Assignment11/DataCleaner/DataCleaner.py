




import re
import requests

class GrossPriceFormatter:
    @staticmethod
    def format(data):
	# Formats the gross price column to 2 decimal places
        for row in data:
            try:
                price = float(row.get("Gross Price", 0))
                row["Gross Price"] = f"{price:.2f}"
            except ValueError:
	# Skip the rows with invalid price values
                continue
        return data


class DuplicateRemover:
    @staticmethod
    def remove(data):
        seen = set()
        unique = []
        for row in data:
	# Normalize keys and values
            row_tuple = tuple(sorted((k.lower(), str(v).strip().lower()) for k, v in row.items()))
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique.append(row)
        print(f"Removed {len(data) - len(unique)} duplicate rows")
        return unique


class AnomalyDetector:
    @staticmethod
    def separate_pepsi(data):
	# Filters out rows where Fuel Type is Pepsi
        valid = []
        anomalies = []
        for row in data:
            if row.get("Fuel Type", "").strip().lower() == "pepsi":
                anomalies.append(row)
            else:
                valid.append(row)
        return valid, anomalies


class ZipCodeFiller:
    def __init__(self, api_key):
        self.api_key = api_key
        self.lookup_count = 0
        self.lookup_limit = 5 # Only lookup the first 5 rows with a missing zip code

    def fill_missing_zips(self, data):
        print("Starting ZIP code filling...")

        # Collect only rows that are missing ZIPs
        missing_rows = [row for row in data if not self._has_zip(row.get("Full Address", ""))]
        print(f"Found {len(missing_rows)} addresses missing ZIP codes")

        # Only update the first 5 of these rows
        for row in missing_rows[:self.lookup_limit]:
            address = row.get("Full Address", "")
            print(f"Trying to extract city/state from: {address}")
            city, state = self.extract_city_state(address)
            print(f"Extracted: city='{city}', state='{state}'")

            if city and state:
                zip_code = self.lookup_zip(city, state)
                if zip_code:
                    row["Full Address"] = address.strip() + f" {zip_code}"
                    print(f"Filled ZIP for {city}, {state} → {zip_code}")
                    self.lookup_count += 1

        if self.lookup_count == 0:
            print("No ZIP codes filled — check address parsing or API issues.") # Shows error(s) in our API key

        return data


    def _has_zip(self, address):
	# Check if the address already has a zip code
        return bool(re.search(r'\\b\\d{5}\\b$', str(address).strip()))

    def extract_city_state(self, address):
	# Parse city and state
        parts = [p.strip() for p in address.split(',') if p.strip()]
        if len(parts) >= 2:
            return parts[-2], parts[-1][:2]  # Simple guess: City, State
        return None, None

    def lookup_zip(self, city, state):
	# Call the external API to get a zip code for the given city/state of purchase
        import requests

        url = "https://app.zipcodebase.com/api/v1/code/city" # The API we chose to hook in
        params = {
            "apikey": self.api_key,
            "city": city,
            "state": state,
            "country": "US"
        }

        try:
            print(f"🔗 Requesting ZIP for: {city}, {state}")
            response = requests.get(url, params=params)


            if response.status_code == 200:
                data = response.json()
                zip_list = data.get("results", [])
                if zip_list and len(zip_list) > 0:
                    zip_code = zip_list[0]  # Use the first returned zip code from list
                    print(f"Selected ZIP code: {zip_code}")
                    return zip_code

                else:
                    print("No ZIP codes found in response")
            else:
                print(f"API Error {response.status_code}: {response.text}") # Shows if there’s an error with our API
        except Exception as e:
            print(f"Exception during API call: {e}")

        return None



