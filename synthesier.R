# Load the libraries (if not already installed, install with install.packages("dplyr"))
library(dplyr)
library(ggplot2)
library(tidyr)
# Set a seed for reproducibility
set.seed(123)

# Original data
weekdays <- c(0.028, 0.245, 0.527, 0.872, 1, 0.918, 0.781, 0.718, 0.672, 0.636, 
              0.636, 0.663, 0.691, 0.745, 0.654, 0.509, 0.391, 0.282, 0.191, 0.118, 
              0.055, 0.045, 0.03, 0.032)



# SPLINE 
gntr <- function(x, a, b, dtype) {
  
  if (dtype == 'weekday') {
    x_points <- c(1-(0.1*a), 5-(0.13*a), 8, 12+(0.15*a), 16, 20-(0.1*a), 24)
    y_points <- 0.3*b*c(0.2+b, 0.8+b, 0.6+1.5*b, 0.9+b, 0.1+b, 0.5+b, 0.3+0.8*b)
    
    spline_interpolation <- spline(x_points, y_points, method = "fmm", n = 1000)
    
    interpolated_function <- function(x) {
      if (x < min(x_points)-5 || x > max(x_points)+5) {
        stop("x is outside the domain of the interpolated function")
      }
      approx(spline_interpolation$x, spline_interpolation$y, x)$y
    }
  }
  
  else if (dtype == 'sat') {
    x_points <- c(1, 5, 8, 12, 16, 20, 24)
    y_points <- 0.2*b*c(0.2+b, 0.8+b, 0.9+1.5*b, 0.9+b, 0.1+b, 0.5+b, 0.3+b)
    
    spline_interpolation <- spline(x_points, y_points, method = "fmm", n = 1000)
    
    interpolated_function <- function(x) {
      if (x < min(x_points)-5 || x > max(x_points)+5) {
        stop("x is outside the domain of the interpolated function")
      }
      approx(spline_interpolation$x, spline_interpolation$y, x)$y
    }
  }
  
  else {
    x_points <- c(1, 5, 8, 12, 16, 20, 24)
    y_points <- 0.25*b*c(0.2+b, 0.5+b, 0.6+1.5*b, 0.9+b, 0.65+b, 0.5+b, 0.3+0.1*b)
    
    spline_interpolation <- spline(x_points, y_points, method = "fmm", n = 1000)
    
    interpolated_function <- function(x) {
      if (x < min(x_points)-5 || x > max(x_points)+5) {
        stop("x is outside the domain of the interpolated function")
      }
      approx(spline_interpolation$x, spline_interpolation$y, x)$y
    }
  }
  
  # Example of using the function
  return (interpolated_function(x))
}



# Monday
mon <- sapply(weekdays, function(x) x + rnorm(1, mean = 0, sd = x * 0.004))
# Tuesday
tue <- sapply(weekdays, function(x) x + rnorm(1, mean = -0.01, sd = x * 0.002))
# Wednesday
wed <- sapply(weekdays, function(x) x + rnorm(1, mean = 0.05, sd = x * 0.002))
# Thursday
thu <- sapply(weekdays, function(x) x + rnorm(1, mean = 0.02, sd = x * 0.04))
# Friday 
fri <- sapply(weekdays, function(x) x + rnorm(1, mean = 0.08, sd = x * 0.02))
# Saturday
sat <- c(0.036, 0.082, 0.154, 0.291, 0.536, 0.763, 0.863, 0.909, 0.872, 0.845, 0.791, 0.654, 0.591, 0.509, 0.436, 0.336, 0.282, 0.273, 0.3, 0.264, 0.182, 0.082, 0.036, 0.027)
# Sunday
sun <- c(0.027, 0.082, 0.118, 0.245, 0.382, 0.509, 0.627, 0.645, 0.672, 0.691, 0.684, 0.609, 0.545, 0.454, 0.345, 0.282, 0.2, 0.173, 0.154, 0.127, 0.064, 0.032, 0.029, 0.22)



# Define the start and end times
start_time <- as.POSIXct("04:00", format = "%H:%M")
end_time <- as.POSIXct("03:00", format = "%H:%M") + 24 * 3600  # Plus 24 hours

# Generate the time sequence in 1-hour increments
time_axis <- seq(start_time, end_time, by = "1 hour")

# Format the times to exclude the date and show only the time of day
time_axis_formatted <- format(time_axis, format = "%I:%M %p")


#generate_day <- function(day_data, dfact, sfact) { # busy [-1, 1]
#  sapply(day_data, function(x) x + rnorm(1, mean=dfact*0.15+sfact*dnorm(0, 0.05), sd=x * 0.01 * dnorm(0, 0.025)))
#}

generate_day <- function(day_data, dfact, sfact, a, b, day_type) {
  time_variability = NULL
  sapply(seq_along(day_data), function(i) {
    base_variation <- rnorm(1, mean = dfact * 0.15 + sfact * dnorm(0, 0.05), sd = day_data[i] * 0.01 * dnorm(0, 0.025))
    time_variation <- if (!is.null(time_variability)) {
      # Example: more variation during peak hours (assuming index i represents time)
      peak_hours <- c(7:9, 17:19)  # Assuming these indices represent peak hours
      if (i %in% peak_hours) {
        rnorm(1, mean = 0, sd = 0.05)  # More variation during peak hours
      } else {
        0
      }
    } else {
      0
    }
    # Adding random outliers
    outlier <- if (runif(1) < 0.05) rnorm(1, mean = 0, sd = 2.5) else 0  # 5% chance of outlier
    
    day_data[i] + base_variation + time_variation + 0.08*gntr(i, a, b, day_type) + rnorm(1, 0, 0.135)
  })
}


# TRAIN LINE 1-16
train_lines_data <- vector("list", 16)

lookup1 = c(0.1, 0.2, -0.1, 0.9, 0.1, 0.2, -0.1, 1.2, 0.1, 0.2, -0.1, 0.3, 0.1, 0.2, -0.1, 0.3, -1.1, 0.3)
lookup2 = c(0.1, 0.2, -0.1, 1, 0.1, 0.2, -0.1, 1.3, 0.1, 0.2, -0.1, 0.3, 0.1, 0.2, -0.1, 0.3, -0.9, 0.3)
lookup3 = c(0.1, 0.2, -0.1, 0.8, 0.1, 0.2, -0.1, 1.1, 0.1, 0.2, -0.1, 0.3, 0.1, 0.2, -0.1, 0.3, -1.3, 0.4)

for (i in 1:16) {
  train_lines_data[[i]] <- list(
    a_mon = generate_day(mon, 0.2, lookup1[i], lookup2[i], lookup3[i], 'weekday'),
    b_tue = generate_day(tue, 0.1, lookup1[i], lookup2[i], lookup3[i], 'weekday'),
    c_wed = generate_day(wed, -0.12, lookup1[i], lookup2[i], lookup3[i], 'weekday'),
    d_thu = generate_day(thu, 0.1, lookup1[i], lookup2[i], lookup3[i], 'weekday'),
    e_fri = generate_day(fri, 0.3, lookup1[i], lookup2[i], lookup3[i], 'weekday'),
    f_sat = generate_day(sat, 0.7, lookup1[i], lookup2[i], lookup3[i], 'sat'), 
    g_sun = generate_day(sun, 0.8, lookup1[i], lookup2[i], lookup3[i], 'sun') 
  )
}



# Combine into a single data frame with a multi-level column structure
#train_lines_df <- do.call(cbind, train_lines_data)

train_lines_data

library(jsonlite)

# Convert the list to JSON
train_lines_json <- toJSON(train_lines_data, pretty = TRUE)

# Write to a JSON file
write(train_lines_json, file = "train_lines_data.json")


# Create a sequence for time points (assuming each day has 24 time points)
time_points <- 1:24

# Initialize an empty data frame
long_df <- data.frame(station = integer(), day = character(), time = integer(), value = numeric())

# Loop through each station and day to populate the data frame
for (station in 1:length(train_lines_data)) {
  for (day in names(train_lines_data[[station]])) {
    day_data <- train_lines_data[[station]][[day]]
    temp_df <- data.frame(station = station, day = day, time = time_points, value = day_data)
    long_df <- rbind(long_df, temp_df)
  }
}

# Convert 'station' and 'day' to factors for better plotting
long_df$station <- as.factor(long_df$station)
long_df$day <- as.factor(long_df$day)


# Create the scatterplot matrix
ggplot(long_df, aes(x = time, y = value)) +
  geom_point(shape=1) +
  facet_grid(day ~ station) +
  labs(title = "Scatterplot Matrix by Train Line and Day",
       x = "Time Point",
       y = "Value") +
  theme_bw() +
  theme(strip.text.x = element_text(angle = 90, hjust = 1))

# Adjust plot parameters as needed
# Note: Adjust 'theme_bw()' and 'labs()' according to your preference
# PARAMETERS
