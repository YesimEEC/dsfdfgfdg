import build_config
import SCons
AddOption('--build_dir',
          dest='build_dir',
          action='store',
          type='string',
          default='build',
          help='Toplevel project directory where build outputs are stored')

AddOption('--toolchain-dir',
          dest='xtensa_toolchain',
          action='store',
          type='string',
          default='/opt/esp/tools/xtensa-esp32-elf/bin',
          help='Toolchain directory path in the system')

AddOption('--arch',
          dest='build_arch',
          action='store',
          type='string',
          default='xtensa',
          help='Build environment, can only be arm or x86')

# Local dictionary for command line options
cmd_options = {
    'build_dir' : GetOption('build_dir'),
    'xtensa_toolchain' : GetOption('xtensa_toolchain'),
    'build_arch' : GetOption('build_arch')
}

Help('''
    Luminula projesi icin build system:
    SCons icerisinde birden fazla target olabilir.

    Dokumantasyon, sistem testleri vb. bircok arac SCons
    uzerinden ayni repo' da toplanacak ve target olarak
    istenilen zaman build edilebilecektir.
    Butun target ciktilari build/bin klasorunde toplanir.

    SCons ile build edilen dosyalari silmek icin:
        scons -c


''', append = True)

blink_env = Environment(tools=['default',
                                'compilation_db',
                                'firmware',
                                'elftohex',
                        ])

# Configure environment
build_config.Blink(blink_env, cmd_options)

# Add SConscript files
blink_env.SConscript(dirs='blink', exports={'env': blink_env}, variant_dir='$BUILD_DIR')
default_builds = []
if blink_env['ARCH'] == 'xtensa':
    default_builds.extend([blink_env.Alias('blink-app')])

    blink_env.Default(default_builds)

if not COMMAND_LINE_TARGETS:
    Clean(default_builds, cmd_options['build_dir'])
