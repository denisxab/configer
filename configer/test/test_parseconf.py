from re import escape

from click.testing import CliRunner
from pytest import raises, mark

from configer import parseconfLogic
from front_cli import parseconf
from helpful_test import ОткатываемыйФайл, ТестовыйФайл
from inout_helpful import enum_parseconf


class Test_Bakend:
    @mark.parametrize(
        ("_path_conf", "outfile"),
        [
            (
                    enum_parseconf.conf.value,
                    enum_parseconf.out_env.value,
            )
        ]
    )
    def test_parseconf(self, _path_conf, outfile):
        res = parseconfLogic._parse_module(_path_conf.path)
        # outfile.обновить(res[0][1])
        assert res[0][1] == outfile.текст

    @mark.parametrize(
        ("_path_conf",),
        [
            (
                    enum_parseconf.rewrite_conf.value,
            )
        ]
    )
    def test_parseconf_rewrite(self, _path_conf):
        res = parseconfLogic._parse_module(_path_conf.path)
        assert res[0] is False
        assert res[1][0] == '../gitignore'

    @mark.parametrize(("_path_conf", "match_except"),
                      [
                          (
                                  enum_parseconf.dont_full_template.value,
                                  escape("admin_panel"),
                          ),
                      ])
    def test_неполный_шаблон(self, _path_conf, match_except):
        """
        Тестирование ситуации когда в шаблоне ожидается ключ, но его нет в словаре

        """
        # В контексте должна возникнуть указанная ошибка
        with raises(KeyError, match=match_except):
            # Проверка создания готового шаблона
            parseconfLogic._parse_module(_path_conf.path)


class Test_CLI:
    @mark.parametrize(
        ("path_conf", "_env_file", 'check_file'),
        [
            (
                    enum_parseconf.conf.value,
                    ОткатываемыйФайл('./__env.env', None),
                    enum_parseconf.out_env.value
            ),
        ]
    )
    def test_parseconf(self, path_conf: ТестовыйФайл, _env_file, check_file):
        runner = CliRunner()
        with _env_file:
            result = runner.invoke(parseconf, [path_conf.path])
            assert result.exit_code == 0, result.output
            assert _env_file.текст == check_file.текст
