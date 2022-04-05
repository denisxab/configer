from click.testing import CliRunner
from logsmal import loglevel
from pytest import mark

from front_cli import ttext
from inout_helpful import enum_ttext
from logic_ttext import ttextLogic


class Test_Back:

    @mark.parametrize(
        ("path_conf", "T_check_file", "name_command", "kwargs"),
        [
            (
                    enum_ttext.conf.value,
                    enum_ttext.template.value,
                    "pytest",
                    {
                        "args": "a, b, c",
                        "name": "sum",
                        "doc": "Тестирование суммирования",
                    }

            )
        ]
    )
    def test_ttext(self, path_conf, T_check_file, name_command, kwargs):
        res = ttextLogic._parse_module(name_command=name_command,
                                       overload_kwargs=kwargs,
                                       path_conf=path_conf.path)
        assert res[1] + '\n' == T_check_file.текст
        print(res)


class Test_CLI:

    @mark.parametrize(
        ("path_conf", "T_check_file", "name_command", "kwargs"),
        [
            (
                    ['-c', enum_ttext.conf.value.path],
                    enum_ttext.template.value,
                    "pytest",
                    [
                        '-k', 'name=sum',
                        '-k', 'doc=Тестирование суммирования',
                        '-k', 'args=a, b, c'
                    ],
            )
        ]
    )
    def test_ttext(self, path_conf, T_check_file, name_command, kwargs):
        loglevel.required_level = 21
        runner = CliRunner()
        result = runner.invoke(ttext, [name_command, *path_conf, *kwargs])
        assert result.exit_code == 0, result.output
        assert result.output == T_check_file.текст
