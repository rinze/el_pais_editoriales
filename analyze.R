library(rjson)
library(dplyr)
library(ggplot2)

opeds <- fromJSON(file = "elpais_opeds_full.json.gz")

# Create a data.frame with the relevant information
Sys.setlocale("LC_TIME", "es_ES.UTF-8")
tags <- lapply(opeds, function(x) {
            date <- x$date
            date <- strsplit(date, "-")
            date <- trimws(date[[1]][1])
            date <- as.Date(date, "%d %b %Y")
            dd <- data.frame(date = as.character(date),
                             tags = as.character(x$tags))
            return(dd)
})

tags <- do.call(rbind, tags)

# Year column
tags$year <- strftime(tags$date, "%Y")

# Get number of editorials published per year
#n_year <- tags %>% group_by(year) %>% summarise(n_year = n())
#tags <- left_join(tags, n_year)

# Count
counts <- tags %>% 
    group_by(year, tags) %>% 
    # Get the absolute count and a normalized count so we can include 2016
    summarise(count = n())#,
    #          wcount = n() / n_year) #%>%
    #arrange(desc(count)) #%>%
    #top_n(10)

plt1 <- ggplot(filter(counts, tags %in% c("Economía", "Venezuela", "Podemos"))) + 
        geom_point(aes(x = year, y = count, color = tags), stat = "identity")
print(plt1)
