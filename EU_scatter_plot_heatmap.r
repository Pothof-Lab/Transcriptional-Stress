library(ggplot2)
aa <- read.csv("/media/jiang/BioData/EU-seq_paper/for_heatmap/scaled_1_to_20.csv", header = TRUE, sep=",")
head(aa)

ggplot(aa, aes(aa$length_log,color = aa$group)) +
  geom_density()+
  xlim(c(3,6))+
  coord_fixed(ratio = 1)+
  scale_color_manual(breaks = c("up","down","stressed","all"),
                     values=c("black","green","grey","red"))+
  theme_classic()


ggplot(aa, aes(aa$Log10.length,aa$Scaled.factor)) +
  theme_minimal()+
  geom_point()
  guides(fill=FALSE)+
  ylab("Transcription production factor")+
  geom_hline(yintercept = 0)+
  geom_vline(xintercept = 0)+
  coord_fixed(ratio = 1)
  


