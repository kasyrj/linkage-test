#!/usr/bin/Rscript
#
# Plot linkage test as a heatmap (X and Y axes are features, and temperature shows how high the degree of linkage is)
# date: 2015-01-20
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

#set logical to FALSE to include middle diagonal
M[lower.tri(M,TRUE)] <- NA

# Optional: Add symmetric row
#for (i in rownames(M))
#{
#	M[i,i] <- 1.0
#}
# TODO: moving axis to top
# axis(3, 1:213, labels = colnames(M), las = 2, line = -0.5 + 0.5, tick = 0, cex.axis = 0.2 + 1/log10(213), hadj = NA, padj = 0)

pdfFile <- paste(outputFileBase, ".pdf", sep = "")
svgFile <- paste(outputFileBase, ".svg", sep = "")
epsFile <- paste(outputFileBase, ".eps", sep = "")

gradient <- colorRampPalette(c("yellow","red"))

pdf(pdfFile, width=20, height=20)

heatmap.2(M,dendrogram='none',density.info='density',Colv=FALSE,na.color='aliceblue',Rowv=FALSE,trace='none',col=gradient,symm=TRUE)
dev.off()

svg(svgFile,width=20,height=20)
heatmap.2(M,dendrogram='none',density.info='density',Colv=FALSE,na.color='aliceblue',Rowv=FALSE,trace='none',col=gradient,symm=TRUE)
dev.off()

postscript(epsFile,horizontal=FALSE, paper = "special",width=20,height=20)
heatmap.2(M,dendrogram='none',density.info='density',Colv=FALSE,na.color='aliceblue',Rowv=FALSE,trace='none',col=gradient,symm=TRUE)
dev.off()
