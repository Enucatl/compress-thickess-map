#!/usr/bin/env Rscript

library(argparse)
library(data.table)
library(ks)

parser <- ArgumentParser(description='kde smoothing of thickness map distribution')
parser$add_argument('source', nargs=1)
parser$add_argument('output', nargs=1)
parser$add_argument('--density_bw', nargs='?', default=2, help='density bandwidth')
parser$add_argument('--pixel_size', nargs='?', default=0.6, help='pixel size (um)')
parser$add_argument('--gridsize', nargs='?', default=512, help='kde gridsize')
parser$add_argument('--bgridsize', nargs='?', default=512, help='kde bgridsize')
parser$add_argument('--xmin', nargs='?', default=0, help='kde xmin')
parser$add_argument('--xmax', nargs='?', default=300, help='kde xmax')

args <- parser$parse_args()
dt = fread(paste("zcat", args$source))

#remove first row
dt = dt[-1]

#convert pixels to um
dt[, size := size * args$pixel_size]

print(dt)

thickness_map = kde(
    dt[, size],
    h=args$density_bw,
    gridsize=args$gridsize,
    xmin=args$xmin,
    xmax=args$xmax,
    binned=TRUE,
    bgridsize=args$bgridsize,
    w=dt[, counts])
saveRDS(thickness_map, args$output)
