from django.test import TestCase

from .minesweeper import GameState, new_game, reveal, to_public_payload


class MinesweeperRulesTests(TestCase):
    def test_first_reveal_is_never_a_mine(self):
        state = new_game(4, 4, 5, seed=2)
        first_mine = next(iter(state.mines_set))

        reveal(state, *first_mine)

        self.assertFalse(state.over)
        self.assertNotIn(first_mine, state.mines_set)
        self.assertIn(first_mine, state.revealed)

    def test_chord_reveal_opens_neighbors_when_flags_match_count(self):
        state = GameState(
            rows=3,
            cols=3,
            mines=1,
            mines_set={(0, 0)},
            revealed={(1, 1)},
            flagged={(0, 0)},
            counts=[
                [0, 1, 0],
                [1, 1, 0],
                [0, 0, 0],
            ],
        )

        reveal(state, 1, 1)

        self.assertIn((0, 1), state.revealed)
        self.assertIn((2, 2), state.revealed)
        self.assertTrue(state.win)

    def test_public_payload_exposes_remaining_mines_and_loss_mines(self):
        state = GameState(
            rows=2,
            cols=2,
            mines=1,
            mines_set={(0, 0)},
            revealed={(0, 0)},
            flagged={(1, 1)},
            counts=[[0, 1], [1, 1]],
            over=True,
            win=False,
        )

        payload = to_public_payload(state)

        self.assertEqual(payload["remainingMines"], 0)
        self.assertTrue(payload["grid"][0][0]["mine"])
        self.assertTrue(payload["grid"][0][0]["revealed"])
