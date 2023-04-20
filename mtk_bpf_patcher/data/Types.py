import enum

class FileTypes(enum.Enum):
    """Supported types of input files."""
    BOOT_IMAGE = 0
    IMAGE_GZ   = 1 # TODO: Add support for other compressed image(s).
    KERNEL_BIN = 2
    UNKNOWN    = 3