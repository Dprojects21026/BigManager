def Color(
    text: str,
    rgb_sys: bool,
    **kwargs
):
    class ColorError(Exception):
        pass

    colors = {
        "red": (255,0,0),
        "green": (0,255,0),
        "blue": (0,0,255),
        "yellow": (255,255,0),
        "purple": (255,0,255)
    }
    rgb = (255,255,255)
    if not rgb_sys:
        ready_color = kwargs.get("ready_color", "")
        if not isinstance(ready_color, str):
            raise ColorError("The ready color must be a string.")
        ready_color = ready_color.strip()
        if not ready_color:
            raise ColorError("The ready color must be set.")
        if ready_color not in colors.keys():
            raise ColorError(f"Ready color {ready_color} does not exist.\nReady colors: {colors.keys()}")
        rgb = colors[ready_color]
    else:
        rgb = kwargs.get("rgb", ())
        if not isinstance(rgb, tuple):
            raise ColorError("The 'rgb' must be a tuple of 3 integers.")
    rn_1 = 0
    if len(rgb) != 3:
        raise ColorError("The 'rgb' must be a tuple of 3 integers.")
    for color in rgb:
        if type(color) is not int:
            if rn_1 == 0:
                raise ColorError(f"Every part of the color must be an 'int' object. Caused: {color}(red)")
            elif rn_1 == 1:
                raise ColorError(f"Every part of the color must be an 'int' object. Caused: {color}(green)")
            elif rn_1 == 2:
                raise ColorError(f"Every part of the color must be an 'int' object. Caused: {color}(blue)")
            else:
                raise ColorError("Unknown error.")
        if not 0 <= color <= 255:
            raise ColorError("RGB values must be between 0 and 255.")
        rn_1 += 1
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{text}\033[0m"
