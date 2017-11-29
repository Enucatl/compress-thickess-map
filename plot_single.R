#!/usr/bin/env Rscript

library(argparse)
library(ggplot2)
library(data.table)
library(ks)

parser <- ArgumentParser(description='plot local thickness density')
parser$add_argument('source', nargs=1)
parser$add_argument('output', nargs=1)
parser$add_argument('--title', nargs=1, help='title of the plot')
parser$add_argument('--batch', action='store_true', help='show plot if false')
parser$add_argument('--xmin', nargs='?', default=0, help='kde xmin')
parser$add_argument('--xmax', nargs='?', default=150, help='kde xmax')

args = parser$parse_args()
smooth.kde = readRDS(args$source)

size = seq(args$xmin, args$xmax, by=0.1)
density = predict(smooth.kde, x=size)

dt = data.table(size=size, density=density)

print(dt)

plot = ggplot(dt, aes(x=size, y=density)) +
    geom_line() +
    xlab("diameter (μm)") +
    labs(title=args$title)

width = 7
factor = 1
height = width * factor
if (!args$batch) {
    print(plot)
    invisible(readLines(con="stdin", 1))
}
ggsave(args$output, plot, width=width, height=height, dpi=300)
