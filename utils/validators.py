def validate_city_name(city, command):

    if not city:
        return (
            f"⚠️ You must provide a city name! "
            f"Use: `!{command} city_name` ⚠️"
        )

    if not city.replace(" ", "").isalpha():
        return "⚠️ The city name can only contain letters! ⚠️"

    if len(city) > 30:
        return "⚠️ The city name is too long! ⚠️"

    return None