lm_eqn = function(m) {
  
  l <- list(a = format(coef(m)[1], digits = 2),
            b = format(abs(coef(m)[2]), digits = 2),
            r2 = format(summary(m)$r.squared, digits = 3));
  
  if (coef(m)[2] >= 0)  {
    eq <- substitute(italic(y) == a + b %.% italic(x)*","~~italic(r)^2~"="~r2,l)
  } else {
    eq <- substitute(italic(y) == a - b %.% italic(x)*","~~italic(r)^2~"="~r2,l)    
  }
  
  as.character(as.expression(eq));                 
}


library(ggplot2)

micr1 <- read.csv("/media/jiang/BioData/TS_prelimary/merge_TSS_GB.csv", header = TRUE, sep=",")
micr2 <- read.csv("/media/jiang/BioData/TS_prelimary/1kb_gene_body.csv", header = TRUE, sep=",")
head(micr1)
head(micr2)


ggplot(micr1,aes(x =micr1$young_TR_log,y =micr1$old_TR_log)) +
  labs(x="young TR",y="old TR") +
  geom_point()+
  geom_hline(yintercept = 0)+
  geom_vline(xintercept = 0)+
  coord_fixed(ratio = 1)+
  guides(fill=FALSE)+
  xlim(-3,3)+
  ylim(-3,3)+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),aspect.ratio=1)



ggplot(micr2,aes(x =micr2$young_log,y =micr2$old_log)) +
  labs(x="1s tkb of gene body expression in young (log10)",y="1st kb of gene body expression in old (log10)") +
  geom_point()+
  geom_hline(yintercept = 0)+
  geom_vline(xintercept = 0)+
  coord_fixed(ratio = 1)+
  guides(fill=FALSE)+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),aspect.ratio=1)+
    geom_text(x = 1, y = 4, label = lm_eqn(lm(micr2$old_log ~ micr2$young_log, micr2)), parse = TRUE) 
