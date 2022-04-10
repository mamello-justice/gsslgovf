#!/usr/bin/python3
import os
import sys
from typing import Tuple


def get_value_in_brackets(line: str) -> str:
    return line[line.find("{") + 1 : line.rfind("}")]


def get_author_last_name(author: Tuple[str]) -> str:
    return author[0]


def get_author_last_name_with_initial(author: Tuple[str]) -> str:
    return f"{author[1][0]}. {author[0]}"


def main():
    if len(sys.argv) != 2:
        print("Usage:\n\t$ bib2tex.py path/to/references.bib")
        exit(1)

    file = sys.argv[1]
    if not os.path.isfile(file):
        print(f"Not a valid file {file}")
        exit(1)

    with open(file) as bibtex:
        bibtex = bibtex.readlines()
        r = bibtex
        i = 0
        while i < len(r):
            line = r[i].strip()
            if not line:
                i += 1
            if "@" == line[0]:
                code = line.split("{")[-1][:-1]
                title = (
                    venue
                ) = volume = number = pages = year = publisher = authors = None
                output_authors: list[Tuple[str, str]] = []
                i += 1
                while i < len(r) and "@" not in r[i]:
                    line = r[i].strip()
                    # print(line)
                    value = get_value_in_brackets(line)
                    if line.startswith("title"):
                        title = value
                    elif line.startswith("journal") or line.startswith("booktitle"):
                        venue = value
                    elif line.startswith("volume"):
                        volume = value
                    elif line.startswith("number"):
                        number = value
                    elif line.startswith("pages"):
                        pages = value
                    elif line.startswith("year"):
                        year = value
                    elif line.startswith("publisher"):
                        publisher = value
                    elif line.startswith("author"):
                        authors = value
                        for LastFirst in authors.split("and"):
                            lf = LastFirst.replace(" ", "").split(",")
                            if len(lf) != 2:
                                continue
                            output_authors.append(
                                (lf[0].capitalize(), lf[1].capitalize())
                            )
                    i += 1

                # Bibitem Code
                print("\\bibitem{%s}" % code)

                # Authors
                first_author = get_author_last_name(output_authors[0])
                if len(output_authors) == 1:
                    print(f"[{first_author} {year}]", end=" ")
                    print(output_authors[0] + ".", end=" ")
                else:
                    print(f"[{first_author} \emph{{et al}}. {year}]", end=" ")
                    print(
                        "{} and {}.".format(
                            ", ".join(
                                get_author_last_name_with_initial(_)
                                for _ in output_authors[:-1]
                            ),
                            get_author_last_name_with_initial(output_authors[-1]),
                        ),
                        end=" ",
                    )

                # Title

                if venue:
                    print(f"{title}.", end=" ")
                    print(
                        "\\emph{{{}}}.".format(
                            " ".join([_.capitalize() for _ in venue.split(" ")]),
                        ),
                        end=" ",
                    )
                    if volume:
                        print(f"{volume}", end="")
                    if volume and pages:
                        print(":", end="")
                    if pages:
                        print(f"{pages}", end="")

                # Publisher
                if publisher and not venue:
                    print(f"\\emph{{{title}}}.", end=" ")
                    print(f"{publisher}", end="")

                if year:
                    print(", {}".format(year))

                print()


if __name__ == "__main__":
    main()
