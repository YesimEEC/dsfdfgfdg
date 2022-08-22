'''
Tools for building firmware images.
'''
from asyncio import subprocess
from SCons.Script import Exit
from SCons.Script import File
from utils import get_kwarg_or_env
import os
import subprocess

def exists(env):
    return True


def __configure_firmware(env, kwargs):
    # Add the common modules
    libpath = get_kwarg_or_env(env, kwargs, 'LIBPATH')
    whole_libs = get_kwarg_or_env(env, kwargs, 'WHOLE_LIBS')

    # Add the chip-specific libraries.
    mcu = get_kwarg_or_env(env, kwargs, 'MCU')

    kwargs['LIBPATH'] = libpath
    kwargs['WHOLE_LIBS'] = whole_libs

def build_firmware(env, target, source, **kwargs):
    env.CompilationDbEntries(source, **kwargs)
    if env['ARCH'] != 'xtensa' and env['ARCH'] != 'x86':
        print('ARCH={} is not yet supported for building firmwares'
                .format(env['ARCH']))
        Exit(2)

    # Add FW components that we want to use
    source = env.Split(source)

    # Add the MCU specific settings
    mcu = get_kwarg_or_env(env, kwargs, 'MCU')
    test = get_kwarg_or_env(env, kwargs, 'TEST')
    if mcu == 'ESP32':
        __configure_firmware(env, kwargs)
    else:
        if test != 'TRUE':
            # TODO: Add support for more MCUs
            print('MCU={} is not yet supported for building firmwares'
                    .format(mcu))
            Exit(2)

    # Request the target to be built
    result = env.Program(target, source, **kwargs)
    return result

def build_firmware_component(env, target, source, **kwargs):
    env.CompilationDbEntries(source, **kwargs)
    obj = []
    libname = ''
    for src in source:
        path = os.path.dirname(src)
        path = path.partition('components/')[2]
        libname = path.partition('/')[0]
        obj_path = os.path.join("$BUILD_DIR", path)
        obj_path = os.path.join(obj_path, os.path.basename(src))
        obj_path = os.path.splitext(obj_path)[0] + '.o'
        obj.append(env.Object(obj_path, src, **kwargs))
    target = os.path.join(target, libname)
    return env.Library(target, obj, **kwargs)

def generate_cert_bundle(env):
    bundle_path = os.path.join('/home/yesim/Desktop/Luminula/build/blink', 'x509_crt_bundle')
    if os.path.isfile(env.subst(bundle_path)):
        return
    
    default_crt_dir = '/opt/esp/esp-idf/components/mbedtls/esp_crt_bundle'

    cmd = [os.path.join(default_crt_dir, 'gen_crt_bundle.py')]
    crt_args=["--input"]
    crt_args.append(os.path.join(default_crt_dir,'cacrt_all.pem'))
    crt_args.append("-q")

    p = subprocess.Popen(cmd+crt_args, cwd='/home/yesim/Desktop/Luminula/build/blink')
    bundle_path = os.path.join('/home/yesim/Desktop/Luminula/build/blink', "x509_crt_bundle")


def generate(env):
    env.AddMethod(build_firmware, 'Firmware')
    env.AddMethod(build_firmware_component, 'FirmwareComponent')
    env.AddMethod(generate_cert_bundle, 'CertBundle')
