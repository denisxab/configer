import pytest
from click.testing import CliRunner

from front_cli import hideconf
from helpful_test import ОткатываемыйФайл, ТестовыйФайл
from inout_helpful import enum_hideconf
from logic_hideconf import hideconfLogic


class Test_Back:

    @pytest.mark.parametrize(
        ("_path_conf", "outfile"),
        [
            (
                    enum_hideconf.conf.value,
                    enum_hideconf.conf_pub.value,
            )
        ]
    )
    def test_hideconf(self, _path_conf, outfile):
        res = hideconfLogic._parse_config(_path_conf.path)
        # outfile.обновить(res[0][1])
        assert res == outfile.текст


class Test_CLI:

    @pytest.mark.parametrize(
        ("path_conf", "conf_pub", "check_file",),
        [
            (
                    enum_hideconf.conf.value,
                    ОткатываемыйФайл('./conf_pub.py', None),
                    enum_hideconf.conf_pub.value
            ),
        ]
    )
    def test_hideconf(self, path_conf: ТестовыйФайл, conf_pub, check_file):
        runner = CliRunner()
        with conf_pub:
            result = runner.invoke(hideconf, [path_conf.path, '-o', conf_pub.path])
            # assert result.exit_code == 0, result.output
            assert conf_pub.текст == check_file.текст
            print(conf_pub.текст)
