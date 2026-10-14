"""Explore Encore's binary insertion without accounts or external services."""

from collections.abc import Callable, Sequence


def insertion_index(
    ranked: Sequence[str], new_movie: str, prefer_new: Callable[[str, str], bool]
) -> int:
    """Return a position in a best-first list without modifying the input.

    The callback returns True when the new movie is preferred to its opponent.
    Answers must be consistent with the current list's order.
    """
    if new_movie in ranked:
        raise ValueError("This movie is already ranked.")
    low, high = 0, len(ranked)
    while low < high:
        middle = (low + high) // 2
        if prefer_new(new_movie, ranked[middle]):
            high = middle
        else:
            low = middle + 1
    return low


def ask_preference(new_movie: str, opponent: str) -> bool:
    while True:
        answer = input(
            f"Which do you prefer?\n  1. {new_movie}\n  2. {opponent}\n"
            "Choose 1 or 2 (q cancels): "
        ).strip().lower()
        if answer == "q":
            raise KeyboardInterrupt
        if answer in {"1", "2"}:
            return answer == "1"
        print("Please enter 1, 2, or q.")


def main() -> None:
    ranked = ["Spirited Away", "The Grand Budapest Hotel", "Arrival"]
    print("Encore ranking experiment — sample order, most preferred first.")
    while True:
        print("\nYour current ranking:")
        for position, movie in enumerate(ranked, 1):
            print(f"  {position}. {movie}")
        try:
            movie = input("\nAdd a watched movie (q exits): ").strip()
            if movie.lower() == "q":
                return
            if not movie:
                continue
            if movie.casefold() in {title.casefold() for title in ranked}:
                print("This movie is already ranked.")
                continue
            position = insertion_index(ranked, movie, ask_preference)
        except KeyboardInterrupt:
            print("\nComparison canceled; your ranking is unchanged.")
            continue
        except EOFError:
            return
        ranked.insert(position, movie)
        print(f"Added {movie} at position {position + 1}.")


if __name__ == "__main__":
    main()
