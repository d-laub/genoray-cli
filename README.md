# genoray-cli
CLI for genoray

### `view` — subset an SVAR

Subset an existing SVAR by region(s) and/or sample(s), writing to a new SVAR directory. Variants whose minor allele count is 0 in the chosen sample subset are dropped from the output.

```text
# Inline region + inline samples
genoray view SOURCE.svar OUT.svar -r chr1:100-200 -s A,B,C

# BED file + sample-name file
genoray view SOURCE.svar OUT.svar -R regions.bed -S samples.txt

# Comma-list of regions
genoray view SOURCE.svar OUT.svar -r chr1:1-100,chr2:200-300 -s A

# Regions only (all samples kept)
genoray view SOURCE.svar OUT.svar -r chr1:1-100

# Samples only (all variants kept)
genoray view SOURCE.svar OUT.svar -s A
```

At least one of `--regions/--regions-file` or `--samples/--samples-file` is required. Region coordinates use bcftools conventions: `chrom:start-end` is 1-based inclusive when inline; BED files are 0-based half-open as usual.
