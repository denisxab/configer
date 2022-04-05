import enum

from helpful_test import ТестовыйФайл, ПрочитанныйТестовыйФайл


class enum_parseconf(enum.Enum):
    conf = ТестовыйФайл(
        "./in/public/parseconf/conf.py",
        '024709589ad1f63956ffacbf7ad22215ef8d5844277a9940790d737521167b62')

    out_env = ПрочитанныйТестовыйФайл(
        "./out/public/parseconf/__env.env",
        '3035b69d8a9cc2d557ec49aef88d20982c102740a51e884ed0400956c0f1793f')

    rewrite_conf = ТестовыйФайл(
        "./in/public/parseconf/rewrite_conf.py",
        '365d721bdfbd660741e85bc47f6d5e7dc2d59a047a24783b61b23bb1279a3dd8')

    dont_full_template = ТестовыйФайл(
        './in/f_parse_1.py',
        '36a8ff6d78412ad1f066f94eeb1fc4f34baca307f8994aaed25e2d69aec5dc1e')


class enum_hideconf(enum.Enum):
    conf = ТестовыйФайл(
        "./in/public/hideconf/conf.py",
        'b4e3c0867be460c867c4abb2e1f35b44831d37bccf829e453d52963c74799bf3')

    conf_pub = ПрочитанныйТестовыйФайл(
        "./out/public/hideconf/conf_pub.py",
        '06d71858d0ec41867f728b9e299f5380ab63c5ca5fa054bb19d3afce34026fd5')


class enum_tcode(enum.Enum):
    print_conf = ТестовыйФайл(
        "./in/public/tcode/print_conf.py",
        'd3076e37cdb3aae9e06b5c595e582a36feed4803b4bac3c359d6b3d1289821aa')

    print_tests = ПрочитанныйТестовыйФайл(
        "./out/public/tcode/print_tests.py",
        'eaf5db27d8944b222e3c082e86a6580a5eab4da6581e563494fc4897c7660d02')
    print_tests_many_lang = ПрочитанныйТестовыйФайл(
        "./out/public/tcode/print_tests_many_lang.txt",
        'a34ca875fab53de183a5d72b2baf7059dc9068cdf837a242560705c9960323cb')
    in_infile = ПрочитанныйТестовыйФайл(
        "./in/public/tcode/infile.py",
        '78d58bfbb81f8c9d9f3fa869c1b98674b4108e99cab8b72e0e558f961314e254')
    out_infile = ПрочитанныйТестовыйФайл(
        "./out/public/tcode/infile.py",
        '78d58bfbb81f8c9d9f3fa869c1b98674b4108e99cab8b72e0e558f961314e254')

    in_upfile = ТестовыйФайл(
        "./in/public/tcode/upfile_conf.py",
        'e51ed85fc75b1d8097c8f9690a3b764515ef42c622d114390a051210d410c81a')
    out_upfile = ПрочитанныйТестовыйФайл(
        "./out/public/tcode/upfile.py",
        '63517c56555433a287c232236c96c24925a7a06be2f9378b2f9d094c790f61ec')


class enum_ttext(enum.Enum):
    conf = ТестовыйФайл(
        "./in/public/ttext/conf.py",
        'e9f2e85f30345b764db5b976aa0fc43b67f1c5230a592c3b4f4b502b2ce9ca20')
    template = ПрочитанныйТестовыйФайл(
        "./out/public/ttext/template.py",
        '3bb9b613fd13d95f995a637f61fab96154401cfaaffe8bd4525bfaa0a9b7f3ff')
