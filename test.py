respone= '"hhh"'
def remove_trailing_quote(s: str) -> str:
    return s[:-1] if s.endswith('"') else s
print (remove_trailing_quote(respone))