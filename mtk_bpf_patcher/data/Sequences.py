import struct

try:
    from data.Types import FileTypes
except ImportError:
    from mtk_bpf_patcher.data.Types import FileTypes

class ByteSequences:
    '''
    This class contains all the byte sequences that are used to identify
    the type of the input file. It also covers the known byte sequences
    that are used to identify the section of the kernel image that needs
    to be patched.
    '''
    signature_map = {
        b'ANDROID!': FileTypes.BOOT_IMAGE,
        b'\x1f\x8b\x08': FileTypes.IMAGE_GZ
    }

    '''The following mapping is used to revert the changes made by James Hsu's patch.'''
    array_map_update_elem = {
        bytes.fromhex("0a2450292801080a087d0a1b28010035") : bytes.fromhex("0a2450292801080a087d0a1b1f2003d5"), # 4.14
        bytes.fromhex("48010035822240b980420491e10313aa") : bytes.fromhex("1f2003d5822240b980420491e10313aa"), # 4.19
    }

    boot_image_header = struct.Struct('8s I I I I I I I I I 4x 16s 512s 8x')