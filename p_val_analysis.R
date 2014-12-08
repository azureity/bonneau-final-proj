data <- read.csv( file = "bonneau-final-proj/finaloutput.csv")

mat <- as.matrix(data)

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

location.array <- array(num.rows)
sorted.data <- sort.array(as.numeric(p.array[,2]),p.array[,1])

show(sorted.data)

plot(sorted.data[,2])


#################################
# Histogram of Prices
#################################

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

hist(prices)

