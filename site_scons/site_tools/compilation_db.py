'''
Tools for building the compilation db.
'''
import importlib
import json
import os
import SCons

def exists(env):
    return True

class _CompilationDbEntryNode(SCons.Node.Python.Value):
    def __init__(self, value):
        super().__init__(value)

    def is_up_to_date(self):
        return False

    def get_csig(self):
        try:
            return self.ninfo.csig
        except AttributeError:
            pass

        contents = self.get_text_contents()
        csig = SCons.Util.MD5signature(contents)
        self.get_ninfo().csig = csig

        return csig

class _CompilationDbNode(SCons.Node.FS.File):
    def __init__(self, name, directory, fs):
        super().__init__(name, directory, fs)
        self._regenerated = False

    def built(self):
        super().built()
        self._regenerated = True

    def changed_content(self, target, prev_ni):
        if self._regenerated:
            return True
        else:
            return super().changed_content(target, prev_ni)

def compilation_db_entry_action_factory(command_string):
    def compilation_db_entry_action(target, source, env):
        command = env.subst(
                    command_string,
                    source=source[0].srcnode(),
                    target=source[0].target_from_source(
                        env.subst('$OBJPREFIX'), env.subst('$OBJSUFFIX')
                    )
                )
        for remove_option in env['COMPILATION_DB_REMOVE_OPTIONS']:
            command = command.replace(remove_option, '')
        entry = {
            'directory': env.Dir('#').get_abspath() + os.sep,
            'command': command,
            'file': source[0].srcnode().get_abspath()
        }

        target[0].write(entry)

    return compilation_db_entry_action

def compilation_db_entry_emitter_factory(command_string):
    def compilation_db_entry_emitter(target, source, env):
        value = str(target[0]) + ' ' + env.subst(command_string)
        db_entry = _CompilationDbEntryNode(value)
        env['COMPILATION_DB_ENTRIES'].append(db_entry)

        return (db_entry, source)

    return compilation_db_entry_emitter

def compilation_db_entries(env, sources, **kwargs):
    sources = env.Split(sources)
    sources = env.arg2nodes(sources)
    entries = []
    for source in sources:
        if source.suffix != '.o':
            entries.append(env._CompilationDbEntry(source, **kwargs))

    return entries

def compilation_db_write_action(target, source, env):
    entries = [entry.read() for entry in env['COMPILATION_DB_ENTRIES']]

    with open(str(target[0]), 'w') as f:
        json.dump(entries, f, indent=4, sort_keys=True)

def scan_entries(node, env, path):
    return env['COMPILATION_DB_ENTRIES']

def compilation_db_create(env, target):
    db = env._CompilationDbFull(target, [])
    return db

def generate(env):
    env.SetDefault(COMPILATION_DB_ENTRIES=[])

    actions = dict()
    emitters = dict()

    for suffix in SCons.Tool.cxx.CXXSuffixes:
        actions[suffix] = SCons.Action.Action(
            compilation_db_entry_action_factory('$CXXCOM'), None
        )
        emitters[suffix] = compilation_db_entry_emitter_factory('$CXXCOM')
    for suffix in SCons.Tool.cc.CSuffixes:
        actions[suffix] = SCons.Action.Action(
            compilation_db_entry_action_factory('$CCCOM'), None
        )
        emitters[suffix] = compilation_db_entry_emitter_factory('$CCCOM')
    # Need to add '.S' because the line in as.py adding it doesn't seem to be execute
    as_suffixes = SCons.Tool.asm.ASSuffixes
    as_suffixes.append('.S')
    for suffix in as_suffixes:
        actions[suffix] = SCons.Action.Action(
            compilation_db_entry_action_factory('$ASCOM'), None
        )
        emitters[suffix] = compilation_db_entry_emitter_factory('$ASCOM')

    env['BUILDERS']['_CompilationDbEntry'] = SCons.Builder.Builder(
        action=actions,
        src_builder=['CFile', 'CXXFile'],
        suffix='.entry',
        single_source=True,
        emitter=emitters,
    )
    env.AddMethod(compilation_db_entries, 'CompilationDbEntries')

    command_string = 'Building compilation database $TARGET'
    env['BUILDERS']['_CompilationDbFull'] = SCons.Builder.Builder(
        action=SCons.Action.Action(compilation_db_write_action, command_string),
        target_scanner=SCons.Scanner.Scanner(function=scan_entries, node_class=None),
        target_factory=lambda name: env.fs._lookup(name, None, _CompilationDbNode, 1)
    )
    env.AddMethod(compilation_db_create, 'CompilationDb')
