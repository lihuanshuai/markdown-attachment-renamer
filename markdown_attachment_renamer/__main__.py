import argparse

from .renamer import rename_attachments


def main():
    parser = argparse.ArgumentParser(description='Rename markdown attachments.')
    parser.add_argument(
        'file', metavar='FILE', type=str, nargs=1,
        help='path to markdown file'
    )
    args = parser.parse_args()
    path: str = args.file[0]
    rename_attachments(path)


if __name__ == "__main__":
    main()
