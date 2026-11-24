export interface CityLocation {
  display_name: string;
  city: string;
  state: string;
  country: string;
  latitude: number;
  longitude: number;
  timezone_str: string;
  timezone_offset: number;
  alt_names?: string[];
}

export const MAJOR_CITIES: CityLocation[] = [
  // Sacred & Classical Vedic Astrology Centers
  { city: "Varanasi", state: "Uttar Pradesh", country: "India", latitude: 25.3176, longitude: 82.9739, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Varanasi (Kashi), Uttar Pradesh, India", alt_names: ["Benares", "Kashi"] },
  { city: "Ujjain", state: "Madhya Pradesh", country: "India", latitude: 23.1765, longitude: 75.7885, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Ujjain (Avantika), Madhya Pradesh, India", alt_names: ["Avanti", "Avantika"] },
  { city: "Ayodhya", state: "Uttar Pradesh", country: "India", latitude: 26.7922, longitude: 82.1998, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Ayodhya, Uttar Pradesh, India", alt_names: ["Saket"] },
  { city: "Haridwar", state: "Uttarakhand", country: "India", latitude: 29.9457, longitude: 78.1642, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Haridwar, Uttarakhand, India", alt_names: ["Hardwar", "Mayapuri"] },
  { city: "Rishikesh", state: "Uttarakhand", country: "India", latitude: 30.0869, longitude: 78.2676, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Rishikesh, Uttarakhand, India" },
  { city: "Prayagraj", state: "Uttar Pradesh", country: "India", latitude: 25.4358, longitude: 81.8463, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Prayagraj (Allahabad), Uttar Pradesh, India", alt_names: ["Allahabad", "Prayag"] },
  { city: "Mathura", state: "Uttar Pradesh", country: "India", latitude: 27.4924, longitude: 77.6737, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Mathura, Uttar Pradesh, India", alt_names: ["Braj"] },
  { city: "Vrindavan", state: "Uttar Pradesh", country: "India", latitude: 27.5806, longitude: 77.7006, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Vrindavan, Uttar Pradesh, India", alt_names: ["Brindavan"] },
  { city: "Puri", state: "Odisha", country: "India", latitude: 19.8135, longitude: 85.8312, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Puri (Jagannath Dham), Odisha, India", alt_names: ["Jagannath Puri"] },
  { city: "Dwarka", state: "Gujarat", country: "India", latitude: 22.2442, longitude: 68.9685, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Dwarka, Gujarat, India", alt_names: ["Dwaraka"] },
  { city: "Rameswaram", state: "Tamil Nadu", country: "India", latitude: 9.2876, longitude: 79.3129, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Rameswaram, Tamil Nadu, India", alt_names: ["Rameshwaram"] },
  { city: "Tirupati", state: "Andhra Pradesh", country: "India", latitude: 13.6288, longitude: 79.4192, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Tirupati, Andhra Pradesh, India", alt_names: ["Tirumala"] },
  { city: "Madurai", state: "Tamil Nadu", country: "India", latitude: 9.9252, longitude: 78.1198, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Madurai, Tamil Nadu, India" },
  { city: "Kanchipuram", state: "Tamil Nadu", country: "India", latitude: 12.8342, longitude: 79.7036, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Kanchipuram, Tamil Nadu, India" },
  { city: "Gaya", state: "Bihar", country: "India", latitude: 24.7914, longitude: 85.0002, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Gaya (Bodh Gaya), Bihar, India" },
  { city: "Somnath", state: "Gujarat", country: "India", latitude: 20.8880, longitude: 70.4012, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Somnath, Gujarat, India" },
  { city: "Shirdi", state: "Maharashtra", country: "India", latitude: 19.7667, longitude: 74.4764, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Shirdi, Maharashtra, India" },

  // Major Indian Metros and Capitals
  { city: "New Delhi", state: "Delhi", country: "India", latitude: 28.6139, longitude: 77.2090, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "New Delhi, Delhi, India", alt_names: ["Delhi", "NCR"] },
  { city: "Mumbai", state: "Maharashtra", country: "India", latitude: 19.0760, longitude: 72.8777, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Mumbai (Bombay), Maharashtra, India", alt_names: ["Bombay"] },
  { city: "Kolkata", state: "West Bengal", country: "India", latitude: 22.5726, longitude: 88.3639, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Kolkata (Calcutta), West Bengal, India", alt_names: ["Calcutta"] },
  { city: "Chennai", state: "Tamil Nadu", country: "India", latitude: 13.0827, longitude: 80.2707, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Chennai (Madras), Tamil Nadu, India", alt_names: ["Madras"] },
  { city: "Bengaluru", state: "Karnataka", country: "India", latitude: 12.9716, longitude: 77.5946, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Bengaluru (Bangalore), Karnataka, India", alt_names: ["Bangalore"] },
  { city: "Hyderabad", state: "Telangana", country: "India", latitude: 17.3850, longitude: 78.4867, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Hyderabad, Telangana, India", alt_names: ["Secunderabad"] },
  { city: "Ahmedabad", state: "Gujarat", country: "India", latitude: 23.0225, longitude: 72.5714, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Ahmedabad, Gujarat, India", alt_names: ["Amdavad"] },
  { city: "Pune", state: "Maharashtra", country: "India", latitude: 18.5204, longitude: 73.8567, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Pune (Poona), Maharashtra, India", alt_names: ["Poona"] },
  { city: "Jaipur", state: "Rajasthan", country: "India", latitude: 26.9124, longitude: 75.7873, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Jaipur, Rajasthan, India" },
  { city: "Lucknow", state: "Uttar Pradesh", country: "India", latitude: 26.8467, longitude: 80.9462, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Lucknow, Uttar Pradesh, India" },
  { city: "Kanpur", state: "Uttar Pradesh", country: "India", latitude: 26.4499, longitude: 80.3319, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Kanpur, Uttar Pradesh, India" },
  { city: "Nagpur", state: "Maharashtra", country: "India", latitude: 21.1458, longitude: 79.0882, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Nagpur, Maharashtra, India" },
  { city: "Indore", state: "Madhya Pradesh", country: "India", latitude: 22.7196, longitude: 75.8577, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Indore, Madhya Pradesh, India" },
  { city: "Thane", state: "Maharashtra", country: "India", latitude: 19.2183, longitude: 72.9781, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Thane, Maharashtra, India" },
  { city: "Bhopal", state: "Madhya Pradesh", country: "India", latitude: 23.2599, longitude: 77.4126, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Bhopal, Madhya Pradesh, India" },
  { city: "Visakhapatnam", state: "Andhra Pradesh", country: "India", latitude: 17.6868, longitude: 83.2185, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Visakhapatnam (Vizag), Andhra Pradesh, India", alt_names: ["Vizag"] },
  { city: "Patna", state: "Bihar", country: "India", latitude: 25.5941, longitude: 85.1376, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Patna, Bihar, India", alt_names: ["Pataliputra"] },
  { city: "Vadodara", state: "Gujarat", country: "India", latitude: 22.3072, longitude: 73.1812, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Vadodara (Baroda), Gujarat, India", alt_names: ["Baroda"] },
  { city: "Ghaziabad", state: "Uttar Pradesh", country: "India", latitude: 28.6692, longitude: 77.4538, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Ghaziabad, Uttar Pradesh, India" },
  { city: "Ludhiana", state: "Punjab", country: "India", latitude: 30.9010, longitude: 75.8573, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Ludhiana, Punjab, India" },
  { city: "Agra", state: "Uttar Pradesh", country: "India", latitude: 27.1767, longitude: 78.0081, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Agra, Uttar Pradesh, India" },
  { city: "Nashik", state: "Maharashtra", country: "India", latitude: 19.9975, longitude: 73.7898, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Nashik, Maharashtra, India" },
  { city: "Faridabad", state: "Haryana", country: "India", latitude: 28.4089, longitude: 77.3178, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Faridabad, Haryana, India" },
  { city: "Meerut", state: "Uttar Pradesh", country: "India", latitude: 28.9845, longitude: 77.7064, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Meerut, Uttar Pradesh, India" },
  { city: "Rajkot", state: "Gujarat", country: "India", latitude: 22.3039, longitude: 70.8022, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Rajkot, Gujarat, India" },
  { city: "Amritsar", state: "Punjab", country: "India", latitude: 31.6340, longitude: 74.8723, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Amritsar, Punjab, India" },
  { city: "Srinagar", state: "Jammu and Kashmir", country: "India", latitude: 34.0837, longitude: 74.7973, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Srinagar, Jammu and Kashmir, India" },
  { city: "Aurangabad", state: "Maharashtra", country: "India", latitude: 19.8762, longitude: 75.3433, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Aurangabad, Maharashtra, India", alt_names: ["Chhatrapati Sambhajinagar"] },
  { city: "Jodhpur", state: "Rajasthan", country: "India", latitude: 26.2389, longitude: 73.0243, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Jodhpur, Rajasthan, India" },
  { city: "Coimbatore", state: "Tamil Nadu", country: "India", latitude: 11.0168, longitude: 76.9558, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Coimbatore, Tamil Nadu, India" },
  { city: "Gwalior", state: "Madhya Pradesh", country: "India", latitude: 26.2183, longitude: 78.1828, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Gwalior, Madhya Pradesh, India" },
  { city: "Vijayawada", state: "Andhra Pradesh", country: "India", latitude: 16.5062, longitude: 80.6480, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Vijayawada, Andhra Pradesh, India" },
  { city: "Chandigarh", state: "Chandigarh", country: "India", latitude: 30.7333, longitude: 76.7794, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Chandigarh, India" },
  { city: "Guwahati", state: "Assam", country: "India", latitude: 26.1445, longitude: 91.7362, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Guwahati, Assam, India" },
  { city: "Bhubaneswar", state: "Odisha", country: "India", latitude: 20.2961, longitude: 85.8245, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Bhubaneswar, Odisha, India" },
  { city: "Thiruvananthapuram", state: "Kerala", country: "India", latitude: 8.5241, longitude: 76.9366, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Thiruvananthapuram, Kerala, India", alt_names: ["Trivandrum"] },
  { city: "Kochi", state: "Kerala", country: "India", latitude: 9.9312, longitude: 76.2673, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Kochi (Cochin), Kerala, India", alt_names: ["Cochin"] },
  { city: "Mysuru", state: "Karnataka", country: "India", latitude: 12.2958, longitude: 76.6394, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Mysuru (Mysore), Karnataka, India", alt_names: ["Mysore"] },
  { city: "Dehradun", state: "Uttarakhand", country: "India", latitude: 30.3165, longitude: 78.0322, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Dehradun, Uttarakhand, India" },
  { city: "Ranchi", state: "Jharkhand", country: "India", latitude: 23.3441, longitude: 85.3096, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Ranchi, Jharkhand, India" },
  { city: "Raipur", state: "Chhattisgarh", country: "India", latitude: 21.2514, longitude: 81.6296, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Raipur, Chhattisgarh, India" },
  { city: "Shimla", state: "Himachal Pradesh", country: "India", latitude: 31.1048, longitude: 77.1734, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Shimla, Himachal Pradesh, India" },
  { city: "Noida", state: "Uttar Pradesh", country: "India", latitude: 28.5355, longitude: 77.3910, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Noida, Uttar Pradesh, India" },
  { city: "Gurugram", state: "Haryana", country: "India", latitude: 28.4595, longitude: 77.0266, timezone_str: "Asia/Kolkata", timezone_offset: 5.5, display_name: "Gurugram (Gurgaon), Haryana, India", alt_names: ["Gurgaon"] },

  // Global Hubs
  { city: "London", state: "England", country: "United Kingdom", latitude: 51.5074, longitude: -0.1278, timezone_str: "Europe/London", timezone_offset: 0.0, display_name: "London, England, United Kingdom" },
  { city: "New York", state: "New York", country: "United States", latitude: 40.7128, longitude: -74.0060, timezone_str: "America/New_York", timezone_offset: -5.0, display_name: "New York, NY, United States", alt_names: ["NYC", "Manhattan"] },
  { city: "San Francisco", state: "California", country: "United States", latitude: 37.7749, longitude: -122.4194, timezone_str: "America/Los_Angeles", timezone_offset: -8.0, display_name: "San Francisco, CA, United States", alt_names: ["SF"] },
  { city: "San Jose", state: "California", country: "United States", latitude: 37.3382, longitude: -121.8863, timezone_str: "America/Los_Angeles", timezone_offset: -8.0, display_name: "San Jose, CA, United States" },
  { city: "Los Angeles", state: "California", country: "United States", latitude: 34.0522, longitude: -118.2437, timezone_str: "America/Los_Angeles", timezone_offset: -8.0, display_name: "Los Angeles, CA, United States", alt_names: ["LA"] },
  { city: "Chicago", state: "Illinois", country: "United States", latitude: 41.8781, longitude: -87.6298, timezone_str: "America/Chicago", timezone_offset: -6.0, display_name: "Chicago, IL, United States" },
  { city: "Houston", state: "Texas", country: "United States", latitude: 29.7604, longitude: -95.3698, timezone_str: "America/Chicago", timezone_offset: -6.0, display_name: "Houston, TX, United States" },
  { city: "Dallas", state: "Texas", country: "United States", latitude: 32.7767, longitude: -96.7970, timezone_str: "America/Chicago", timezone_offset: -6.0, display_name: "Dallas, TX, United States" },
  { city: "Seattle", state: "Washington", country: "United States", latitude: 47.6062, longitude: -122.3321, timezone_str: "America/Los_Angeles", timezone_offset: -8.0, display_name: "Seattle, WA, United States" },
  { city: "Toronto", state: "Ontario", country: "Canada", latitude: 43.6532, longitude: -79.3832, timezone_str: "America/Toronto", timezone_offset: -5.0, display_name: "Toronto, ON, Canada" },
  { city: "Vancouver", state: "British Columbia", country: "Canada", latitude: 49.2827, longitude: -123.1207, timezone_str: "America/Vancouver", timezone_offset: -8.0, display_name: "Vancouver, BC, Canada" },
  { city: "Sydney", state: "New South Wales", country: "Australia", latitude: -33.8688, longitude: 151.2093, timezone_str: "Australia/Sydney", timezone_offset: 10.0, display_name: "Sydney, NSW, Australia" },
  { city: "Melbourne", state: "Victoria", country: "Australia", latitude: -37.8136, longitude: 144.9631, timezone_str: "Australia/Melbourne", timezone_offset: 10.0, display_name: "Melbourne, VIC, Australia" },
  { city: "Singapore", state: "Central", country: "Singapore", latitude: 1.3521, longitude: 103.8198, timezone_str: "Asia/Singapore", timezone_offset: 8.0, display_name: "Singapore" },
  { city: "Dubai", state: "Dubai", country: "United Arab Emirates", latitude: 25.2048, longitude: 55.2708, timezone_str: "Asia/Dubai", timezone_offset: 4.0, display_name: "Dubai, United Arab Emirates" },
  { city: "Tokyo", state: "Tokyo", country: "Japan", latitude: 35.6762, longitude: 139.6503, timezone_str: "Asia/Tokyo", timezone_offset: 9.0, display_name: "Tokyo, Japan" },
  { city: "Paris", state: "Île-de-France", country: "France", latitude: 48.8566, longitude: 2.3522, timezone_str: "Europe/Paris", timezone_offset: 1.0, display_name: "Paris, France" },
  { city: "Berlin", state: "Berlin", country: "Germany", latitude: 52.5200, longitude: 13.4050, timezone_str: "Europe/Berlin", timezone_offset: 1.0, display_name: "Berlin, Germany" },
  { city: "Zurich", state: "Zurich", country: "Switzerland", latitude: 47.3769, longitude: 8.5417, timezone_str: "Europe/Zurich", timezone_offset: 1.0, display_name: "Zurich, Switzerland" },
  { city: "Kathmandu", state: "Bagmati", country: "Nepal", latitude: 27.7172, longitude: 85.3240, timezone_str: "Asia/Kathmandu", timezone_offset: 5.75, display_name: "Kathmandu, Nepal" },
  { city: "Colombo", state: "Western", country: "Sri Lanka", latitude: 6.9271, longitude: 79.8612, timezone_str: "Asia/Colombo", timezone_offset: 5.5, display_name: "Colombo, Sri Lanka" },
];

export function searchClientCities(query: string, limit: number = 8): CityLocation[] {
  const q = query.trim().toLowerCase();
  if (q.length < 2) return [];

  const prefixMatches: CityLocation[] = [];
  const containsMatches: CityLocation[] = [];

  for (const item of MAJOR_CITIES) {
    const cityLower = item.city.toLowerCase();
    const stateLower = item.state.toLowerCase();
    const countryLower = item.country.toLowerCase();
    const altLowers = (item.alt_names || []).map((a) => a.toLowerCase());

    if (cityLower.startsWith(q) || altLowers.some((a) => a.startsWith(q))) {
      prefixMatches.push(item);
    } else if (
      cityLower.includes(q) ||
      stateLower.includes(q) ||
      countryLower.includes(q) ||
      altLowers.some((a) => a.includes(q))
    ) {
      containsMatches.push(item);
    }
  }

  return [...prefixMatches, ...containsMatches].slice(0, limit);
}
