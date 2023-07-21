connect_to_database <- function(db_name) {
  db_location <- file.path("standup_db", db_name)


  con <- dbConnect(RSQLite::SQLite(), dbname=db_location)
  print(glue::glue("db_location: {db_location}\n\n"))
  return(con)
}
