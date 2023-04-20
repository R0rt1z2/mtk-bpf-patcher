try:
    from data.Types import FileTypes
except ImportError:
    from mtk_bpf_patcher.data.Types import FileTypes

class ByteSequences:
    signature_map = {
        b'ANDROID!': FileTypes.BOOT_IMAGE,
        b'\x1f\x8b\x08': FileTypes.IMAGE_GZ
    }

    '''The following mapping is used to revert the changes made by James Hsu's patch.'''
    array_map_update_elem = {
        bytes.fromhex("0a2450292801080a087d0a1b28010035") : bytes.fromhex("0a2450292801080a087d0a1b1f2003d5"), # 4.14
        bytes.fromhex("48010035822240b980420491e10313aa") : bytes.fromhex("1f2003d5822240b980420491e10313aa"), # 4.19
    }