import colorsys


def generate_distinct_colors(n, saturation=0.7, value=0.95):
    """
    Generate n distinct hexadecimal colors for plotting markers on a map.

    Args:
        n (int): Number of distinct colors to generate.
        saturation (float, optional): Saturation level (0.0 to 1.0). Defaults to 0.7.
        value (float, optional): Value/brightness level (0.0 to 1.0). Defaults to 0.95.

    Returns:
        list: List of n hexadecimal color codes (e.g., ['#FF0000', '#00FF00', ...]).
    """
    colors = []
    for i in range(n):
        # Distribute hues evenly around the color wheel
        hue = i / n
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        # Convert RGB to hexadecimal
        hex_color = "#{:02X}{:02X}{:02X}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )
        colors.append(hex_color)
    return colors
