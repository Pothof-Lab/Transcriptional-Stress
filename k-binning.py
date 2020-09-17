import argparse
import sys

from deeptools import parserCommon
from deeptools import heatmapper
from deeptools._version import __version__


def parseArguments(args=None):
    parser = \
        argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""

This tool summarizes and prepares an intermediary file containing
scores associated with genomic regions.  Typically, these genoic regions are
genes, but any other regions defined in a BED or interval format can be
used. This tool can also be used to filter and sort regions according
to their score.

To learn more about the specific parameters type:

%(prog)s reference-point --help or
%(prog)s scale-regions --help

""",
            epilog='An example usage is:\n  %(prog)s reference-point -S '
            '<biwig file> -R <bed file> -b 1000\n \n')

    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    subparsers = parser.add_subparsers(
        title='Commands',
        dest='command',
        metavar='')

    # scale-regions mode options
    scaleRegions = subparsers.add_parser(
        'scale-regions',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=[parserCommon.computeMatrixRequiredArgs(),
                 parserCommon.computeMatrixOutputArgs(),
                 parserCommon.computeMatrixOptArgs(case='scale-regions')],
        help="In the scale-regions mode, all regions in the BED file are "
        "stretched or shrunk to the same length (bp) that is indicated by "
        "the user.",
        usage='An example usage is:\n  %(prog)s -S '
        '<biwig file> -R <bed file> -b 1000\n \n')


    # reference point arguments
    refpoint = subparsers.add_parser(
        'reference-point',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=[parserCommon.computeMatrixRequiredArgs(),
                 parserCommon.computeMatrixOutputArgs(),
                 parserCommon.computeMatrixOptArgs(case='reference-point')],
        help="Reference-point refers to a position within the BED regions "
        "(e.g start of region). In the reference-point, mode only those "
        "genomic positions before (downstream) and/or after (upstream) the "
        "reference point will be plotted.",
        usage='An example usage is:\n  %(prog)s -S '
        '<biwig file> -R <bed file> -a 3000 -b 3000\n\ n')

    args = parser.parse_args(args)

    if args.quiet is False:
        args.verbose = True
    else:
        args.verbose = False

    if args.command == 'scale-regions':
        args.nanAfterEnd = False
        args.referencePoint = None
    elif args.command == 'reference-point':
        if args.beforeRegionStartLength == 0 and \
                args.afterRegionStartLength == 0:
            sys.stderr.write("\nUpstrean and downstream regions are both "
                             "set to 0. Nothing to output. Maybe you want to "
                             "use the scale-regions mode?\n")
            exit()

    return(args)


def main(args):
    parameters = {'upstream': args.beforeRegionStartLength,
                  'downstream': args.afterRegionStartLength,
                  'body': args.regionBodyLength,
                  'bin size': args.binSize,
                  'ref point': args.referencePoint,
                  'verbose': args.verbose,
                  'bin avg type': args.averageTypeBins,
                  'missing data as zero': args.missingDataAsZero,
                  'min threshold': args.minThreshold,
                  'max threshold': args.maxThreshold,
                  'scale': args.scale,
                  'skip zeros': args.skipZeros,
                  'nan after end': args.nanAfterEnd,
                  'proc number': args.numberOfProcessors,
                  }

    hm = heatmapper.heatmapper()

    hm.computeMatrix(args.scoreFileName.name, args.regionsFileName,
                     parameters, verbose=args.verbose)
    if args.sortRegions != 'no':
        hm.sortMatrix(sort_using=args.sortUsing, sort_method=args.sortRegions)

    hm.saveMatrix(args.outFileName)

    if args.outFileNameMatrix:
        hm.saveMatrixValues(args.outFileNameMatrix)

    if args.outFileNameData:
        hm.saveTabulatedValues(args.outFileNameData)

    if args.outFileSortedRegions:
        hm.saveBED(args.outFileSortedRegions)


if __name__ == "__main__":
    args = parseArguments()
    main(args)
