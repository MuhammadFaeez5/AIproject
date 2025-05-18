def rule_based_signal_timing(row):
    strategies = []
    
    # Convert all inputs to proper types first
    try:
        rain = float(row["rain_1h"])
        snow = float(row["snow_1h"])
        vehicles = int(row["Vehicles"])
        hour = int(row["hour"])
        clouds = int(row["clouds_all"])
        congestion = bool(int(row.get("congestion_pred", 0)))
        weekend = bool(int(row.get("is_weekend", 0)))
    except (KeyError, ValueError) as e:
        print(f"Error converting inputs: {e}")
        return ["⚠️ System error - using default timing"]

    # Define conditions clearly
    is_rainy = rain > 0.2
    is_snowy = snow > 0
    high_vehicles = vehicles > 50
    rush_hour = hour in {7,8,9,16,17,18}  # Using set for faster lookup
    visibility_low = clouds > 75
    weekend_daytime = weekend and (10 <= hour <= 18)

    # Build strategy list - all conditions checked independently
    if high_vehicles:
        strategies.append("🚦 Extend green time (high traffic volume)")
    
    if is_snowy:
        strategies.append("❄️ Reduce speed limits (snow conditions)")
    
    if congestion and rush_hour:
        strategies.append("⏰ Rush hour mode (extended green times)")
    
    if congestion and (is_rainy or is_snowy):
        strategies.append("⚠️ Weather alert mode (safety buffers)")
    
    if visibility_low:
        strategies.append("🌫️ Extended clearance (low visibility)")
    
    if weekend_daytime:
        strategies.append("🟰 Weekend traffic pattern timing")

    # Default if no special conditions
    if not strategies:
        strategies.append("✅ Normal signal operation")

    return strategies