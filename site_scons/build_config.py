import os
from tty import CFLAG
import extra_libdeps

def Common(env, cmd_options):
    extra_libdeps.setup_environment(env)

    env['PROJECT_DIR'] = os.getcwd()
    env['BUILD_BASE'] = '#' + cmd_options['build_dir']
    env['BUILD_DIR'] = '#' + cmd_options['build_dir']

    env['ARCH'] = cmd_options['build_arch']

    if env['ARCH'] == 'xtensa':

        env.Append(ASFLAGS=['-mlongcalls'])

        env.Append(CFLAGS=['-std=gnu99'])

        env.Append(CCFLAGS=[
                            '-mlongcalls',
                            '-Wno-frame-address',
                            '-ffunction-sections',
                            '-fdata-sections',
                            '-Wall',
                            '-Werror=all',
                            '-Wno-error=unused-function',
                            '-Wno-error=unused-variable',
                            '-Wno-error=deprecated-declarations',
                            '-Wno-unused-parameter',
                            '-Wno-sign-compare',
                            '-ggdb',
                            '-Og',
                            '-fstrict-volatile-bitfields',
                            '-Wno-error=unused-but-set-variable',
                            '-fno-jump-tables',
                            '-fno-tree-switch-conversion',
                            '-fno-exceptions',
                            '-Wno-old-style-declaration',
                            ])

        env.Append(CXXFLAGS=[
                            '-std=gnu++11',
                            '-fno-rtti',
                            ])

        env.Append(CPPDEFINES=[ 'ESP32',
                                'PROJECT_NAME=\\\"espidf-blink\\\"', 
                                'PROJECT_VER=\\\"1\\\"', 'IDF_VER=\\\"4.4.1\\\"', 
                                '_POSIX_READER_WRITER_LOCKS', '_GNU_SOURCE',
                                'ESP_PLATFORM',
                                ('F_CPU', '$BOARD_F_CPU'),
                                'HAVE_CONFIG_H',
                                ('MBEDTLS_CONFIG_FILE', '\\"mbedtls/esp_config.h\\"')
                            ])

        env.Append(LINKFLAGS=[
                            ])
        
        env.Append(ASFLAGS=env.get("CFLAGS", [])[:])

        env.PrependENVPath('PATH', cmd_options['xtensa_toolchain'])

        env['AR'] = 'xtensa-esp32-elf-ar'
        env['AS'] = 'xtensa-esp32-elf-gcc'
        env['CC'] = 'xtensa-esp32-elf-gcc'
        env['CXX'] = 'xtensa-esp32-elf-g++'
        env['LINK'] = 'xtensa-esp32-elf-gcc'
        env['RANLIB'] = 'xtensa-esp32-elf-ranlib'
        env['OBJCOPY'] = 'xtensa-esp32-elf-objcopy'
        env['RANLIB'] = 'xtensa-esp32-elf-ranlib'
        env['SIZETOOL'] = 'xtensa-esp32-elf-size'

        env.Append(CPPPATH = ['/opt/esp/esp-idf/components/esp_ringbuf/include',
                              '#blink',
                              '/opt/esp/esp-idf/components/newlib/platform_include',
                              '/opt/esp/esp-idf/components/freertos/include',
                              '/opt/esp/esp-idf/components/freertos/include/esp_additions/freertos',
                              '/opt/esp/esp-idf/components/freertos/port/xtensa/include',
                              '/opt/esp/esp-idf/components/freertos/include/esp_additions',
                              '/opt/esp/esp-idf/components/freertos/port/xtensa/include/freertos',
                              '/opt/esp/esp-idf/components/freertos/port/priv_include',
                              '/opt/esp/esp-idf/components/freertos/include/freertos',
                              '/opt/esp/esp-idf/components/esp_hw_support/include',
                              '/opt/esp/esp-idf/components/esp_hw_support/include/soc',
                              '/opt/esp/esp-idf/components/esp_hw_support/include/soc/esp32',
                              '/opt/esp/esp-idf/components/esp_hw_support/port/esp32',
                              '/opt/esp/esp-idf/components/esp_hw_support/port/esp32/private_include',
                              '/opt/esp/esp-idf/components/esp_hw_support/port/include',
                              '/opt/esp/esp-idf/components/heap/include',
                              '/opt/esp/esp-idf/components/log/include',
                              '/opt/esp/esp-idf/components/lwip/include/apps',
                              '/opt/esp/esp-idf/components/lwip/include/apps/sntp',
                              '/opt/esp/esp-idf/components/lwip/lwip/src/include',
                              '/opt/esp/esp-idf/components/lwip/port/esp32/include',
                              '/opt/esp/esp-idf/components/lwip/port/esp32/include/arch',
                              '/opt/esp/esp-idf/components/soc/include',
                              '/opt/esp/esp-idf/components/soc/esp32',
                              '/opt/esp/esp-idf/components/soc/esp32/include',
                              '/opt/esp/esp-idf/components/hal/esp32/include',
                              '/opt/esp/esp-idf/components/hal/include',
                              '/opt/esp/esp-idf/components/hal/platform_port/include',
                              '/opt/esp/esp-idf/components/esp_rom/include',
                              '/opt/esp/esp-idf/components/esp_rom/include/esp32',
                              '/opt/esp/esp-idf/components/esp_rom/esp32',
                              '/opt/esp/esp-idf/components/esp_common/include',
                              '/opt/esp/esp-idf/components/esp_system/include',
                              '/opt/esp/esp-idf/components/esp_system/port/soc',
                              '/opt/esp/esp-idf/components/esp_system/port/public_compat',
                              '/opt/esp/esp-idf/components/esp_system/port/include',
                              '/opt/esp/esp-idf/components/esp32/include',
                              '/opt/esp/esp-idf/components/xtensa/include',
                              '/opt/esp/esp-idf/components/xtensa/esp32/include',
                              '/opt/esp/esp-idf/components/driver/include',
                              '/opt/esp/esp-idf/components/driver/esp32/include',
                              '/opt/esp/esp-idf/components/driver/include/driver',
                              '/opt/esp/esp-idf/components/esp_pm/include',
                              '/opt/esp/esp-idf/components/efuse/include',
                              '/opt/esp/esp-idf/components/efuse/esp32/include',
                              '/opt/esp/esp-idf/components/vfs/include',
                              '/opt/esp/esp-idf/components/esp_wifi/include',
                              '/opt/esp/esp-idf/components/esp_event/include',
                              '/opt/esp/esp-idf/components/esp_event/private_include',
                              '/opt/esp/esp-idf/components/esp_netif/include',
                              '/opt/esp/esp-idf/components/esp_netif/private_include',
                              '/opt/esp/esp-idf/components/esp_netif/lwip',
                              '/opt/esp/esp-idf/components/esp_eth/include',
                              '/opt/esp/esp-idf/components/tcpip_adapter/include',
                              '/opt/esp/esp-idf/components/esp_phy/include',
                              '/opt/esp/esp-idf/components/esp_phy/esp32/include',
                              '/opt/esp/esp-idf/components/esp_ipc/include',
                              '/opt/esp/esp-idf/components/app_trace/include',
                              '/opt/esp/esp-idf/components/app_trace/port/include',
                              '/opt/esp/esp-idf/components/esp_timer/include',
                              '/opt/esp/esp-idf/components/esp_timer/private_include',
                              '/opt/esp/esp-idf/components/mbedtls/port/include',
                              '/opt/esp/esp-idf/components/mbedtls/mbedtls/include',
                              '/opt/esp/esp-idf/components/mbedtls/esp_crt_bundle/include',
                              '/opt/esp/esp-idf/components/app_update/include',
                              '/opt/esp/esp-idf/components/spi_flash/include',
                              '/opt/esp/esp-idf/components/bootloader_support/include',
                              '/opt/esp/esp-idf/components/bootloader_support/include_bootloader',
                              '/opt/esp/esp-idf/components/nvs_flash/include',
                              '/opt/esp/esp-idf/components/pthread/include',
                              '/opt/esp/esp-idf/components/esp_gdbstub/include',
                              '/opt/esp/esp-idf/components/esp_gdbstub/xtensa',
                              '/opt/esp/esp-idf/components/esp_gdbstub/esp32',
                              '/opt/esp/esp-idf/components/esp_gdbstub/private_include',
                              '/opt/esp/esp-idf/components/espcoredump/include',
                              '/opt/esp/esp-idf/components/espcoredump/include/port/xtensa',
                              '/opt/esp/esp-idf/components/espcoredump/include_core_dump',
                              '/opt/esp/esp-idf/components/espcoredump/include_core_dump/port/xtensa',
                              '/opt/esp/esp-idf/components/wpa_supplicant/include',
                              '/opt/esp/esp-idf/components/wpa_supplicant/port/include',
                              '/opt/esp/esp-idf/components/wpa_supplicant/esp_supplicant/include',
                              '/opt/esp/esp-idf/components/ieee802154/include',
                              '/opt/esp/esp-idf/components/console',
                              '/opt/esp/esp-idf/components/asio/asio/asio/include',
                              '/opt/esp/esp-idf/components/asio/port/include',
                              '/opt/esp/esp-idf/components/cbor/port/include',
                              '/opt/esp/esp-idf/components/unity/include',
                              '/opt/esp/esp-idf/components/unity/unity/src',
                              '/opt/esp/esp-idf/components/cmock/CMock/src',
                              '/opt/esp/esp-idf/components/coap/port/include',
                              '/opt/esp/esp-idf/components/coap/libcoap/include',
                              '/opt/esp/esp-idf/components/nghttp/port/include',
                              '/opt/esp/esp-idf/components/nghttp/nghttp2/lib/includes',
                              '/opt/esp/esp-idf/components/esp-tls', 
                              '/opt/esp/esp-idf/components/esp-tls/esp-tls-crypto',
                              '/opt/esp/esp-idf/components/esp-tls/private_include',
                              '/opt/esp/esp-idf/components/esp_adc_cal/include',
                              '/opt/esp/esp-idf/components/esp_hid/include',
                              '/opt/esp/esp-idf/components/esp_hid/private',
                              '/opt/esp/esp-idf/components/tcp_transport/include',
                              '/opt/esp/esp-idf/components/esp_http_client/include',
                              '/opt/esp/esp-idf/components/esp_http_client/lib/include',
                              '/opt/esp/esp-idf/components/esp_http_server/include',
                              '/opt/esp/esp-idf/components/esp_http_server/src/port/esp32',
                              '/opt/esp/esp-idf/components/esp_http_server/src/util',
                              '/opt/esp/esp-idf/components/esp_https_ota/include',
                              '/opt/esp/esp-idf/components/esp_lcd/include',
                              '/opt/esp/esp-idf/components/esp_lcd/interface',
                              '/opt/esp/esp-idf/components/protobuf-c/protobuf-c',
                              '/opt/esp/esp-idf/components/protocomm/include/common',
                              '/opt/esp/esp-idf/components/protocomm/include/security',
                              '/opt/esp/esp-idf/components/protocomm/include/transports',
                              '/opt/esp/esp-idf/components/protocomm/proto-c',
                              '/opt/esp/esp-idf/components/mdns/include',
                              '/opt/esp/esp-idf/components/esp_local_ctrl/include',
                              '/opt/esp/esp-idf/components/esp_local_ctrl/proto-c',
                              '/opt/esp/esp-idf/components/sdmmc/include',
                              '/opt/esp/esp-idf/components/esp_serial_slave_link/include',
                              '/opt/esp/esp-idf/components/esp_serial_slave_link/include/esp_serial_slave_link',
                              '/opt/esp/esp-idf/components/esp_websocket_client/include',
                              '/opt/esp/esp-idf/components/expat/expat/expat/lib',
                              '/opt/esp/esp-idf/components/expat/port/include',
                              '/opt/esp/esp-idf/components/wear_levelling/include',
                              '/opt/esp/esp-idf/components/fatfs/diskio',
                              '/opt/esp/esp-idf/components/fatfs/vfs',
                              '/opt/esp/esp-idf/components/fatfs/src',
                              '/opt/esp/esp-idf/components/freemodbus/common/include',
                              '/opt/esp/esp-idf/components/freemodbus/modbus/include',
                              '/opt/esp/esp-idf/components/freemodbus/port',
                              '/opt/esp/esp-idf/components/freemodbus/modbus/rtu',
                              '/opt/esp/esp-idf/components/freemodbus/modbus/ascii',
                              '/opt/esp/esp-idf/components/freemodbus/modbus/tcp',
                              '/opt/esp/esp-idf/components/freemodbus/serial_slave/port',
                              '/opt/esp/esp-idf/components/freemodbus/serial_master/port',
                              '/opt/esp/esp-idf/components/freemodbus/common',
                              '/opt/esp/esp-idf/components/freemodbus/tcp_master/port',
                              '/opt/esp/esp-idf/components/freemodbus/tcp_slave/port',
                              '/opt/esp/esp-idf/components/freemodbus/tcp_slave/modbus_controller',
                              '/opt/esp/esp-idf/components/freemodbus/serial_master/modbus_controller',
                              '/opt/esp/esp-idf/components/freemodbus/serial_slave/modbus_controller',
                              '/opt/esp/esp-idf/components/freemodbus/tcp_master/modbus_controller',
                              '/opt/esp/esp-idf/components/idf_test/include',
                              '/opt/esp/esp-idf/components/idf_test/include_esp32',
                              '/opt/esp/esp-idf/components/jsmn/include',
                              '/opt/esp/esp-idf/components/json/cJSON',
                              '/opt/esp/esp-idf/components/libsodium/libsodium/src/libsodium/include',
                              '/opt/esp/esp-idf/components/libsodium/port_include',
                              '/opt/esp/esp-idf/components/libsodium/libsodium/src/libsodium/include/sodium',
                              '/opt/esp/esp-idf/components/libsodium/port',
                              '/opt/esp/esp-idf/components/libsodium/port_include/sodium',
                              '/opt/esp/esp-idf/components/mqtt/esp-mqtt/include',
                              '/opt/esp/esp-idf/components/openssl/include',
                              '/opt/esp/esp-idf/components/perfmon/include',
                              '/opt/esp/esp-idf/components/spiffs/include',
                              '/opt/esp/esp-idf/components/ulp/include',
                              '/opt/esp/esp-idf/components/wifi_provisioning/include',
        ])  

    else:
        print('ARCH={} is not yet supported'.format(env['ARCH']))
        env.Exit(2)

def Luminula(env, cmd_options):
    Common(env, cmd_options)

    env['MCU'] = 'ESP32'
    env['DEVICE'] = 'esp32dev'

    build_dir = env['BUILD_DIR']
    build_dir = os.path.join(build_dir, 'luminula')
    env['BUILD_DIR'] = build_dir

def Blink(env, cmd_options):
    Common(env, cmd_options)

    env.Append(CPPDEFINES=['CONFIG_BLINK_GPIO=2'])

    env['MCU'] = 'ESP32'
    env['DEVICE'] = 'esp32dev'

    build_dir = env['BUILD_DIR']
    build_dir = os.path.join(build_dir, 'blink')
    env['BUILD_DIR'] = build_dir
