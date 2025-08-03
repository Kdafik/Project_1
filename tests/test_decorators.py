from src.decorators import log


def test_log(capsys):
    @log("log.txt")
    def func2(my_name):
        print(f"Hello, {my_name}!")

    name = "Alimad"
    func2(name)
    captured = capsys.readouterr()
    assert captured.out == f"Hello, {name}!\n"

    @log()
    def func1(a, b):
        return a + b

    print(func1(1, 2))
    captured = capsys.readouterr()
    assert captured.out == "3\n"
