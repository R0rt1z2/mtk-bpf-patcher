import os
import gzip
import struct

try:
    from data.Types import FileTypes
    from data.Sequences import ByteSequences
except ImportError:
    from mtk_bpf_patcher.data.Types import FileTypes
    from mtk_bpf_patcher.data.Sequences import ByteSequences

class Parser:
    def __init__(self, input, logger) -> None:
        '''
        Constructor for the parser.
        @param input: The input file.
        @param logger: The logger object.
        return: None
        '''
        self.logger = logger
        self.input_handle = None
        self.input = os.path.abspath(input)

        # Try to open the input file and save its handle.
        try:
            self.input_handle = open(self.input, "rb")
        except FileNotFoundError:
            logger.log(2, f"Input file '{input}' does not exist!")
        except OSError:
            logger.log(2, f"Error: could not open input file '{input}'!")
        if not os.path.isfile(input):
            logger.log(2, f"Input file '{input}' does not exist!")

        # Decide the type of the input file.
        self.input_type = self.decide_type()

    def __del__(self) -> None:
        '''
        Destructor for the parser.
        return: None
        '''
        if self.input_handle:
            try:
                self.input_handle.close()
            except OSError:
                exit("FATAL: could not close input file!")

    def read_and_seek(self, size, offset = 0, handle = None) -> bytes:
        '''
        Reads the specified amount of bytes from the input file.
        @param size: The amount of bytes to read.
        @param offset: The offset to seek to after reading.
        @param handle: The handle to read from.
        return: The data that was read.
        '''
        # Let the user specify a handle to read from.
        if not handle:
            handle = self.input_handle

        # Read the amount of bytes specified and seek back to the given
        # offset.
        data = handle.read(size)
        handle.seek(offset)

        # Return what we read.
        return data

    def seek_and_read(self, offset, size) -> bytes:
        '''
        Seeks to the specified offset and reads the specified amount of bytes.
        @param offset: The offset to seek to.
        @param size: The amount of bytes to read.
        return: The data that was read.
        '''

        # Seek to the specified offset and read the specified amount of bytes.
        self.input_handle.seek(offset)
        return self.input_handle.read(size)

    def decide_type(self) -> FileTypes:
        '''
        Decides the type of the input file.
        return: The type of the input file.
        '''
        # We use the first 8 bytes as a reference to determine the type of the input file.
        header = self.read_and_seek(8, 0)

        # Check if the header contains any of the supported signatures.
        for signature, file_type in ByteSequences.signature_map.items():
            if signature in header or signature in header[::-1]:
                self.logger.log(0, f"Detected {file_type.name} for {self.input}!")
                return file_type

        # No known signature was found default to binary and hope for the best.
        self.logger.log(1, f"Could not detect file type for {self.input}! Defaulting to binary.")
        return FileTypes.KERNEL_BIN

    def gzip_decompress(self, data) -> bytes:
        '''
        Decompresses the given data using gzip.
        @param data: The data to decompress.
        return: The decompressed data.
        '''
        try:
            return gzip.decompress(data)
        except zlib.error as e:
            self.logger.log(2, e)

    def gzip_compress(self, data) -> bytes:
        '''
        Compresses the given data using gzip.
        @param data: The data to compress.
        return: The compressed data.
        '''
        try:
            return gzip.compress(data, compresslevel=9) # Default to MAX compression ratio.
        except Exception as e:
            self.logger.log(2, e)

    def get_kernel_data(self) -> bytes:
        '''
        Returns the kernel (binary) data from the input file.
        return: The kernel data.
        '''
        # If the input file is a kernel binary already, we don't need to do anything.
        if self.input_type == FileTypes.KERNEL_BIN:
            return self.read_and_seek(os.path.getsize(self.input))

        # If the input file is a compressed image, we need to decompress it.
        if self.input_type == FileTypes.IMAGE_GZ:
            self.logger.log(1, f"Decompressing {self.input}...")
            return self.gzip_decompress(self.read_and_seek(os.path.getsize(self.input)))

        # We don't support boot images yet.
        if self.input_type == FileTypes.BOOT_IMAGE:
            self.logger.log(1, f"Extracting kernel from {self.input}...")
            # Extract the kernel from the boot image.
            self.input_handle.seek(0x4040 if self.input_handle.read(4) == b'BFBF' else 0)

            # Use the header to extract the kernel information.
            magic, kernel_size, kernel_addr, ramdisk_size, ramdisk_addr, second_size, second_addr, \
                tags_addr, page_size, dt_size, name, cmdline = ByteSequences.boot_image_header.unpack(self.input_handle.read(ByteSequences.boot_image_header.size))

            # Decide the type again since we don't know if the kernel is compressed or not.
            self.input_handle.seek(page_size) # So decide_type() can read the header(s).
            self.input_type = self.decide_type()

            if self.input_type == FileTypes.IMAGE_GZ:
                # Decompress the kernel.
                return self.gzip_decompress(self.seek_and_read(page_size, kernel_size))
            else:
                # Return the kernel.
                return self.seek_and_read(page_size, kernel_size)

            self.logger.log(2, f"Could not extract kernel from boot image!")

    def patch_kernel_data(self, data, bytes, replacement) -> bytes:
        '''
        Patches the kernel data by replacing the given bytes sequence with the given replacement.
        @param data: The kernel data to patch.
        @param bytes: The bytes sequence to replace.
        @param replacement: The replacement for the bytes sequence.
        return: The patched kernel data.
        '''
        # Make sure the bytes sequence is in the kernel data.
        if bytes not in data:
            self.logger.log(4, f"Could not find '{bytes.hex()}' in the kernel data!") # This is fine, we might be trying multiple sequences.
            return None

        # Replace the bytes sequence with the replacement.
        return data.replace(bytes, replacement)
