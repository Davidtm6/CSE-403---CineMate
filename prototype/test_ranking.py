import math
import unittest

from ranking import insertion_index


class RankingTests(unittest.TestCase):
    def test_all_positions_for_small_and_large_lists(self):
        for size in range(129):
            ranked = [f"film-{i}" for i in range(size)]
            for desired in range(size + 1):
                comparisons = []

                def prefer_new(new_movie, opponent):
                    comparisons.append(opponent)
                    return desired <= int(opponent.split("-")[1])

                with self.subTest(size=size, position=desired):
                    original = ranked.copy()
                    actual = insertion_index(ranked, "new-film", prefer_new)
                    self.assertEqual(actual, desired)
                    self.assertEqual(ranked, original)
                    self.assertLessEqual(
                        len(comparisons), math.ceil(math.log2(size + 1))
                    )

    def test_duplicate_is_rejected_before_comparison(self):
        with self.assertRaises(ValueError):
            insertion_index(["Arrival"], "Arrival", lambda *_: self.fail())

    def test_cancel_leaves_list_unchanged(self):
        ranked = ["A", "B", "C"]

        def cancel(*_):
            raise KeyboardInterrupt

        with self.assertRaises(KeyboardInterrupt):
            insertion_index(ranked, "D", cancel)
        self.assertEqual(ranked, ["A", "B", "C"])


if __name__ == "__main__":
    unittest.main()
