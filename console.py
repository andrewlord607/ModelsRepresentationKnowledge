from Parser.Parser import Parser


if __name__ == '__main__':
    parser = Parser()
    while 1 == 1:
        input_str = input("#: ")
        print(parser.parse_input(input_str))


