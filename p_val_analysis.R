data <- read.csv( file = "bonneau-final-proj/finaloutput.csv")

mat <- as.matrix(data)

#################################
# Sorting
#################################
sort.array = function(input,locations) {
  num_passes = 0
  while(1) {
    num_swaps = 0
    for (x in 1 :((length(input)-1)-num_passes)) {
      if (input[x] > input[x+1]) {
        ## Price Sorting
        temp = input[x]
        input[x] = input[x+1]
        input[x+1] = temp
        ## Respective Location Sorting
        temp_2 = locations[x]
        locations[x] = locations[x+1]
        locations[x+1] = temp_2
        
        num_swaps = num_swaps + 1
      }
    }
    num_passes = num_passes + 1
    if(num_swaps == 0) break
  }
  
  result <- cbind(locations, input)
  return(result)
}

#################################
# P-Value Graph
#################################

num.rows <- nrow(mat)

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
} 
rm(n)

location.array <- array(dim=num.rows)
sorted.data <- sort.array(as.numeric(p.array[,2]),p.array[,1])

show(sorted.data)

plot(sorted.data[,2])

write.csv(format(sorted.data, scientific=FALSE), file = "sorted_p_vals.csv")


#################################
# Reduced Graph
#################################

reduced.array <- array(dim=219)
for (x in 9000:9219) {
  reduced.array[x-8999] <- sorted.data[x,2]
}

plot(reduced.array)
  

#################################
# Histogram of Prices
#################################

# Example of smallest p val (0)
plot.histogram <- function(mat,row) {
  list <- as.character(mat[row,2])
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
  
  h<-hist(prices, breaks=10, col="red", xlab="Miles Per Gallon", 
          main="Histogram with Normal Curve") 
  xfit<-seq(min(prices),max(prices),length=40) 
  yfit<-dnorm(xfit,mean=mean(prices),sd=sd(prices)) 
  yfit <- yfit*diff(h$mids[1:2])*length(prices) 
  lines(xfit, yfit, col="blue", lwd=2)
}
# Example of smallest p val (0)
plot.histogram(mat,1)

# Example of largest p val
lg_pval_location <- sorted.data[num.rows-4000]
lg_pval_index <- -1
for (x in 1:num.rows) {
  if (mat[x,1] == lg_pval_location) {
    lg_pval_index <- x
  }
}


plot.histogram(mat,lg_pval_index)


#################################
# Average Graph
#################################

neighborhood_ref <- read.csv("bonneau-final-proj/neighborhood_ref.txt")
num_neighborhoods <- nrow(neighborhood_ref)

avg_prices <- array(0, dim=num_neighborhoods)
prices_count <- array(0, dim=num_neighborhoods)
index <- 1;
for (y in 1:length(mat[,1])){
  base_sum <- 0
  char_cpy <- toString(as.character(mat[y,1]))
  char_split <-strsplit(char_cpy,",")
  index <- as.numeric(gsub("\\(", "", char_split[[1]][1]))
  
  #function?
  list <- as.character(mat[y,2])
  list_1 <- gsub(",","", list)
  list_2 <- gsub("'","",list_1)
  list_3 <- gsub("\\[", "", list_2)
  list_4 <- gsub("\\]", "", list_3)
  new_list <- strsplit(list_4, " ")
  vector <- c()
  for (n in 1:length(new_list[[1]])) {
    vector[n] <- new_list[[1]][n]
  }
  prices <- as.numeric(vector)
  rm(list, list_1, list_2, list_3, list_4, new_list, vector)
  
  
  for (z in 1:length(prices)) {
    base_sum <- base_sum + prices[z]
    prices_count[index] <- prices_count[index] + 1
  }
  avg_prices[index] <- avg_prices[index] + base_sum
}

for (x in 1:length(avg_prices)) {
  avg_prices[x] <- avg_prices[x]/prices_count[x]
}