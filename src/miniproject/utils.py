"""Utility functions for the miniproject package."""


def pos_neg_view(number: float | str, pct: bool = False) -> str:
    """Return a string with positive or negative styling based on the number.

    Args:
        number (int | float | str): The number to style.
        pct (bool): If true include the sufix '%' at number.

    Returns:
        str: The styled number as a string.
    """
    if not isinstance(number, str):
        number = str(number)
    if '-' not in number:
        return f'[positive]{number + "%" if pct else number}[/positive]'
    return f'[negative]{number + "%" if pct else number}[/negative]'


def br_number(number: float | str, decimals: int = 2, pct: bool = False) -> str:
    """Format a number according to Brazilian conventions.

    Args:
        number (float | str): The number to be formatted.
        decimals (int): The number of decimal places to format the number with. Default is 2.

    Returns:
        str: The formatted number as a string with thousands separator. Example: 1.234.567,89
    """
    # Deve coverter formatos como "1234567,59" para "1.234.567,59" ou "1234567.59" para "1.234.567,59"
    if isinstance(number, str):
        number = number.replace(',', '.')
        number = float(number)
    formatted_number = f'{number:,.{decimals}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return pos_neg_view(formatted_number, pct=pct)


if __name__ == '__main__':
    # Test the utility functions
    print(pos_neg_view(10850.45))
    print(pos_neg_view(-5))
    print(br_number(1234567.89))
    print(br_number(-1234567.89))
