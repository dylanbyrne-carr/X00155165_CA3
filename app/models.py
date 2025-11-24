import random
from typing import List, Dict
from flask_login import UserMixin

class User(UserMixin):
    """
    USer model for authentication
    UserMixin has useful methods for Flask-login
    """

    def __init__(self, id: int, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password

USERS = {
    'user': User(1, 'user', 'password'),
    'admin': User(2, 'admin', 'admin123')
}

def get_user(username: str):
    return USERS.get(username)

def get_user_by_id(user_id):
    """Get user by ID - required by Flask-Login."""
    for user in USERS.values():
        if str(user.id) == str(user_id):
            return user
    return None
class DiceRoller:
    """A dice roller with history tracking and statistics"""

    def __init__(self):
        self.history: List[int] = []

    def roll(self, num_dice: int = 1, sides: int = 6) -> List[int]:
        """Roll one or more dice."""
        if num_dice < 1:
            raise ValueError("Must roll at least one die")
        if sides < 1:
            raise ValueError("Die must have at least one side")
        results = [random.randint(1, sides) for _ in range (num_dice)]
        self.history.extend(results)
        return results

    def roll_sum(self, num_dice: int = 2, sides: int = 6) -> int:
        """Roll mulptiple dice and return the sum."""
        return sum(self.roll(num_dice, sides))

    def get_history(self) -> List[int]:
        """Get all previous rolls."""
        return self.history.copy()

    def clear_history(self) -> None:
        """Clear roll history."""
        self.history.clear()

    def get_stats(self) -> Dict[str, float]:
        """
        Get statistics for all rolls.
        
        Returns:
            Dictionary with average, min, max, count
        """
        if not self.history:
            return {'average': 0, 'min': 0, 'max': 0, 'count': 0}

        return{
            'average': sum(self.history) / len(self.history),
            'min': min(self.history),
            'max': max(self.history),
            'count': len(self.history)
        }
