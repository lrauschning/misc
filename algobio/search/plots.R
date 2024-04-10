#!/usr/bin/Rscript
library(tidyverse)

benches <- read.csv("/tmp/benchmarks")

naive_benches <- filter(benches, algorithm=="naive")

dna_benches <- filter(benches, alphabet=="dna")
naive_dna_benches <- filter(dna_benches, algorithm=="naive")
kmp_dna_benches <- filter(dna_benches, algorithm=="kmp")
gs_bm_dna_benches <- filter(dna_benches, algorithm=="gs-boyer-moore")
bc_bm_dna_benches <- filter(dna_benches, algorithm=="bc-boyer-moore")

alnum_benches <- filter(benches, alphabet=="alnum")
naive_alnum_benches <- filter(alnum_benches, algorithm=="naive")
kmp_alnum_benches <- filter(alnum_benches, algorithm=="kmp")
gs_bm_alnum_benches <- filter(alnum_benches, algorithm=="gs-boyer-moore")
bc_bm_alnum_benches <- filter(alnum_benches, algorithm=="bc-boyer-moore")


ggplot(data = naive_benches, aes(x=text_length, y=time, color=pattern_length, shape=alphabet)) + 
	geom_point(size=2) +
	stat_smooth(data=naive_benches, method = lm, formula = y ~ poly(x, raw = TRUE))
ggsave("plot1b-time.png")

ggplot(data = naive_benches, aes(x=text_length, y=comps, color=pattern_length, shape=alphabet)) + 
	geom_point(size=2) +
	stat_smooth(data=naive_benches, method = lm, formula = y ~ poly(x, raw = TRUE))
ggsave("plot1b-comps.png")


ggplot(data = dna_benches, aes(x=text_length, y=time, color=pattern_length, shape=algorithm)) + 
	geom_point(size=2) +
	stat_smooth(data=naive_dna_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=kmp_dna_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=gs_bm_dna_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=bc_bm_dna_benches, method = lm, formula = y ~ poly(x, raw = TRUE))
ggsave("plot4c-dna.png")

ggplot(data = dna_benches, aes(x=text_length, y=comps, color=pattern_length, shape=algorithm)) + 
	geom_point(size=2) +
	stat_smooth(data=naive_dna_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=kmp_dna_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=gs_bm_dna_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=bc_bm_dna_benches, method = lm, formula = y ~ poly(x, raw = TRUE))
ggsave("plot4d-dna.png")

ggplot(data = alnum_benches, aes(x=text_length, y=time, color=pattern_length, shape=algorithm)) + 
	geom_point(size=2) +
	stat_smooth(data=naive_alnum_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=kmp_alnum_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=gs_bm_alnum_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=bc_bm_alnum_benches, method = lm, formula = y ~ poly(x, raw = TRUE))
ggsave("plot4c-alnum.png")

ggplot(data = alnum_benches, aes(x=text_length, y=comps, color=pattern_length, shape=algorithm)) + 
	geom_point(size=2) +
	stat_smooth(data=naive_alnum_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=kmp_alnum_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=gs_bm_alnum_benches, method = lm, formula = y ~ poly(x, raw = TRUE)) +
	stat_smooth(data=bc_bm_alnum_benches, method = lm, formula = y ~ poly(x, raw = TRUE))
ggsave("plot4d-alnum.png")
