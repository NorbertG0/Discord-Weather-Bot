def validate_city_name(city, command):

    if not city or not city.strip():
        return (
            f"⚠️ You must provide a city name! "
            f"Use: `!{command} city_name` ⚠️"
        )

    city = city.strip()

    if len(city) > 50:
        return "⚠️ The city name is too long! ⚠️"

    if not all(char.isalpha() or char in " -'." for char in city):
        return "⚠️ The city name contains invalid characters! ⚠️"

    return None