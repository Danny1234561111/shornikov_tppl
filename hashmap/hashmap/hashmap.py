import re
class Iloc:
    def __init__(self, data):
        self.iloc = list(data[key] for key in sorted(data, key=str))

    def __getitem__(self, index):
        if not 0 <= index < len(self.iloc):
            raise IndexError("Index out of range")
        return self.iloc[index]
class Ploc:
    def __init__(self, data):
        self._data = data

    def _parse_condition(self, condition):
        match = re.match(r'([<>=]+)(-?\d+\.?\d*)', condition.strip())
        if not match:
            raise ValueError("Invalid condition format")
        op, value = match.groups()
        return op, float(value)

    def _check_condition(self, value, op, condition_value):
        if op == '>': return value > condition_value
        if op == '>=': return value >= condition_value
        if op == '<': return value < condition_value
        if op == '<=': return value <= condition_value
        if op == '=': return value == condition_value
        if op == '<>': return value != condition_value
        raise ValueError(f"Invalid operator: {op}")

    def _extract_key_values(self, key):
        key = key.replace("(", "").replace(")", "").strip()
        return [float(x) for x in re.split(r'[^0-9\.\-]+', key) if x]

    def __getitem__(self, conditions):
        if re.search(r'[a-zA-Z]', conditions):
            raise ValueError("Invalid condition format")
        conditions = [c.strip() for c in re.split(r',', conditions) if c.strip()]
        result = {}
        for key, value in self._data.items():
            if isinstance(key, str) and not re.search(r'[a-zA-Z]', key):
                key_values = self._extract_key_values(key)
                if len(key_values) != len(conditions): continue
                if all(self._check_condition(key_values[i], *self._parse_condition(conditions[i])) for i in range(len(conditions))):
                    result[key] = value
            elif len(conditions) == 1:
                try:
                  key_num = float(key)
                  op, condition_value = self._parse_condition(conditions[0])
                  if self._check_condition(key_num, op, condition_value):
                      result[str(key)] = value
                except ValueError:
                  continue
        return result
class SpecialHashMap(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iloc = Iloc(self)
        self.ploc = Ploc(self)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.iloc = Iloc(self)
        self.ploc = Ploc(self)

    def __delitem__(self, key):
        super().__delitem__(key)
        self.iloc = Iloc(self)
        self.ploc = Ploc(self)