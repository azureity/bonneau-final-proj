data <- read.csv( file = "bonneau-final-proj/finaloutput.csv")

mat <- as.matrix(data)

num.rows <- nrow(mat)

# P-Value Graph
p.array <- array(dim=c(num.rows,2))

for (n in 1:num.rows) {
  line <- as.character(mat[n,3]) 
  p_val <- gsub(".*,","",line)
  p_val_1 <- gsub(" ", "", p_val)
  p_val_2 <- gsub(")", "", p_val_1)
  p_val_fin <- as.numeric(p_val_2)
  rm(p_val,p_val_1,p_val_2)
  
  p.array[n,1] <- as.character(mat[n,1])
  p.array[n,2] <- p_val_fin
} rm(n)


new.array <- as.numeric(sort.int(p.array[,2]), decreasing = TRUE)

new.new.array <- array(dim=c(202,1))
for (i in 5735:num.rows) {
  new.new.array[i-5734] <- new.array[5735]
} 
rm(i)

show(new.array)

plot(new.array)


# Histogram of Prices
list <- as.character(mat[1,2])
list_1 <- gsub(",","", list)
list_2 <- gsub("'","",list_1)
list_3 <- gsub("\\[", "", list_2)
list_4 <- gsub("\\]", "", list_3)
rm(list, list_1, list_2, list_3)

new_list <- strsplit(list_4, " ")
vector <- c()

for (n in 1:length(new_list[[1]])) {
  vector[n] <- new_list[[1]][n]
} 
rm(n)

prices <- as.numeric(vector)

hist(prices, angle = 90)

