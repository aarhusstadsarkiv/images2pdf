from gooey import Gooey, GooeyParser
import img2pdf
from pathlib import Path

# From https://github.com/chriskiehl/Gooey/issues/207
# For disabling gooey, you can pass --ignore-gooey as a commandline arg when
# calling your file. For pre-filling items in Gooey, you can specify defaults
# in your argparse code:
# parser.add_argument("-f', '--foo', default="foobar")
# And they'll show in the form fields when Gooey loads.


@Gooey(program_name="Images2pdf",
       return_to_config=True,
       required_cols=1)
def parse_args():
    desc = "Konvertér en eller flere billedfiler til en enkelt flersidet PDF-fil."
    dir_input_msg = "Vælg en folder med billeder, der skal konverteres"
    save_file_msg = "Vælg placering og filnavn for pdf-filen"

    parser = GooeyParser(description=desc)
    parser.add_argument("in_folder",
                        metavar="Vælg mappe med billedfiler",
                        help=dir_input_msg,
                        widget="DirChooser")
    parser.add_argument("out_file",
                        metavar="Vælg hvor pdf-filen skal gemmes",
                        help=save_file_msg,
                        widget="FileSaver")

    return parser.parse_args()


def generate_pdf(image_folder, out_file):
    # image_folder and out_file are Path-objects
    files = []
    for fn in image_folder.rglob('*.*'):
        if fn.suffix in ['.png', '.jpg', '.jp2', '.jpeg']:
            files.append(str(fn))  # img2pdf.convert requirement

    # print("in_folder: " + args.in_folder)
    with open(out_file, "wb") as f:
        f.write(img2pdf.convert(files))


if __name__ == '__main__':
    args = parse_args()
    print("Arguments parsed")
    print("Generating pdf...")
    generate_pdf(Path(args.in_folder), Path(args.out_file))
    print("Pdf-file generated. Done")
