
def c(m:str, r: int, g: int, b:int) -> str:
    return f'\x1b[38;2;{r};{g};{b}m{m}\x1b[0m'