import pytest
from app.models import DiceRoller


class TestBasicRolling:
    """Test basic dice rolling."""

    def setup_method(self):
        """Set up test - runs before each test."""
        self.roller = DiceRoller()

    def test_roll_default(self):
        """Test rolling 1d6 (default)."""
        result = self.roller.roll()
        assert len(result) == 1
        assert 1 <= result[0] <= 6

    def test_roll_multiple_dice(self):
        """Test rolling multiple dice."""
        result = self.roller.roll(3, 6)
        assert len(result) == 3
        for roll in result:
            assert 1 <= roll <= 6

    def test_roll_different_sides(self):
        """Test different dice types."""
        result = self.roller.roll(1, 20)
        assert 1 <= result[0] <= 20

    def test_roll_invalid_num_dice(self):
        """Test that invalid number of dice raises error."""
        with pytest.raises(ValueError):
            self.roller.roll(0, 6)

    def test_roll_invalid_sides(self):
        """Test that invalid sides raises error."""
        with pytest.raises(ValueError):
            self.roller.roll(1, 0)


class TestRollSum:
    """Test sum functionality."""

    def setup_method(self):
        self.roller = DiceRoller()

    def test_roll_sum_default(self):
        """Test sum with default params (2d6)."""
        result = self.roller.roll_sum()
        assert 2 <= result <= 12

    def test_roll_sum_custom(self):
        """Test sum with custom dice."""
        result = self.roller.roll_sum(3, 6)
        assert 3 <= result <= 18


class TestHistory:
    """Test history tracking."""

    def setup_method(self):
        self.roller = DiceRoller()

    def test_history_tracks_rolls(self):
        """Test that rolls are tracked."""
        self.roller.roll(3, 6)
        assert len(self.roller.get_history()) == 3

    def test_history_clear(self):
        """Test clearing history."""
        self.roller.roll(5, 6)
        self.roller.clear_history()
        assert len(self.roller.get_history()) == 0


class TestStatistics:
    """Test statistics feature."""

    def setup_method(self):
        self.roller = DiceRoller()

    def test_stats_empty(self):
        """Test stats with no history."""
        stats = self.roller.get_stats()
        assert stats['average'] == 0
        assert stats['count'] == 0

    def test_stats_with_rolls(self):
        """Test stats calculation."""
        self.roller.history = [1, 2, 3, 4, 5]
        stats = self.roller.get_stats()
        assert stats['average'] == 3.0
        assert stats['min'] == 1
        assert stats['max'] == 5
        assert stats['count'] == 5