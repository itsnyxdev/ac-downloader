def resolution(res: str) -> tuple[int, int]:
    x = int(res.split("x")[0])
    y = int(res.split("x")[1])
    return x, y
