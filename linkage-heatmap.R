#!/usr/bin/Rscript
#
# Plot linkage test as a heatmap (X and Y axes are features, and temperature shows how high the degree of linkage is)
# date: 2023-12-20
# author: Kaj Syrjänen
# install gplots library before using (install.packages("gplots")

library('gplots')

args = commandArgs(trailingOnly=TRUE)

outputFileBase <- 'linkage_heatmap' # If second parameter is not provided, the script will default to this output file base

if (length(args) == 0) {

    stop("Please specify input file as an argument, e.g. `Rscript --vanilla linkage_heatmap.r linkage_data.csv`",
         call.=FALSE) 

} else {

    inputFile <- args[1]
    if (length(args)==2) {
    outputFileBase <- args[2];

    }
}

mydata <- read.csv(inputFile, header=TRUE)

an <- with(mydata,unique(c(as.character(feature_a),as.character(feature_b))))
M <- array(0,c(length(an),length(an)), list(an,an))
newdata <- mydata[,c("feature_a","feature_b","linkage_percentage")]
i <- match(newdata$feature_a,an)
j <- match(newdata$feature_b,an)
M[cbind(i,j)] <- M[cbind(j,i)] <- newdata$linkage_percentage

# Remove lower triangle from heatmap; similarity of (A,B) === similarity of (B,A) for all pairs, so it gives us no extra information
M[lower.tri(M,TRUE)] <- NA

# Optional: Add symmetric diagonal; heat map values for these are 1.0, as all features perfectly match themselves.
# Uncomment the following rows to enable

# for (i in rownames(M))
#{
#	M[i,i] <- 1.0
#}

# Construct file names for output
pdfFile <- paste(outputFileBase, ".pdf", sep = "")
svgFile <- paste(outputFileBase, ".svg", sep = "")
epsFile <- paste(outputFileBase, ".eps", sep = "")

gradient <- colorRampPalette(c("yellow","red"))

# create PDF
pdf(pdfFile, width=20, height=20)
heatmap.2(M,dendrogram='none',density.info='density',Colv=FALSE,na.color='aliceblue',Rowv=FALSE,trace='none',col=gradient,symm=TRUE)
dev.off()

# create SVG
svg(svgFile,width=20,height=20)
heatmap.2(M,dendrogram='none',density.info='density',Colv=FALSE,na.color='aliceblue',Rowv=FALSE,trace='none',col=gradient,symm=TRUE)
dev.off()

# create EPS
postscript(epsFile,horizontal=FALSE, paper = "special",width=20,height=20)
heatmap.2(M,dendrogram='none',density.info='density',Colv=FALSE,na.color='aliceblue',Rowv=FALSE,trace='none',col=gradient,symm=TRUE)
dev.off()
