import logging

from sg import sg


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)s\t%(message)s")
    sg.prepare_site()
    sg.copy_static_content()
    sg.generate_site()


if __name__ == '__main__':
    main()
