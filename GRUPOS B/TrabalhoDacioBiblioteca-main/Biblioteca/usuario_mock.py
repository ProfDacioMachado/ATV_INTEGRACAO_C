class UserStoreMock:
    """
    Mock simples de Users: mantém um conjunto de IDs.
    Interface mínima:
      - add(user_id)
      - exists(user_id) -> bool
    """
    def __init__(self):
        self._users = set()

    def add(self, user_id: int):
        self._users.add(user_id)

    def exists(self, user_id: int) -> bool:
        return user_id in self._users