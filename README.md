# linkage-test

A simple Python3 program to perform the linkage test originally proposed in Syrjänen et al. (2016). The repository also includes an R script to help visualize the results as a heatmap.

If you use this tool in your research, please cite the paper Syrjänen et al. (2016).

## Basic usage of linkage test

Ensure you have Python3 installed. For an overview of command line options see `linkage-test.py --help`

Basic analysis of the test data with the following settings:

- input file `example-data/testdata.csv`,
- present characters are indicated by `1`,
- absent characters are indicated by `0`,
- missing characters are indicated by `-`,
- output is stored in file `results.csv`: 

`linkage-test.py -i "example-data/testdata.csv" -p "1" -m "-" -a "0" -o "results.csv"`

## Basic visualization with R

Ensure your R has `gplots` installed.

The following creates plots in SVG, PDF and EPS formats with the file names `visualization.svg`, `visualization.pdf` and `visualization.eps` based on linkage test results in file `results.csv`

`Rscript linkage-heatmap.R results.csv visualization`

## References

Syrjänen, Kaj, Terhi Honkola, Jyri Lehtinen, Antti Leino and Outi Vesakoski.
2016. Applying population genetic approaches within languages: Finnish
dialects as linguistic populations. _Language Dynamics and Change_ 6.235-83.
[DOI: https://doi.org/10.1163/22105832-00602002](https://doi.org/10.1163/22105832-00602002)
