import copy
import io
import unittest

from contextlib import redirect_stdout
from unittest.mock import patch

import risk_game


class TestRiskGame(unittest.TestCase):

    # Run before every test
    def setUp(self):

        risk_game.reset_game()
        risk_game.reset_game_metrics()


    # ---------------------------------------
    # Test 1: starting territory ownership
    # ---------------------------------------

    def test_starting_territories(self):

        player_1_territories = (
            risk_game.get_player_territories("Player 1")
        )

        player_2_territories = (
            risk_game.get_player_territories("Player 2")
        )

        self.assertEqual(
            player_1_territories,
            ["A", "B", "C"]
        )

        self.assertEqual(
            player_2_territories,
            ["D", "E", "F"]
        )


    # ---------------------------------------
    # Test 2: valid attacks
    # ---------------------------------------

    def test_valid_attacks(self):

        player_1_attacks = (
            risk_game.get_valid_attacks("Player 1")
        )

        self.assertIn(
            ("B", "D"),
            player_1_attacks
        )

        self.assertIn(
            ("C", "E"),
            player_1_attacks
        )

        # Player 1 cannot attack its own territory
        self.assertNotIn(
            ("A", "B"),
            player_1_attacks
        )


    # ---------------------------------------
    # Test 3: reinforcement calculation
    # ---------------------------------------

    def test_reinforcement_calculation(self):

        reinforcements = (
            risk_game.calculate_reinforcements(
                "Player 1"
            )
        )

        # Three territories gives one army
        self.assertEqual(
            reinforcements,
            1
        )


    # ---------------------------------------
    # Test 4: valid reinforcement
    # ---------------------------------------

    def test_valid_reinforcement(self):

        armies_before = (
            risk_game.territories["B"]["armies"]
        )

        with redirect_stdout(io.StringIO()):

            result = risk_game.reinforce_territory(
                "Player 1",
                "B",
                2
            )

        armies_after = (
            risk_game.territories["B"]["armies"]
        )

        self.assertTrue(result)

        self.assertEqual(
            armies_after,
            armies_before + 2
        )


    # ---------------------------------------
    # Test 5: invalid reinforcement
    # ---------------------------------------

    def test_invalid_reinforcement(self):

        armies_before = (
            risk_game.territories["D"]["armies"]
        )

        with redirect_stdout(io.StringIO()):

            result = risk_game.reinforce_territory(
                "Player 1",
                "D",
                2
            )

        armies_after = (
            risk_game.territories["D"]["armies"]
        )

        self.assertFalse(result)

        self.assertEqual(
            armies_after,
            armies_before
        )


    # ---------------------------------------
    # Test 6: defender wins equal dice
    # ---------------------------------------

    def test_defender_wins_tie(self):

        with redirect_stdout(io.StringIO()):

            attacker_losses, defender_losses = (
                risk_game.compare_dice(
                    [5],
                    [5]
                )
            )

        self.assertEqual(
            attacker_losses,
            1
        )

        self.assertEqual(
            defender_losses,
            0
        )


    # ---------------------------------------
    # Test 7: deterministic territory capture
    # ---------------------------------------

    @patch(
        "risk_game.roll_dice",
        side_effect=[
            [6, 5, 4],
            [1]
        ]
    )
    def test_territory_capture(
        self,
        mocked_roll_dice
    ):

        risk_game.territories["B"]["armies"] = 4
        risk_game.territories["D"]["armies"] = 1

        with redirect_stdout(io.StringIO()):

            captured = risk_game.attack_territory(
                "B",
                "D"
            )

        self.assertTrue(captured)

        self.assertEqual(
            risk_game.territories["D"]["owner"],
            "Player 1"
        )

        self.assertEqual(
            risk_game.territories["D"]["armies"],
            1
        )

        self.assertEqual(
            risk_game.game_metrics[
                "Player 1"
            ]["territories_captured"],
            1
        )


    # ---------------------------------------
    # Test 8: invalid attack
    # ---------------------------------------

    def test_invalid_attack_against_own_territory(self):

        with redirect_stdout(io.StringIO()):

            result = risk_game.attack_territory(
                "A",
                "B"
            )

        self.assertFalse(result)


    # ---------------------------------------
    # Test 9: winner detection
    # ---------------------------------------

    def test_winner_detection(self):

        for territory_data in (
            risk_game.territories.values()
        ):

            territory_data["owner"] = "Player 1"

        winner = risk_game.check_winner()

        self.assertEqual(
            winner,
            "Player 1"
        )


    # ---------------------------------------
    # Test 10: reset game
    # ---------------------------------------

    def test_game_reset(self):

        risk_game.territories["B"]["armies"] = 20
        risk_game.territories["D"]["owner"] = "Player 1"

        risk_game.reset_game()

        self.assertEqual(
            risk_game.territories["B"]["armies"],
            3
        )

        self.assertEqual(
            risk_game.territories["D"]["owner"],
            "Player 2"
        )


    # ---------------------------------------
    # Test 11: metrics reset
    # ---------------------------------------

    def test_metrics_reset(self):

        risk_game.game_metrics[
            "Player 1"
        ]["attacks_made"] = 10

        risk_game.reset_game_metrics()

        self.assertEqual(
            risk_game.game_metrics[
                "Player 1"
            ]["attacks_made"],
            0
        )


    # ---------------------------------------
    # Test 12: reproducible game outcome
    # ---------------------------------------

    def test_reproducible_random_seed(self):

        with redirect_stdout(io.StringIO()):

            winner_1, turns_1, metrics_1 = (
                risk_game.play_game(
                    max_turns=100,
                    player_1_agent="Random Agent",
                    player_2_agent="Rule-Based Agent",
                    random_seed=12345
                )
            )

            winner_2, turns_2, metrics_2 = (
                risk_game.play_game(
                    max_turns=100,
                    player_1_agent="Random Agent",
                    player_2_agent="Rule-Based Agent",
                    random_seed=12345
                )
            )

        self.assertEqual(
            winner_1,
            winner_2
        )

        self.assertEqual(
            turns_1,
            turns_2
        )

        # Decision time is excluded because timing
        # can vary slightly between executions
        for player_name in [
            "Player 1",
            "Player 2"
        ]:

            for metric_name in [
                "attacks_made",
                "successful_attacks",
                "armies_lost",
                "territories_captured",
                "decisions_made",
                "simulations_run"
            ]:

                self.assertEqual(
                    metrics_1[
                        player_name
                    ][metric_name],

                    metrics_2[
                        player_name
                    ][metric_name]
                )


if __name__ == "__main__":
    unittest.main()