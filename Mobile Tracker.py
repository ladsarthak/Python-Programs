import phonenumbers
from phonenumbers import geocoder, carrier, timezone, phonenumberutil
import geocoder as geo
import time

def get_number_type_name(number_type):
    type_map = {
        phonenumberutil.PhoneNumberType.FIXED_LINE: "Fixed Line",
        phonenumberutil.PhoneNumberType.MOBILE: "Mobile",
        phonenumberutil.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
        phonenumberutil.PhoneNumberType.TOLL_FREE: "Toll Free",
        phonenumberutil.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        phonenumberutil.PhoneNumberType.SHARED_COST: "Shared Cost",
        phonenumberutil.PhoneNumberType.VOIP: "VoIP",
        phonenumberutil.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        phonenumberutil.PhoneNumberType.PAGER: "Pager",
        phonenumberutil.PhoneNumberType.UAN: "UAN",
        phonenumberutil.PhoneNumberType.VOICEMAIL: "Voicemail",
        phonenumberutil.PhoneNumberType.UNKNOWN: "Unknown"
    }
    return type_map.get(number_type, "Unknown")

while True:
    mobile_number = input("Enter a mobile number (with country code, e.g., +1234567890) or type exit: ")
    if mobile_number.strip().lower() == "exit":
        print("Exiting...")
        time.sleep(1)
        break

    try:
        parsed_number = phonenumbers.parse(mobile_number)

        if not phonenumbers.is_valid_number(parsed_number):
            print("Invalid phone number.")
            time.sleep(1)
            continue

        # Get additional info
        country_code = parsed_number.country_code
        national_number = parsed_number.national_number
        number_type = phonenumbers.number_type(parsed_number)
        carrier_name = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        formatted_e164 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        formatted_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        formatted_international = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        location = geocoder.description_for_number(parsed_number, "en")
        if not location:
            print("Location not found for this number.")
            time.sleep(1)
            continue

        print(f"Country Code: +{country_code}")
        print(f"National Number: {national_number}")
        print(f"Number Type: {get_number_type_name(number_type)}")
        print(f"Is Valid: {True}")
        print(f"Is Possible: {is_possible}")
        print(f"Formatted (E.164): {formatted_e164}")
        print(f"Formatted (National): {formatted_national}")
        print(f"Formatted (International): {formatted_international}")
        print(f"Approximate location: {location}")
        if carrier_name:
            print(f"Carrier: {carrier_name}")
        if time_zones:
            print(f"Time zones: {', '.join(time_zones)}")

        g = geo.arcgis(location)
        if not g.ok:
            try:
                g = geo.google(location)
            except Exception:
                g = None
        if g and not g.ok:
            try:
                g = geo.bing(location)
            except Exception:
                g = None

        if not g or not g.ok:
            print("Could not geocode the location with available providers.")
            time.sleep(1)
            continue

        print(f"Latitude: {g.lat:.43f}")
        print(f"Longitude: {g.lng:.43f}")
        time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)