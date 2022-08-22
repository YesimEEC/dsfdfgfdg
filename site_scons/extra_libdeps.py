# The function setup_environment adds to your environment the ability to link
# to static libraries with --whole-archive (WHOLE_LIBS) or --start-group
# (GROUPED_LIBS)and still have automatic dependency tracking for those
# libraries.

import SCons.Scanner

def _make_nodes(strings, env):
    if not strings:
        return []

    result = []
    for string in strings:
        result.append(env.File(env.subst(string)).abspath)

    return result

def setup_environment(env):
    env['LINK_WHOLE_LIBS'] = '-Wl,--whole-archive $_WHOLELIBFLAGS -Wl,--no-whole-archive'
    env['_WHOLELIBFLAGS'] = '${_concat(LIBLINKPREFIX, WHOLE_LIBS, LIBLINKSUFFIX, __env__)}'
    env['_make_nodes'] = _make_nodes
    env['_WHOLELIBFLAGS'] += ' ${_make_nodes(WHOLE_LIBS_ABS, __env__)}'

    linkcom = env['LINKCOM']
    index = linkcom.find('$SOURCES')
    new_linkcom = linkcom[:index] + '$LINK_WHOLE_LIBS ' + linkcom[index:]
    env['LINKCOM'] = new_linkcom

    env['LINKCOM'] += ' -Wl,--start-group $_GROUPEDLIBFLAGS -Wl,--end-group'
    env['_GROUPEDLIBFLAGS'] = '${_concat(LIBLINKPREFIX, GROUPED_LIBS, LIBLINKSUFFIX, __env__)}'
    env['_GROUPEDLIBFLAGS'] += ' ${_make_nodes(GROUPED_LIBS_ABS, __env__)}'

    try:
        update_scanner(env['BUILDERS']['Program'])
    except:
        pass

def update_scanner(builder):

    old_scanner = builder.target_scanner

    if old_scanner:
        path_function = old_scanner.path_function
        def new_scanner(node, env, path=()):
            old_libs = env.get('LIBS', [])
            new_libs = old_libs.copy()
            new_libs.extend(env.get('WHOLE_LIBS', []))
            new_libs.extend(env.get('GROUPED_LIBS', []))
            env['LIBS'] = new_libs
            result = old_scanner.function(node, env, path)
            result.extend(_make_nodes(env.get('WHOLE_LIBS_ABS', []), env))
            result.extend(_make_nodes(env.get('GROUPED_LIBS_ABS', []), env))
            env['LIBS'] = old_libs
            return result
    else:
        raise ValueError('Expected a builder with a scanner installed')

    new_target_scanner = SCons.Scanner.Scanner(function=new_scanner,
            path_function=path_function)
    builder.target_scanner = new_target_scanner