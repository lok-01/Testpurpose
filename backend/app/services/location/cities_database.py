"""
Comprehensive Built-in Astronomical City Database for India & Worldwide
Guarantees 100% offline reliability with exact Latitude, Longitude,
historical IANA timezones, and standard UTC offsets.
"""

from typing import List, Dict, Any

CITIES_DATA: List[Dict[str, Any]] = [
    # Sacred & Classical Vedic Astrology Centers
    {"city": "Varanasi", "state": "Uttar Pradesh", "country": "India", "latitude": 25.3176, "longitude": 82.9739, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Benares", "Kashi"]},
    {"city": "Ujjain", "state": "Madhya Pradesh", "country": "India", "latitude": 23.1765, "longitude": 75.7885, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Avanti", "Avantika"]},
    {"city": "Ayodhya", "state": "Uttar Pradesh", "country": "India", "latitude": 26.7922, "longitude": 82.1998, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Saket"]},
    {"city": "Haridwar", "state": "Uttarakhand", "country": "India", "latitude": 29.9457, "longitude": 78.1642, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Hardwar", "Mayapuri"]},
    {"city": "Rishikesh", "state": "Uttarakhand", "country": "India", "latitude": 30.0869, "longitude": 78.2676, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Prayagraj", "state": "Uttar Pradesh", "country": "India", "latitude": 25.4358, "longitude": 81.8463, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Allahabad", "Prayag", "Triveni"]},
    {"city": "Mathura", "state": "Uttar Pradesh", "country": "India", "latitude": 27.4924, "longitude": 77.6737, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Braj"]},
    {"city": "Vrindavan", "state": "Uttar Pradesh", "country": "India", "latitude": 27.5806, "longitude": 77.7006, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Brindavan"]},
    {"city": "Puri", "state": "Odisha", "country": "India", "latitude": 19.8135, "longitude": 85.8312, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Jagannath Puri"]},
    {"city": "Dwarka", "state": "Gujarat", "country": "India", "latitude": 22.2442, "longitude": 68.9685, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Dwaraka"]},
    {"city": "Rameswaram", "state": "Tamil Nadu", "country": "India", "latitude": 9.2876, "longitude": 79.3129, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Rameshwaram"]},
    {"city": "Tirupati", "state": "Andhra Pradesh", "country": "India", "latitude": 13.6288, "longitude": 79.4192, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Tirumala"]},
    {"city": "Madurai", "state": "Tamil Nadu", "country": "India", "latitude": 9.9252, "longitude": 78.1198, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Kanchipuram", "state": "Tamil Nadu", "country": "India", "latitude": 12.8342, "longitude": 79.7036, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Conjeevaram"]},
    {"city": "Gaya", "state": "Bihar", "country": "India", "latitude": 24.7914, "longitude": 85.0002, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Bodh Gaya"]},
    {"city": "Somnath", "state": "Gujarat", "country": "India", "latitude": 20.8880, "longitude": 70.4012, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Prabhas Patan"]},
    {"city": "Shirdi", "state": "Maharashtra", "country": "India", "latitude": 19.7667, "longitude": 74.4764, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},

    # Major Indian Metros and Capitals
    {"city": "New Delhi", "state": "Delhi", "country": "India", "latitude": 28.6139, "longitude": 77.2090, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Delhi", "NCR"]},
    {"city": "Mumbai", "state": "Maharashtra", "country": "India", "latitude": 19.0760, "longitude": 72.8777, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Bombay"]},
    {"city": "Kolkata", "state": "West Bengal", "country": "India", "latitude": 22.5726, "longitude": 88.3639, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Calcutta"]},
    {"city": "Chennai", "state": "Tamil Nadu", "country": "India", "latitude": 13.0827, "longitude": 80.2707, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Madras"]},
    {"city": "Bengaluru", "state": "Karnataka", "country": "India", "latitude": 12.9716, "longitude": 77.5946, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Bangalore"]},
    {"city": "Hyderabad", "state": "Telangana", "country": "India", "latitude": 17.3850, "longitude": 78.4867, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Secunderabad"]},
    {"city": "Ahmedabad", "state": "Gujarat", "country": "India", "latitude": 23.0225, "longitude": 72.5714, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Amdavad"]},
    {"city": "Pune", "state": "Maharashtra", "country": "India", "latitude": 18.5204, "longitude": 73.8567, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Poona"]},
    {"city": "Jaipur", "state": "Rajasthan", "country": "India", "latitude": 26.9124, "longitude": 75.7873, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Pink City"]},
    {"city": "Lucknow", "state": "Uttar Pradesh", "country": "India", "latitude": 26.8467, "longitude": 80.9462, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Kanpur", "state": "Uttar Pradesh", "country": "India", "latitude": 26.4499, "longitude": 80.3319, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Cawnpore"]},
    {"city": "Nagpur", "state": "Maharashtra", "country": "India", "latitude": 21.1458, "longitude": 79.0882, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Indore", "state": "Madhya Pradesh", "country": "India", "latitude": 22.7196, "longitude": 75.8577, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Thane", "state": "Maharashtra", "country": "India", "latitude": 19.2183, "longitude": 72.9781, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Bhopal", "state": "Madhya Pradesh", "country": "India", "latitude": 23.2599, "longitude": 77.4126, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Visakhapatnam", "state": "Andhra Pradesh", "country": "India", "latitude": 17.6868, "longitude": 83.2185, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Vizag"]},
    {"city": "Patna", "state": "Bihar", "country": "India", "latitude": 25.5941, "longitude": 85.1376, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Pataliputra"]},
    {"city": "Vadodara", "state": "Gujarat", "country": "India", "latitude": 22.3072, "longitude": 73.1812, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Baroda"]},
    {"city": "Ghaziabad", "state": "Uttar Pradesh", "country": "India", "latitude": 28.6692, "longitude": 77.4538, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Ludhiana", "state": "Punjab", "country": "India", "latitude": 30.9010, "longitude": 75.8573, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Agra", "state": "Uttar Pradesh", "country": "India", "latitude": 27.1767, "longitude": 78.0081, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Nashik", "state": "Maharashtra", "country": "India", "latitude": 19.9975, "longitude": 73.7898, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Nasik"]},
    {"city": "Faridabad", "state": "Haryana", "country": "India", "latitude": 28.4089, "longitude": 77.3178, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Meerut", "state": "Uttar Pradesh", "country": "India", "latitude": 28.9845, "longitude": 77.7064, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Rajkot", "state": "Gujarat", "country": "India", "latitude": 22.3039, "longitude": 70.8022, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Amritsar", "state": "Punjab", "country": "India", "latitude": 31.6340, "longitude": 74.8723, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Srinagar", "state": "Jammu and Kashmir", "country": "India", "latitude": 34.0837, "longitude": 74.7973, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Aurangabad", "state": "Maharashtra", "country": "India", "latitude": 19.8762, "longitude": 75.3433, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Chhatrapati Sambhajinagar"]},
    {"city": "Dhanbad", "state": "Jharkhand", "country": "India", "latitude": 23.7957, "longitude": 86.4304, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Jodhpur", "state": "Rajasthan", "country": "India", "latitude": 26.2389, "longitude": 73.0243, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Coimbatore", "state": "Tamil Nadu", "country": "India", "latitude": 11.0168, "longitude": 76.9558, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Gwalior", "state": "Madhya Pradesh", "country": "India", "latitude": 26.2183, "longitude": 78.1828, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Vijayawada", "state": "Andhra Pradesh", "country": "India", "latitude": 16.5062, "longitude": 80.6480, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Chandigarh", "state": "Chandigarh", "country": "India", "latitude": 30.7333, "longitude": 76.7794, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Guwahati", "state": "Assam", "country": "India", "latitude": 26.1445, "longitude": 91.7362, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Gauhati"]},
    {"city": "Bhubaneswar", "state": "Odisha", "country": "India", "latitude": 20.2961, "longitude": 85.8245, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Thiruvananthapuram", "state": "Kerala", "country": "India", "latitude": 8.5241, "longitude": 76.9366, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Trivandrum"]},
    {"city": "Kochi", "state": "Kerala", "country": "India", "latitude": 9.9312, "longitude": 76.2673, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Cochin"]},
    {"city": "Mysuru", "state": "Karnataka", "country": "India", "latitude": 12.2958, "longitude": 76.6394, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Mysore"]},
    {"city": "Dehradun", "state": "Uttarakhand", "country": "India", "latitude": 30.3165, "longitude": 78.0322, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Ranchi", "state": "Jharkhand", "country": "India", "latitude": 23.3441, "longitude": 85.3096, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Raipur", "state": "Chhattisgarh", "country": "India", "latitude": 21.2514, "longitude": 81.6296, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Shimla", "state": "Himachal Pradesh", "country": "India", "latitude": 31.1048, "longitude": 77.1734, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Simla"]},
    {"city": "Noida", "state": "Uttar Pradesh", "country": "India", "latitude": 28.5355, "longitude": 77.3910, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},
    {"city": "Gurugram", "state": "Haryana", "country": "India", "latitude": 28.4595, "longitude": 77.0266, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": ["Gurgaon"]},
    {"city": "Jammu", "state": "Jammu and Kashmir", "country": "India", "latitude": 32.7266, "longitude": 74.8570, "timezone_str": "Asia/Kolkata", "timezone_offset": 5.5, "alt_names": []},

    # International Cities & Astrology Centers
    {"city": "London", "state": "England", "country": "United Kingdom", "latitude": 51.5074, "longitude": -0.1278, "timezone_str": "Europe/London", "timezone_offset": 0.0, "alt_names": []},
    {"city": "Greenwich", "state": "England", "country": "United Kingdom", "latitude": 51.4826, "longitude": 0.0077, "timezone_str": "Europe/London", "timezone_offset": 0.0, "alt_names": []},
    {"city": "New York", "state": "New York", "country": "United States", "latitude": 40.7128, "longitude": -74.0060, "timezone_str": "America/New_York", "timezone_offset": -5.0, "alt_names": ["NYC", "Manhattan"]},
    {"city": "Los Angeles", "state": "California", "country": "United States", "latitude": 34.0522, "longitude": -118.2437, "timezone_str": "America/Los_Angeles", "timezone_offset": -8.0, "alt_names": ["LA"]},
    {"city": "San Francisco", "state": "California", "country": "United States", "latitude": 37.7749, "longitude": -122.4194, "timezone_str": "America/Los_Angeles", "timezone_offset": -8.0, "alt_names": ["SF", "Bay Area"]},
    {"city": "San Jose", "state": "California", "country": "United States", "latitude": 37.3382, "longitude": -121.8863, "timezone_str": "America/Los_Angeles", "timezone_offset": -8.0, "alt_names": ["Silicon Valley"]},
    {"city": "Chicago", "state": "Illinois", "country": "United States", "latitude": 41.8781, "longitude": -87.6298, "timezone_str": "America/Chicago", "timezone_offset": -6.0, "alt_names": []},
    {"city": "Houston", "state": "Texas", "country": "United States", "latitude": 29.7604, "longitude": -95.3698, "timezone_str": "America/Chicago", "timezone_offset": -6.0, "alt_names": []},
    {"city": "Dallas", "state": "Texas", "country": "United States", "latitude": 32.7767, "longitude": -96.7970, "timezone_str": "America/Chicago", "timezone_offset": -6.0, "alt_names": []},
    {"city": "Seattle", "state": "Washington", "country": "United States", "latitude": 47.6062, "longitude": -122.3321, "timezone_str": "America/Los_Angeles", "timezone_offset": -8.0, "alt_names": []},
    {"city": "Washington", "state": "District of Columbia", "country": "United States", "latitude": 38.9072, "longitude": -77.0369, "timezone_str": "America/New_York", "timezone_offset": -5.0, "alt_names": ["Washington DC", "DC"]},
    {"city": "Boston", "state": "Massachusetts", "country": "United States", "latitude": 42.3601, "longitude": -71.0589, "timezone_str": "America/New_York", "timezone_offset": -5.0, "alt_names": []},
    {"city": "Toronto", "state": "Ontario", "country": "Canada", "latitude": 43.6532, "longitude": -79.3832, "timezone_str": "America/Toronto", "timezone_offset": -5.0, "alt_names": []},
    {"city": "Vancouver", "state": "British Columbia", "country": "Canada", "latitude": 49.2827, "longitude": -123.1207, "timezone_str": "America/Vancouver", "timezone_offset": -8.0, "alt_names": []},
    {"city": "Sydney", "state": "New South Wales", "country": "Australia", "latitude": -33.8688, "longitude": 151.2093, "timezone_str": "Australia/Sydney", "timezone_offset": 10.0, "alt_names": []},
    {"city": "Melbourne", "state": "Victoria", "country": "Australia", "latitude": -37.8136, "longitude": 144.9631, "timezone_str": "Australia/Melbourne", "timezone_offset": 10.0, "alt_names": []},
    {"city": "Singapore", "state": "Central", "country": "Singapore", "latitude": 1.3521, "longitude": 103.8198, "timezone_str": "Asia/Singapore", "timezone_offset": 8.0, "alt_names": []},
    {"city": "Kuala Lumpur", "state": "Federal Territory", "country": "Malaysia", "latitude": 3.1390, "longitude": 101.6869, "timezone_str": "Asia/Kuala_Lumpur", "timezone_offset": 8.0, "alt_names": ["KL"]},
    {"city": "Dubai", "state": "Dubai", "country": "United Arab Emirates", "latitude": 25.2048, "longitude": 55.2708, "timezone_str": "Asia/Dubai", "timezone_offset": 4.0, "alt_names": ["UAE"]},
    {"city": "Tokyo", "state": "Tokyo", "country": "Japan", "latitude": 35.6762, "longitude": 139.6503, "timezone_str": "Asia/Tokyo", "timezone_offset": 9.0, "alt_names": []},
    {"city": "Paris", "state": "Île-de-France", "country": "France", "latitude": 48.8566, "longitude": 2.3522, "timezone_str": "Europe/Paris", "timezone_offset": 1.0, "alt_names": []},
    {"city": "Berlin", "state": "Berlin", "country": "Germany", "latitude": 52.5200, "longitude": 13.4050, "timezone_str": "Europe/Berlin", "timezone_offset": 1.0, "alt_names": []},
    {"city": "Zurich", "state": "Zurich", "country": "Switzerland", "latitude": 47.3769, "longitude": 8.5417, "timezone_str": "Europe/Zurich", "timezone_offset": 1.0, "alt_names": []},
    {"city": "Kathmandu", "state": "Bagmati", "country": "Nepal", "latitude": 27.7172, "longitude": 85.3240, "timezone_str": "Asia/Kathmandu", "timezone_offset": 5.75, "alt_names": []},
    {"city": "Colombo", "state": "Western", "country": "Sri Lanka", "latitude": 6.9271, "longitude": 79.8612, "timezone_str": "Asia/Colombo", "timezone_offset": 5.5, "alt_names": []},
]

def search_offline_cities(query: str, limit: int = 8) -> List[Dict[str, Any]]:
    """
    Fast offline search for cities by name, state, country, or alternative names.
    Case-insensitive, prioritizes exact starts-with matches.
    """
    q = query.strip().lower()
    if len(q) < 2:
        return []

    prefix_matches = []
    contains_matches = []

    for item in CITIES_DATA:
        city_lower = item["city"].lower()
        state_lower = item["state"].lower()
        country_lower = item["country"].lower()
        alt_lowers = [a.lower() for a in item.get("alt_names", [])]

        disp = f"{item['city']}, {item['state']}, {item['country']}".strip(", ")
        res_dict = {
            "display_name": disp,
            "city": item["city"],
            "state": item["state"],
            "country": item["country"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "timezone_str": item["timezone_str"],
            "timezone_offset": item["timezone_offset"],
        }

        # Check exact prefix on city or alt names
        if city_lower.startswith(q) or any(a.startswith(q) for a in alt_lowers):
            prefix_matches.append(res_dict)
        elif q in city_lower or q in state_lower or q in country_lower or any(q in a for a in alt_lowers):
            contains_matches.append(res_dict)

    combined = prefix_matches + contains_matches
    return combined[:limit]
