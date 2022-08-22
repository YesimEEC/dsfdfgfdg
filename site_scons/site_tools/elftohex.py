import SCons

def generate(env):

    env.SetDefault(
        ELFTOHEX='$OBJCOPY --gap-fill 255 -O ihex $SOURCE $TARGET'
    )

    env['BUILDERS']['ElfToHex'] = SCons.Builder.Builder(
        action=SCons.Action.Action('$ELFTOHEX'),
        single_source =True,
        suffix='.hex'
    )

def exists(env):
    return True
