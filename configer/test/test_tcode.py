from pprint import pprint

from click.testing import CliRunner
from logsmal import loglevel
from pytest import mark

from front_cli import tcodp, tcodi, tcodu
from helpful_test import ОткатываемыйФайл
from helpful_test import ПрочитанныйТестовыйФайл
from inout_helpful import enum_tcode
from logic_tcode import tcodeLogic


class Test_Back:
    @mark.parametrize(
        ("infile", "outfile", "name", "lang"),
        [
            (
                    enum_tcode.print_conf.value,
                    enum_tcode.print_tests.value,
                    "sum",
                    "py",
            )
        ]
    )
    def test_print(self, infile, outfile, name, lang):
        res = tcodeLogic.print(name_command=name, lang=lang, _path_conf=infile.path)
        # outfile.обновить(res)
        assert res + '\n' == outfile.текст

    @mark.parametrize(
        ("infile_conf", "insert_text", "outfile", "name", "lang"),
        [
            (
                    enum_tcode.print_conf.value,
                    enum_tcode.in_infile.value,
                    enum_tcode.out_infile.value,
                    "sum",
                    "py",
            )
        ]
    )
    def test_infile(self, infile_conf, insert_text, outfile, name, lang):
        res = tcodeLogic.infile(insert_text=insert_text.текст, _path_conf=infile_conf.path)
        # outfile.обновить(res)
        assert res == outfile.текст

    @mark.parametrize(
        ("_path_conf", "upfile_text", "outfile", "name", "lang"),
        [
            (
                    enum_tcode.in_upfile.value,
                    enum_tcode.out_infile.value,
                    enum_tcode.out_upfile.value,
                    "sum",
                    "py",
            )
        ]
    )
    def test_upfile(self, _path_conf, upfile_text, outfile, name, lang):
        res = tcodeLogic.upfile(from_update_text=upfile_text.текст, _path_conf=_path_conf.path)
        # outfile.обновить(res)
        assert res == outfile.текст


class Test_CLI:

    @mark.parametrize(
        ("name_command", "lang", 'path_conf', 'T_check_data'),
        [
            (
                    'sum',
                    ['-l', 'py'],
                    ['-c', enum_tcode.print_conf.value.path],
                    enum_tcode.print_tests.value.текст
            ),
            (
                    'sum',
                    ['-l', 'py, js, cpp'],
                    ['-c', enum_tcode.print_conf.value.path],
                    enum_tcode.print_tests_many_lang.value.текст
            ),
        ]
    )
    def test_print_(self, name_command, lang, path_conf, T_check_data):
        """
        python ./configer/main.py tcode print sum -l "cpp, py" -c ./configer/test/in/public/tcode/print_conf.py;


        :param name_command:
        :param lang:
        :param path_conf:
        :return:
        """
        loglevel.required_level = 21
        runner = CliRunner()
        result = runner.invoke(tcodp, [name_command, *lang, *path_conf])
        assert result.exit_code == 0, result.output
        assert result.output == T_check_data
        print(result.output)

    @mark.parametrize(
        ("type_file", "insert_file", 'backup_file', 'check_file', 'path_conf'),
        [
            (
                    ['-t', 'py, md, json'],
                    './in/public/tcode/',
                    ОткатываемыйФайл("./in/public/tcode/infile.py", None),
                    enum_tcode.out_infile.value,
                    ['-c', enum_tcode.print_conf.value.path],
            ),
        ]
    )
    def test_infile(self, type_file, insert_file: str, check_file: ПрочитанныйТестовыйФайл,
                    backup_file: ОткатываемыйФайл,
                    path_conf):
        runner = CliRunner()
        with backup_file:
            result = runner.invoke(tcodi, [insert_file, *type_file, *path_conf])
            assert result.exit_code == 0, result.output
            assert backup_file.прочесть() == check_file.текст
            print(backup_file.прочесть())

    @mark.parametrize(
        ("type_file", "path_search", 'check_file', 'path_conf'),
        [
            (
                    ['-t', 'py, md, json'],
                    ОткатываемыйФайл('./in/public/tcode/upfile.py', None),
                    enum_tcode.out_upfile.value,
                    ['-c', enum_tcode.in_upfile.value.path],
            ),
        ]
    )
    def test_upfile(self, type_file: set[str], path_search: ОткатываемыйФайл, check_file: ПрочитанныйТестовыйФайл,
                    path_conf: str):
        runner = CliRunner()
        with path_search:
            result = runner.invoke(tcodu, [path_search.path, *type_file, *path_conf])
            assert result.exit_code == 0, pprint(result.output)
            assert path_search.прочесть() == check_file.текст
            print(path_search.прочесть())
