#!/usr/bin/env python3.11

import argparse

try:
    from utils.logger import Logger
    from utils.parser import Parser
    from data.Sequences import ByteSequences
    from data.Types import FileTypes
except ImportError:
    from mtk_bpf_patcher.utils.logger import Logger
    from mtk_bpf_patcher.utils.parser import Parser
    from mtk_bpf_patcher.data.Sequences import ByteSequences
    from mtk_bpf_patcher.data.Types import FileTypes

def main() -> None:
    '''
    The main function.
    return: None
    '''
    # Parse the command line arguments.
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input_file", help="The input file")
    argparser.add_argument("output_file", help="The output file")
    argparser.add_argument("-l", "--log_file", help="The log file")
    argparser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = argparser.parse_args()

    # Initialize the logger and print the banner.
    logger = Logger(args.log_file, args.debug)
    logger.print_banner()

    # Determine the file type. This is automatically done by the parser's
    # constructor.
    parser = Parser(args.input_file, logger)

    # Try to get the kernel data (the binary itself).
    kernel_data = parser.get_kernel_data()

    # We've got the kernel data, now we need to find a matching sequence
    # in order to patch it.
    for bytes, replacement in ByteSequences.array_map_update_elem.items():
        # The following call will return None if the bytes sequence is not
        # found in the kernel data.
        patched_data = parser.patch_kernel_data(kernel_data, bytes, replacement)

        # If the patched data is not None, we've found a match.
        if patched_data is not None:
            logger.log(3, f"Found a match for '{bytes.hex()}'!")
            break # We don't need to keep looking for a match.

    # Double check that we've found a match.
    if patched_data is None:
        logger.log(2, "Unable to find a match for any of the sequences :(")

    # If the file type is a compressed image, we need to compress the patched
    # data.
    if parser.input_type == FileTypes.IMAGE_GZ:
        # Only add the .gz extension if it's not already there.
        if not args.output_file.endswith(".gz"):
            args.output_file = f'{args.output_file}.gz' # For consistency.
        logger.log(1, "Compressing the patched kernel binary...")
        patched_data = parser.gzip_compress(patched_data)

    # Write the patched data to the output file.
    with open(args.output_file, "wb") as f:
        f.write(patched_data)

    logger.log(3, f"Success. The patched kernel is available at {args.output_file}!")

if __name__ == "__main__":
    main()